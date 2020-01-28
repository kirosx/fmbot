from telebot import TeleBot
from db.maindb import Database
from utils import *
from db.dbclass import PaymentRecord, User, DebtRecord, UserCategory
from config import *
from keyboard import Keyboard
from charts.chart import ChartBuilder


class AbstractHandler:
    def __init__(self, bot):
        self.db = Database()
        self.bot = bot
        self.keyboard = Keyboard()


class HandlerRecord(AbstractHandler):
    def __init__(self, bot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: command_checker(m.text, PAY_TYPES))
        def make_record(message):
            payment_type, value, target = message.text.split()
            payment = PaymentRecord(message.from_user.id, payment_type, value, target)
            self.db.session.add(payment)
            self.db.session.commit()
            self.bot.send_message(message.from_user.id, REC + message.text,
                                  reply_markup=self.keyboard.delete_record_button(payment))

        @self.bot.message_handler(func=lambda m: command_checker(m.text, DEBT_TYPES))
        def make_debt_record(message):
            typ, val, tar = message.text.split()
            debt = DebtRecord(message.from_user.id, typ, val, tar)
            self.db.session.add(debt)
            self.db.session.commit()
            self.bot.send_message(message.from_user.id, debt.return_message())
            full_debt = self.db.full_debt_for_person(message.from_user.id, debt.person)
            self.bot.send_message(message.from_user.id, debt_message(full_debt, debt.person))


class HandlerCommands(AbstractHandler):
    def __init__(self, bot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            user = self.db.find_user_by_tgid(message.from_user.id)
            if not user:
                new_user = User(message.from_user.first_name, message.from_user.id, message.from_user.username)
                self.db.session.add(new_user)
                self.db.session.commit()
                self.bot.send_message(new_user.tgid, new_user.welcome_message())
            self.bot.send_message(message.from_user.id, f'{WELCOME} {message.from_user.first_name}',
                                  reply_markup=self.keyboard.main_menu())

        @self.bot.message_handler(commands=['help'])
        def help_message(message):
            self.bot.send_message(message.from_user.id, HELPMESSAGE, parse_mode='HTML')


class HandlerReport(AbstractHandler):
    report_dict = REPORTDICT

    def __init__(self, bot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text in self.report_dict.keys())
        def day_report(message):
            user = message.from_user.id
            days = self.report_dict[message.text]
            day_payments = self.db.select_payments_from_days(user, days)
            if not day_payments:
                self.bot.send_message(user, NOPAY)
                return
            for record in day_payments:
                self.bot.send_message(user, record.return_message())
            chart = ChartBuilder(day_payments, user, days)
            self.bot.send_message(user, TOTAL + str(self.db.total_sum(day_payments)),
                                  reply_markup=self.keyboard.chart_menu(user, days, chart.menu_chart))


class HandlerCallback(AbstractHandler):
    def __init__(self, bot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.callback_query_handler(func=lambda c: callback_delete_payment_checker(c.data, c.from_user.id))
        def delete_record(callback):
            com, user, target = callback.data.split()
            if com == 'del':
                record = self.db.payments.filter(PaymentRecord.id == int(target),
                                                 PaymentRecord.user_tgid == int(user)).first()
                if record:
                    self.db.session.delete(record)
                    self.db.session.commit()
                    self.bot.send_message(callback.from_user.id, DELETED)
                if not record:
                    self.bot.send_message(callback.from_user.id, NOTFOUND)
            for i in self.db.all_debs_for_person(user, target):
                self.bot.send_message(user, i.return_message())

        @self.bot.callback_query_handler(func=lambda c: chart_callback_checker(c.data, c.from_user.id))
        def show_chart(callback):
            type_chart, user, days = callback.data.split()[1:]
            newchart = ChartBuilder(self.db.select_payments_from_days(int(user), int(days)), int(user), int(days))
            newchartname = newchart.build_chart_for_callback(type_chart)
            self.bot.send_photo(callback.from_user.id, open(newchartname, 'rb'))
            newchart.delete_all_charts()


class HandlerDebt(AbstractHandler):
    def __init__(self, bot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text == DEBTS)
        def return_debts(message):
            debtors = self.db.not_null_debtors(message.from_user.id)
            if not debtors:
                self.bot.send_message(message.from_user.id, NODEBTS)
                return
            for k, v in debtors.items():
                msg = f'You owe to {k}\n{v}' if v < 0 else f'{k} owe you\n{v}'
                self.bot.send_message(message.from_user.id, msg,
                                      reply_markup=self.keyboard.all_debts(message.from_user.id, k))


class HandlerCategories(AbstractHandler):
    def __init__(self, bot: TeleBot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.callback_query_handler(func=lambda c: category_command_checker(c.data))
        def saving_new_category(c):
            if int(c.data.split()[1]) == c.from_user.id:
                self.bot.send_message(c.from_user.id, NAMECAT, reply_markup=self.keyboard.cancel_button())
                self.bot.register_next_step_handler_by_chat_id(c.from_user.id, save_category)

        def save_category(message):
            user = message.from_user.id
            if message == CANCEL:
                self.bot.delete_message(message_id=message.id)
                self.bot.send_message(user, CANCEL, reply_markup=self.keyboard.main_menu())
                return
            if message.text.upper() not in [i.category for i in self.db.user_categories(user)]:
                new_category = UserCategory(user, message.text.upper())
                self.db.session.add(new_category)
                self.db.session.commit()
            else:
                self.bot.send_message(message.from_user.id, ALLREADYCAT)

        @self.bot.callback_query_handler(func=lambda c: category_delete_checker(c.data))
        def delete_category(c):
            user, category = c.data.split()[1:]
            obj = self.db.return_single_category(int(user), category)
            if obj:
                self.db.session.delete(obj)
                self.db.session.commit()
                self.bot.send_message(int(user), f'{CATDELETED}{category}')



class HandlerProfile(AbstractHandler):
    def __init__(self, bot):
        super().__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text in PROFILE_BUTTONS)
        def profile_answer(m):
            user = m.from_user.id
            if m.text == PROFILE_BUTTONS[0]:
                self.bot.send_message(user, self.db.find_user_by_tgid(user).welcome_message())
                user_categories = self.db.user_categories(user)
                if not user_categories:
                    self.bot.send_message(user, NOCAT, reply_markup=self.keyboard.add_category(user))
                    return
                self.bot.send_message(user, YOURCAT)
                for i in user_categories:
                    self.bot.send_message(user, i.category, reply_markup=self.keyboard.watch_or_delete_category(user, i.category))
                self.bot.send_message(user, f'{ALLCAT} {len(user_categories)}', reply_markup=self.keyboard.add_category(user))
                return
            self.bot.send_message(m.from_user.id, MAIL)

        @self.bot.message_handler(func=lambda m: True)
        def any_message(m):
            self.bot.send_message(m.from_user.id, UNRCG)

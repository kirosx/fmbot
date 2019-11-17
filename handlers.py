from telebot import TeleBot
from db.maindb import Database
from utils import command_checker, allow_user, callback_delete_checker, debt_message
from db.dbclass import PaymentRecord, User, DebtRecord
from config import SPENT, EARN, TOTAL, NOPAY, PAY_TYPES, DEBT_TYPES
from keyboard import Keyboard


class HandlerRecord:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.db = Database()
        self.keyboard = Keyboard()

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: all((command_checker(m.text, PAY_TYPES), allow_user(m.from_user.id))))
        def make_record(message):
            payment_type, value, target = message.text.split()
            payment = PaymentRecord(message.from_user.id, payment_type, value, target)
            self.db.session.add(payment)
            self.db.session.commit()
            self.bot.send_message(message.from_user.id, 'RECORDED\n' + message.text,
                                  reply_markup=self.keyboard.delete_record_button(payment))

        @self.bot.message_handler(func=lambda m: all((command_checker(m.text, DEBT_TYPES), allow_user(m.from_user.id))))
        def make_debt_record(message):
            typ, val, tar = message.text.split()
            debt = DebtRecord(message.from_user.id, typ, val, tar)
            self.db.session.add(debt)
            self.db.session.commit()
            self.bot.send_message(message.from_user.id, debt.return_message())
            full_debt = self.db.full_debt_for_person(message.from_user.id, debt.person)
            self.bot.send_message(message.from_user.id, debt_message(full_debt, debt.person))

    #  @self.bot.message_handler(func=lambda m: True)
    # def unknown_command(message):
    #    self.bot.send_message(message.from_user.id, 'UNRECOGNIZED COMMAND')


class HandlerCommands:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.db = Database()
        self.keyboard = Keyboard()

    def run_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            user = self.db.find_user_by_tgid(message.from_user.id)
            if not user:
                new_user = User(message.from_user.first_name, message.from_user.id, message.from_user.username)
                self.db.session.add(new_user)
                self.db.session.commit()
                self.bot.send_message(new_user.tgid, new_user.welcome_message())
            self.bot.send_message(user.tgid, f'Welcome to familybot you are registered as {user.name}',
                                  reply_markup=self.keyboard.main_menu())


class HandlerReport:
    report_dict = {
        'Выписка за день': 1,
        'Выписка за неделю': 7,
        'Выписка за месяц': 30
    }

    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.db = Database()
        self.keyboard = Keyboard()

        # @self.bot.message_handler(commands=['all'])
        # def report_all_for_user(message):
        #     # for record in self.db.show_records_by_tgid(message.from_user.id):
        #     self.bot.send_message(message.from_user.id, self.db.show_recs_tabulate_by_user(message.from_user.id))
        #     self.bot.send_message(message.from_user.id, TOTAL + str(self.db.total_result_for_user(message.from_user.id)))
        #
        # @self.bot.message_handler(commands=['minus'])
        # def report_minus_user(message):
        #     query = self.db.show_minus_from_user(message.from_user.id)
        #     for i in query:
        #         self.bot.send_message(message.from_user.id, i)
        #     self.bot.send_message(message.from_user.id, SPENT + str(self.db.abs_sum_of_values(query)))
        #
        # @self.bot.message_handler(commands=['plus'])
        # def report_minus_user(message):
        #     query = self.db.show_plus_from_user(message.from_user.id)
        #     for i in query:
        #         self.bot.send_message(message.from_user.id, i)
        #     self.bot.send_message(message.from_user.id, EARN + str(self.db.abs_sum_of_values(query)))
    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text in self.report_dict.keys())
        def day_report(message):
            day_payments = self.db.select_payments_from_days(message.from_user.id, self.report_dict[message.text])
            if not day_payments:
                self.bot.send_message(message.from_user.id, NOPAY)
                return
            for record in day_payments:
                self.bot.send_message(message.from_user.id, record.return_message())
            self.bot.send_message(message.from_user.id, TOTAL + str(self.db.total_sum(day_payments)))


class HandlerCallback:
    def __init__(self, bot: TeleBot):
        self.db = Database()
        self.bot = bot
        self.keyboard = Keyboard()

    def run_handlers(self):
        @self.bot.callback_query_handler(func=lambda c: callback_delete_checker(c.data, c.from_user.id))
        def delete_record(callback):
            com, obj_id, user = callback.data.split()
            record = self.db.payments.filter(PaymentRecord.id == int(obj_id),
                                             PaymentRecord.user_tgid == int(user)).first()
            if record:
                self.db.session.delete(record)
                self.db.session.commit()
                self.bot.send_message(callback.from_user.id, 'Удалено!')

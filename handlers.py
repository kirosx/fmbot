from telebot import TeleBot
from db.maindb import Database
from utils import command_checker, allow_user
from db.dbclass import PaymentRecord, User
from config import SPENT, EARN, TOTAL, NOPAY


class HandlerRecord:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.db = Database()

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: all((command_checker(m.text), allow_user(m.from_user.id))))
        def make_record(message):
            payment_type, value, target = message.text.split()
            payment = PaymentRecord(message.from_user.id, payment_type, value, target)
            self.db.session.add(payment)
            self.db.session.commit()
            self.bot.send_message(message.from_user.id, 'RECORDED')

    #  @self.bot.message_handler(func=lambda m: True)
    # def unknown_command(message):
    #    self.bot.send_message(message.from_user.id, 'UNRECOGNIZED COMMAND')


class HandlerCommands:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.db = Database()

    def run_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            user = self.db.find_user_by_tgid(message.from_user.id)
            if not user:
                new_user = User(message.from_user.first_name, message.from_user.id, message.from_user.username)
                self.db.session.add(new_user)
                self.db.session.commit()
                self.bot.send_message(new_user.tgid, new_user.welcome_message())
            self.bot.send_message(user.tgid, f'Welcome to familybot you are registered as {user.name}')

        @self.bot.message_handler(commands=['all'])
        def report_all_for_user(message):
            # for record in self.db.show_records_by_tgid(message.from_user.id):
            self.bot.send_message(message.from_user.id, self.db.show_recs_tabulate_by_user(message.from_user.id))
            self.bot.send_message(message.from_user.id, TOTAL + str(self.db.total_result_for_user(message.from_user.id)))

        @self.bot.message_handler(commands=['minus'])
        def report_minus_user(message):
            query = self.db.show_minus_from_user(message.from_user.id)
            for i in query:
                self.bot.send_message(message.from_user.id, i)
            self.bot.send_message(message.from_user.id, SPENT + str(self.db.abs_sum_of_values(query)))

        @self.bot.message_handler(commands=['plus'])
        def report_minus_user(message):
            query = self.db.show_plus_from_user(message.from_user.id)
            for i in query:
                self.bot.send_message(message.from_user.id, i)
            self.bot.send_message(message.from_user.id, EARN + str(self.db.abs_sum_of_values(query)))

        @self.bot.message_handler(commands=['day'])
        def day_report(message):
            day_payments = self.db.select_payments_from_days(message.from_user.id)
            if not day_payments:
                self.bot.send_message(message.from_user.id, NOPAY)
                return
            for record in day_payments:
                self.bot.send_message(message.from_user.id, record.return_message())

        @self.bot.message_handler(commands=['week'])
        def day_report(message):
            for record in self.db.select_payments_from_days(message.from_user.id, 7):
                self.bot.send_message(message.from_user.id, record.return_message())

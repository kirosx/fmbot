from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, REMOTE_DATABASE
from .dbclass import User, PaymentRecord
from tabulate import tabulate
from datetime import timedelta, datetime


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Database(metaclass=Singleton):
    def __init__(self, database_url=DATABASE_URL):
        self.engine = create_engine(database_url)
        self.session = sessionmaker(self.engine)()
        self.users = self.session.query(User)
        self.payments = self.session.query(PaymentRecord)

    @staticmethod
    def abs_sum_of_values(query):
        return sum([i.value for i in query])

    def find_user_by_tgid(self, tgid: int):
        return self.users.filter(User.tgid == tgid).first()

    def show_records_by_tgid(self, tgid: int):
        return self.payments.filter(PaymentRecord.user_tgid == tgid)

    def show_plus_from_user(self, tgid: int):
        return self.payments.filter(PaymentRecord.user_tgid == tgid, PaymentRecord.payment_type == '+')

    def show_minus_from_user(self, tgid: int):
        return self.payments.filter(PaymentRecord.user_tgid == tgid, PaymentRecord.payment_type == '-')

    def show_recs_tabulate_by_user(self, tgid: int):
        return tabulate([[i.time, i.value, i.target, i.payment_type] for i in self.show_records_by_tgid(tgid)],
                        headers=[' ',  '$$$', 'ЦЕЛЬ', 'ТИП'],
                        tablefmt='orgtbl')

    def select_payments_from_days(self, tgid: int, days: int = 1):
        return [row for row in self.payments.all() if row.time >= datetime.today() - timedelta(days=days)
                and row.user_tgid == tgid]

    def total_result_for_user(self, tgid: int):
        return (self.abs_sum_of_values(self.show_plus_from_user(tgid))
                - self.abs_sum_of_values(self.show_minus_from_user(tgid)))

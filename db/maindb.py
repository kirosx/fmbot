from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, REMOTE_DATABASE
from .dbclass import User, PaymentRecord, DebtRecord, UserCategory, KeyWordCategory
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
        self.debt = self.session.query(DebtRecord)
        self.categories = self.session.query(UserCategory)
        self.keywords = self.session.query(KeyWordCategory)

    @staticmethod
    def abs_sum_of_values(query):
        return sum([i.value for i in query])

    @staticmethod
    def total_sum(queryset):
        return sum([x.value for x in queryset if x.payment_type == '+'])\
               - sum([y.value for y in queryset if y.payment_type == '-'])

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

    def full_debt_for_person(self, owner_tgid: int, person):
        full_debt = sum([i.value for i in self.debt.filter(DebtRecord.user_tgid == owner_tgid,
                                                           DebtRecord.person == person,
                                                           DebtRecord.debt_type == '-+')]) - \
                    sum([i.value for i in self.debt.filter(DebtRecord.user_tgid == owner_tgid,
                                                           DebtRecord.person == person,
                                                           DebtRecord.debt_type == '+-')])
        return full_debt

    def not_null_debtors(self, tgid: int):
        debtors = {i.person for i in self.debt.filter(DebtRecord.user_tgid == tgid)
                   if self.full_debt_for_person(tgid, i.person) != 0}
        return {i: self.full_debt_for_person(tgid, i) for i in debtors}

    def all_debs_for_person(self, tgid, person):
        return [i for i in self.debt.filter(DebtRecord.user_tgid == tgid, DebtRecord.person == person)]

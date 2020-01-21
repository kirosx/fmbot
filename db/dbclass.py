from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    tgid = Column(Integer, unique=True)
    tg_username = Column(String(30))

    def welcome_message(self):
        return f'Welcome to FamilyBot you are registered as {self.name}'

    def __init__(self, name, tgid, tg_username=None):
        self.name = name
        self.tgid = tgid
        self.tg_username = tg_username

    def __repr__(self):
        return f'<User - {self.name} {self.tgid}>'


class PaymentRecord(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_tgid = Column(Integer, ForeignKey('users.tgid'))
    payment_type = Column(String(3))
    value = Column(Float)
    target = Column(String(50))
    time = Column(DateTime, default=datetime.utcnow)

    def return_message(self):
        message = f'{self.time}  {self.payment_type} {self.value} {self.target}'
        return message

    def __init__(self, user_tgid, payment_type, value, target):
        self.user_tgid = user_tgid
        self.payment_type = payment_type
        self.value = float(value)
        self.target = target

    # def __repr__(self):
    #     return f'{self.user_tgid} {self.payment_type} {self.target} {self.value}\n{self.time}'


class DebtRecord(Base):
    __tablename__ = 'debt'
    id = Column(Integer, primary_key=True)
    user_tgid = Column(Integer, ForeignKey('users.tgid'))
    debt_type = Column(String(3))
    value = Column(Float)
    person = Column(String(50))
    time = Column(DateTime, default=datetime.utcnow)

    def __init__(self, tgid, typ, value, person):
        self.user_tgid = tgid
        self.debt_type = typ
        self.value = float(value)
        self.person = person.title()

    def return_message(self):
        point = 'Занял(а)' if self.debt_type == '-+' else 'Вернул(а)'
        return f'{self.time} {self.person} {point} {self.value}'

    def __repr__(self):
        return self.return_message()


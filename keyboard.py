from db.maindb import Database
from db.dbclass import PaymentRecord
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import REPORT_BUTTONS, PROFILE_BUTTONS, DEBTS, ADDCAT, KEYWRDS, DELCAT, CANCEL


class Keyboard:
    def __init__(self):
        self.markup = None
        self.db = Database()

    def delete_record_button(self, record: PaymentRecord):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(InlineKeyboardButton('Удалить', callback_data=f'del {record.user_tgid} {record.id}'))
        return self.markup

    def main_menu(self):
        self.markup = ReplyKeyboardMarkup(True, row_width=3)
        self.markup.row(*REPORT_BUTTONS)
        self.markup.row(DEBTS)
        self.markup.row(*PROFILE_BUTTONS)
        return self.markup

    def all_debts(self, user, person):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(InlineKeyboardButton('Все записи', callback_data=f'deb {user} {person}'))
        return self.markup

    def chart_menu(self, user, days, menu_chart: dict):
        self.markup = InlineKeyboardMarkup(row_width=1)
        for k, v in menu_chart.items():
            self.markup.add(InlineKeyboardButton(k, callback_data=f'chart {v} {user} {days}'))
        return self.markup

    def add_category(self, user):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(InlineKeyboardButton(ADDCAT, callback_data=f'addcategory {user}'))
        return self.markup

    def watch_or_delete_category(self, user, category):
        self.markup = InlineKeyboardMarkup(row_width=2)
        watch = InlineKeyboardButton(KEYWRDS, callback_data=f'keywords {user} {category}')
        delete = InlineKeyboardButton(DELCAT, callback_data=f'delcategory {user} {category}')
        self.markup.add(watch, delete)
        return self.markup

    def cancel_button(self):
        self.markup = ReplyKeyboardMarkup()
        self.markup.row(CANCEL)
        return self.markup

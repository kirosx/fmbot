from db.maindb import Database
from db.dbclass import PaymentRecord
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import REPORT_BUTTONS


class Keyboard:
    def __init__(self):
        self.markup = None
        self.db = Database()

    def delete_record_button(self, record: PaymentRecord):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(InlineKeyboardButton('Delete', callback_data=f'del {record.id} {record.user_tgid}'))
        return self.markup

    def main_menu(self):
        self.markup = ReplyKeyboardMarkup(True, row_width=3)
        self.markup.row(*REPORT_BUTTONS)
        self.markup.row('Долги')
        return self.markup

    def all_debts(self, user, person):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(InlineKeyboardButton('All Debts', callback_data=f'deb {person} {user}'))
        return self.markup

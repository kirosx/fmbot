from telebot import TeleBot
from config import TOKEN
from main_handler import HandlerBuilder


class Bot:
    def __init__(self, token: str):
        self.bot = TeleBot(token)
        self.handler = HandlerBuilder(self.bot)

    def run_bot(self):
        self.handler.run_handlers()
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    family_bot = Bot(TOKEN)
    family_bot.run_bot()

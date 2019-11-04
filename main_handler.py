from telebot import TeleBot
from handlers import HandlerRecord, HandlerCommands


class HandlerBuilder:
    def __init__(self, bot: TeleBot):
        self.handler_record = HandlerRecord(bot)
        self.handler_commands = HandlerCommands(bot)

    def run_handlers(self):
        for handler in self.__dict__.values():
            handler.run_handlers()

from handlers import HandlerRecord, HandlerCommands, HandlerCallback, HandlerReport, HandlerDebt, HandlerProfile, HandlerCategories


class HandlerBuilder:
    def __init__(self, bot):
        self.handler_record = HandlerRecord(bot)
        self.handler_commands = HandlerCommands(bot)
        self.handler_callback = HandlerCallback(bot)
        self.handler_report = HandlerReport(bot)
        self.handler_debt = HandlerDebt(bot)
        self.handler_profile = HandlerProfile(bot)
        self.handler_categories = HandlerCategories(bot)

    def run_handlers(self):
        for handler in self.__dict__.values():
            handler.run_handlers()

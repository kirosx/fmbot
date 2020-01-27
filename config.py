TOKEN = '***TOKEN***'
ALLOWED_USERS = []
DBNAME = 'fmbot'
DATABASE_URL = f'mysql://@localhost/{DBNAME}?charset=utf8'
PAY_TYPES = ['+', '-']
DEBT_TYPES = ['+-', '-+']
REMOTE_DATABASE = ''
SPENT = 'Итого потрачено:\n'
EARN = 'Итого заработано:\n'
TOTAL = 'Итого в кассе:\n'
NOPAY = 'Нет расходов'
REPORT_BUTTONS = ['Выписка за день', "Выписка за неделю", "Выписка за месяц"]
PROFILE_BUTTONS = ['Профиль', 'about']
MAIL = 'ehalgreka@protonmail.com'
CALLBACKCOMMANDS = ['del', 'deb']
UNRCG = 'Неизвестный запрос!\nДля регистрации в боте введите /start\nПомощь /help'
WELCOME = 'Вас приветствует BudgetBot, вы зарегестрированны как'
CHARTSSTRING = ['all', 'plus', 'minus']
REC = 'Записано\n'
NOTFOUND = 'Запись не найдена!'
DELETED = 'Удалено!'
DEBTS = 'Долги'
NODEBTS = 'Нет долгов'
REPORTDICT = {
        'Выписка за день': 1,
        'Выписка за неделю': 7,
        'Выписка за месяц': 30
    }
ALL = 'Все записи'
PROFIT = 'Доходы'
EXPENSES = 'Расходы'
REGTIME = 'Дата регистрации:'
HELPMESSAGE = 'Здравствуйте вас приветствует <strong>BudgetBot</strong>\n' \
              'Бот принимает комманды вида:\n <code>+ сумма цель</code>\n' \
              'либо: \n<code>- сумма цель</code>\n' \
              'Где <code>+</code> и <code>-</code> это получение дохода или трата соответственно\n' \
              'Например:\n<code>- 500 бензин</code> означает что вы потратили 500 рублей на бензин\n' \
              'Так же бот делает долговые записи, вида:\n<code>-+ сумма цель</code>\n' \
              'Например запись вида:\n<code>-+ 100 коллега1</code>  означает что вы одолжили 100 рублей коллеге\n' \
              'а запись:\n<code>+- 50 коллега1</code> что коллега вернул 50'

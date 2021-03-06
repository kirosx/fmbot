from config import ALLOWED_USERS, CALLBACKCOMMANDS, CHARTSSTRING


def float_checker(float_from_user_str: str):
    try:
        float(float_from_user_str)
    except ValueError:
        return False
    return True


def command_checker(user_string: str, types: list):
    spl = user_string.split()
    return True if len(spl) == 3 and spl[0] in types and float_checker(spl[1]) else False


def allow_user(message_from_id: int):
    return True if message_from_id in ALLOWED_USERS else False


def callback_delete_payment_checker(callback_string: str, caller_id: int):
    if len(callback_string.split()) == 3 and callback_string.split()[0] in ('del', 'deb'):
        command, user, obj = callback_string.split()
        return True if caller_id == int(user) and command in CALLBACKCOMMANDS else False


def chart_callback_checker(callback_string: str, caller_id: int):
    callback = callback_string.split()
    return True if len(callback) == 4 and callback[0] == 'chart' and callback[1] in CHARTSSTRING \
                   and int(callback[2]) == caller_id else False


def debt_message(debt: float, person: str):
    if debt > 0:
        message = f'{person} owe you {debt}'
    elif debt < 0:
        message = f'You owe {person} {debt}'
    else:
        message = f'{person} nothing owe to you!'
    return message


def category_command_checker(callback_string):
    command = callback_string.split()[0]
    return True if command == 'addcategory' else False


def keyword_callback_checker(callback_string):
    return True if callback_string.split()[0] == 'keywords' else False


def add_keyword_checker(callback_string):
    return True if callback_string.split()[0] == 'addkeyword' else False


def category_delete_checker(callback_string):
    return True if callback_string.split()[0] == 'delcategory' else False


def create_database_model():
    '''
    Перед созданием таблиц необходимо создать бд с именем DBNAME из config.py
    '''
    from db.maindb import Database
    from db.dbclass import Base
    db = Database()
    Base.metadata.create_all(db.engine)
    return 'database created'

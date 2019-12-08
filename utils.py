from config import ALLOWED_USERS, CALLBACKCOMMANDS


def float_checker(float_from_user_str: str):
    try:
        float(float_from_user_str)
    except ValueError:
        return False
    return True


def command_checker(user_string: str, types: list):
    spl = user_string.split()
    return True if len(spl) > 2 and spl[0] in types and float_checker(spl[1]) else False


def allow_user(message_from_id: int):
    return True if message_from_id in ALLOWED_USERS else False


def callback_delete_payment_checker(callback_string: str, caller_id: int):
    command, obj, user = callback_string.split()
    return True if caller_id == int(user) and command in CALLBACKCOMMANDS else False


def debt_message(debt: float, person: str):
    if debt > 0:
        message = f'{person} owe you {debt}'
    elif debt < 0:
        message = f'You owe {person} {debt}'
    else:
        message = f'{person} nothing owe to you!'
    return message

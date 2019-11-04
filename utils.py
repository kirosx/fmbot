from config import PAY_TYPES, ALLOWED_USERS


def float_checker(float_from_user_str: str):
    try:
        float(float_from_user_str)
    except Exception:
        return False
    return True


def command_checker(user_string: str):
    spl = user_string.split()
    return True if len(spl) > 2 and spl[0] in PAY_TYPES and float_checker(spl[1]) else False


def allow_user(message_from_id: int):
    return True if message_from_id in ALLOWED_USERS else False




import datetime


def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


def get_param(param, in_name, default):
    if in_name in param and param[in_name]:
        return param[in_name]
    else:
        return default

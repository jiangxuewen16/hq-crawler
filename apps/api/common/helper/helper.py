import datetime
import time


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


def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def getDayList():
    start = str(datetime.date(datetime.date.today().year, datetime.date.today().month, 1))
    end = time.strftime("%Y-%m-%d", time.localtime())
    result = []
    for date in dateRange(start, end):
        result.append({'_id': date[-2:], 'avg_score': 5})
    return result

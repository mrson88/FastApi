import datetime
import time


def before_x_day(day):
    date_today = datetime.date.today()
    no_of_days = datetime.timedelta(days=day)
    return (date_today - no_of_days).strftime("%d-%m-%Y")


def time_hour():
    return time.strftime('%H')


def time_minute():
    return time.strftime('%M')


def time_today():
    return time.strftime('%H:%M')


def time_today_second():
    return time.strftime('%H:%M:%S')


def date_today_strf():
    date_today = datetime.date.today()
    return date_today.strftime("%d-%m-%Y")

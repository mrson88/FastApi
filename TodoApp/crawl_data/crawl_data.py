import requests
from bs4 import BeautifulSoup
import time
import datetime
import random
import secrets


def crawl_data():
    response = requests.get("https://xosoketqua.com/xsmb-xo-so-mien-bac.html")
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find('div', class_='block-main-content')
    body_1 = soup.find('div', class_='list-link')
    result_day = str(check_body(body_1.findChildren("a", class_="u-line"))[2]).split(' ')[1]
    print(result_day)
    result_raw = check_body(body.findChildren("span", class_="div-horizontal"))
    result_final = result_raw[-27:]
    # print(f'result_final= {result_final}')
    return [result_day, result_final]


def check_body(b):
    return [b[i].text for i in range(len(b))]


def create_data_five_minute():
    data = create_data_list_five_minute()
    date_today = datetime.date.today()
    # no_of_days = datetime.timedelta(days=1)
    # before_one_days = (date_today - no_of_days).strftime("%d/%m/%Y")
    date_today_strftime = date_today.strftime("%d-%m-%Y")
    # print(date_today_strftime)
    time_today_strtime = time.strftime('%H:%M')
    return [date_today_strftime, time_today_strtime, data]


def create_data_list_five_minute():
    five_minute_data = []
    for i in range(27):
        data = secrets.randbelow(100000)
        if i >= 0:
            five_minute_data.append(data)
        elif i > 10:
            five_minute_data.append(data[1:])
        elif i > 18:
            five_minute_data.append(data[2:])
        else:
            five_minute_data.append(data[3:])
    print(five_minute_data)
    return five_minute_data

import requests
from bs4 import BeautifulSoup


def crawl_data():
    response = requests.get("https://xosoketqua.com/xsmb-xo-so-mien-bac.html")
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find('div', class_='block-main-content')
    body_1 = soup.find('div', class_='list-link')
    result_day = str(check_body(body_1.findChildren("a", class_="u-line"))[2]).split(' ')[1]
    print(result_day)
    result_raw = check_body(body.findChildren("span", class_="div-horizontal"))
    result_final = result_raw[-27:]
    print(f'result_final= {result_final}')
    return [result_day, result_final]


def check_body(b):
    return [b[i].text for i in range(len(b))]

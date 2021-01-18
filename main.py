import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

HOST = 'http://lawyers.minjust.ru/'
HEADERS = {
    'User-Agent': 'Googlebot',
    'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    if r.ok:
        return r.text
    print(r.status_code)


def write_card_csv(data):
    with open('lawyers_cards.csv', 'a') as file:
        order = ['name',
                 'status',
                 'registerNumber',
                 'identityCard',
                 'lawyersPalat',
                 'actionForm',
                 'actionTitle',
                 'adress',
                 'phone',
                 'email',
                 'changeName',
                 'orderSubject'
                 ]
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def write_links_csv(data):
    with open('links.csv', 'a') as file:
        order = ['link']
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def get_lawyers_links(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='persons').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        try:
            link = HOST + tds[1].find('a').get('href')
        except AttributeError:
            link = ''
        data = {'link': link}
        write_links_csv(data)


def get_pagination(html):
    soup = BeautifulSoup(html, 'lxml')
    count_page = soup.find('ul', class_='pagination').find_all('li')[-1].find('a').get('href')
    count_page = count_page.split('=')
    return int(count_page[-1])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', id='forms').find_all('div')

    name = divs[0].find('span').text  # Имя
    status = divs[0].find_all('span')[-1].text  # Статус
    register_number = divs[2].find_all('p')[-1].text  # Реестровый номер
    identity_card = divs[3].find_all('p')[-1].text  # № Удостоверения
    lawyers_palat = divs[4].find_all('p')[-1].text  # Адвокатская палата
    action_form = divs[5].find_all('p')[-1].text  # Организационная форма
    action_title = divs[6].find_all('p')[-1].text  # Название
    adress = divs[7].find_all('p')[-1].text  # Адрес
    phone = divs[8].find_all('p')[-1].text  # Телефон
    email = divs[9].find_all('p')[-1].text  # Email
    change_name = divs[10].find_all('p')[-1].text  # ФИО до изменения
    order_subject = divs[12].find_all('p')[-1].text  # Приказ территориального органа

    data = {'name': name,
            'status': status,
            'registerNumber': register_number,
            'identityCard': identity_card,
            'lawyersPalat': lawyers_palat,
            'actionForm': action_form,
            'actionTitle': action_title,
            'adress': adress,
            'phone': phone,
            'email': email,
            'changeName': change_name,
            'orderSubject': order_subject
            }
    write_card_csv(data)


def make_all_links(url):
    text = get_html(url)
    get_lawyers_links(text)


def make_lawyers_data(url):
    text = get_html(url)
    get_page_data(text)


def main():

    url = 'http://lawyers.minjust.ru/Lawyers?page={}'
    urls = [url.format(str(i)) for i in range(0, get_pagination(get_html('http://lawyers.minjust.ru/Lawyers')))]

    # Мультипроцессинг
    with Pool(30) as p:
        p.map(make_all_links, urls)


if __name__ == '__main__':
    main()

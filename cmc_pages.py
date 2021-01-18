import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

HOST = 'http://lawyers.minjust.ru/'


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['registerNumber'],
                         data['link'],
                         data['name'],
                         data['subject'],
                         data['identityCard'],
                         data['status']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', class_='persons').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        try:
            registerNumber = tds[0].text.strip()
        except:
            registerNumber = ''
        try:
            link = HOST + tds[1].find('a').get('href')
        except:
            link = ''
        try:
            name = tds[1].find('a').text.strip()
        except:
            name = ''
        try:
            subject = tds[2].text.strip()
        except:
            subject = ''
        try:
            identityCard = tds[3].text.strip()
        except:
            identityCard = ''
        try:
            status = tds[4].text.strip()
        except:
            status = ''

        data = {'registerNumber': registerNumber,
                'link': link,
                'name': name,
                'subject': subject,
                'identityCard': identityCard,
                'status': status
                }

        write_csv(data)


def make_all(url):
    text = get_html(url)
    get_page_data(text)


def main():
    # 6825
    # url = 'http://lawyers.minjust.ru/Lawyers?page=0'
    #
    # while True:
    #     get_page_data(get_html(url))
    #
    #     soup = BeautifulSoup(get_html(url), 'lxml')
    #
    #     try:
    #         url = 'http://lawyers.minjust.ru' + soup.find('ul', class_='pagination').find_all('li', class_='page-item')[-2].find('a', class_='page-link').get('href')
    #         print(url)
    #     except:
    #         print('Парсинг окончен...')
    #         break

    # ===========================================================
    # Мультипроцессинг
    # url = 'http://lawyers.minjust.ru/Lawyers?page={}'
    # urls = [url.format(str(i)) for i in range(0, 6826)]
    # with Pool(20) as p:
    #     p.map(make_all, urls)

    url = 'http://lawyers.minjust.ru/Lawyers?page=0'
    soup = BeautifulSoup(get_html(url), 'lxml')
    try:
        page_count = int(soup.find('ul', class_='pagination').find('a', {'aria-label': 'Последняя'}).get('href').split('=')[-1])
    except:
        page_count = 1


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import csv


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 'accept':'*/*'}
HOST = 'https://www.avito.ru'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1
    return pagination

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-root-G3n7v')
    
    cars = []
    for item in items:
        cars.append({
            'title': item.find('h3', class_='title-root-395AQ').get_text(),
            'link': HOST + item.find('a', class_='link-link-39EVK').get('href'),
            'price': item.find('span', class_='price-text-1HrJ_').get_text(),
            'location': item.find('div', class_='geo-georeferences-3or5Q').find_next('span').get_text(),

        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['location']])

def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pagination = get_pages_count(html.text)
        for page in range(1, pagination + 1):
            print(f'Парсинг страницы {page} из {pagination}...')
            html = get_html(URL, params={'p': page})
            cars.extend(get_content(html.text))
        print(f'Получено {len(cars)} автомобилей')
        save_file(cars, FILE)
    else:
        print('Error')    
parse()
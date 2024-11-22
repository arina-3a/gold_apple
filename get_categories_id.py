import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import logging
import time
import random
from datetime import datetime

from record_categories_id_to_db import insert_data_into_brands_table
from category_check import set_difference, list_of_missing_items


def get_brands_page(url: str) -> BeautifulSoup | None:
    """
    Получает HTML-страницу и возвращает объект BeautifulSoup для анализа.

    :param url: URL-адрес страницы
    :return: Объект BeautifulSoup или None если произошла ошибка
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Поднимает HTTPError для плохих http-ответов (4xx и 5xx)
    except requests.exceptions.RequestException as e:
        logging.error("Ошибка при запросе URL: %s", e)
        return None
    return BeautifulSoup(response.text, 'html.parser')


def parse_links(bs: BeautifulSoup) -> list[str]:
    links = []
    li_blocks = bs.find_all('li', class_='PuxFQ')
    for li in li_blocks:
        link = li.find('a').attrs['href']
        links.append(link)
    return links

def get_categories_id(url: str) -> BeautifulSoup | None:
    headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error("HTTP error occurred: %s", http_err)
        return None
    except requests.exceptions.RequestException as req_err:
        logging.error("Request error occurred: %s", req_err)
        return None

    return BeautifulSoup(response.text, 'html.parser')

def parse_categories_id(links: list[str])-> list[tuple[str, str]]:
    # на входе массив строк: '/brands/love', и тд
    # на выходе список кортежей: ('2423432', 'love')
    categories_id = []
    for link in links:
        time.sleep(round(random.uniform(2, 5), 1))
        print('запуск парсинга для ', link)
        bs = get_categories_id('https://goldapple.ru' + link)
        if bs is not None:
            script_position = bs.find('script', attrs={'data-n-head': '1', 'data-hid': 'gtm-script'}).find_next('script')
            if script_position is not None:
                category_id = re.search(r'"entityId":"(\d+)"', script_position.text).group(1)
                categories_id.append((category_id, link.replace('/brands/', '')))
    return categories_id


def record_categories_into_db(links: list[str]) -> None:
    start, intermediate_values, end = 0, 0, len(links)
    while start <= end:
        intermediate_values = start + 50
        for i in range(start, intermediate_values, 5):
            print(f'выполняется запрос для бренда {links[i]}')
            print(f'Выполняется batch: {i/5+1} /{len(links)/5}')
            categories_id = parse_categories_id(links=links[i:i+5])
            pprint(categories_id)
            insert_data_into_brands_table(categories_id=categories_id)
        start +=50
        delay = round(random.uniform(100, 360), 1)
        print(f'Сейчас будет произведена задержка на {delay} секунд между крупными частями парсинга.')
        print(f'Время начала задержки: {datetime.now().strftime("%H:%M:%S")}.')
        time.sleep(delay)

# def record_categories_into_db(links: list[str]) -> None:
#     start = 0
#     end = len(links)
#     batch_size = 50
#     step_size = 5
#
#     while start < end:
#         intermediate_values = min(start + batch_size, end)
#         for i in range(start, intermediate_values, step_size):
#             if i < end:  # Проверка на допустимый индекс
#                 sub_links = links[i:i + step_size]
#                 print(f'выполняется запрос для брендов: {sub_links}')
#                 print(f'Выполняется batch: {i // step_size + 1} / {end // step_size}')
#                 categories_id = parse_categories_id(links=sub_links)
#                 pprint(categories_id)
#                 insert_data_into_brands_table(categories_id=categories_id)
#
#         start += batch_size
#         delay = round(random.uniform(100, 360), 1)
#         print(f'Сейчас будет произведена задержка на {delay} секунд между крупными частями парсинга.')
#         print(f'Время начала задержки: {datetime.now().strftime("%H:%M:%S")}.')
#         time.sleep(delay)



def main():
    bs = get_brands_page('https://goldapple.ru/brands')  # парсинг h tml страницы с брендами
    pprint(bs)
    links = parse_links(bs=bs)  # получение ссылок на бренды
    set = set_difference(links=links)
    print(set)
    links_of_missing_items = list_of_missing_items(set=set)
    record_categories_into_db(links=links_of_missing_items)





if __name__ == '__main__':
    main()

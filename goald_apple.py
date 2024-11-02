from bs4 import BeautifulSoup
from typing import Any
import requests
import re
import json
from  pprint import pprint
import psycopg2
from datetime import datetime

# Запрос на получение данных json по 1 интересующей страницы бренда
def inserting_values_into_the_database(data_from_all_pages: list[list[list[Any | None]]], categoryId : int):
    conn = database_connection()
    cursor = conn.cursor()
    for page in range(0, len(data_from_all_pages)):
        for product in range(0, len(data_from_all_pages[page])):
            product_name = data_from_all_pages[page][product][1]
            productType = data_from_all_pages[page][product][2]
            itemId = data_from_all_pages[page][product][3]
            currentUnitValue = data_from_all_pages[page][product][4]
            unitName = data_from_all_pages[page][product][5]
            price_current = data_from_all_pages[page][product][6]
            price_regular = data_from_all_pages[page][product][7]
            discount_percent = data_from_all_pages[page][product][8]
            cursor.execute("SELECT productid_goldapple FROM products WHERE productid_goldapple = %s", (itemId,))
            result = cursor.fetchone()
            if result:
                print('Запись не добавилась, так как она уже есть в бд')
            else:
                cursor.execute("INSERT INTO products (brandid ,productid_goldapple, productname, producttype, currentunitvalue, unitname) "
                           "VALUES (%s, %s, %s, %s, %s, %s)", ( '9', data_from_all_pages[page][product][3], product_name, productType, currentUnitValue, unitName))
            #вставка данных по ценам работает
            # currentTime = datetime.now()
            # cursor.execute("SELECT productid FROM products WHERE productid_goldapple = %s", (itemId,))
            # result = cursor.fetchone()
            # cursor.execute("INSERT INTO prices (productid, date, price_current, price_regular, discount_percent) " "VALUES (%s, %s, %s, %s, %s)",
            #                (result[0], currentTime, price_current, price_regular, discount_percent))
    conn.commit()
    cursor.close()  # закрываем курсор
    conn.close()  # закрываем соединение


def request_for_receipt_of_goods_by_brand(url_, categoryId, page):
    # URL для запроса
    #url = 'https://goldapple.ru/front/api/catalog/products' # https://goldapple.ru/brands/catrice  ?p=1
    url = url_
    # Параметры запроса
    params = {
        'categoryId': categoryId,
        'cityId': '9ae64229-9f7b-4149-b27a-d1f6ec74b5ce',
        'pageNumber': str(page),
        'z': '14-46'
    }

    # Заголовки запроса
    headers = {
        'sec-ch-ua-platform': '"Linux"',
        'Referer': '',
        'x-gast': '37068833.637526624,37068833.637526624',
        'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'traceparent': '00-e03db3c5320b40913569f8c588ecf10a-e5c3a03f41eef85e-01',
        'x-app-version': '1.60.0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*'
    }
    # Выполнение GET-запроса
    response = requests.get(url, headers=headers, params=params)
    ga_response = response.json()
    return ga_response

def cleanup_response_page(response):
    products_info=[]
    for product in response['data']['products']:
        brand_name = product['brand']
        print(brand_name)
        product_name = product['name']
        print(product_name)
        productType = product['productType']
        print(productType)
        itemId = product['itemId']
        print(itemId)
        currentUnitValue = product['attributes']['units']['currentUnitValue'] #объем/количество товара в мл/шт и т д
        print(currentUnitValue)
        unitName = product['attributes']['units']['name'] # название единицы измерения товара
        print(unitName)
        price_current = product['price']['actual']['amount']
        print(price_current)
        price_regular = product['price']['regular']['amount']
        print(price_regular)
        if product['labels']: # обязательно необходима сначала проверка на то, что поле labels не пустое
            discount_percent = product['labels'][0].get('text')
        else:
            discount_percent = None
        print(discount_percent)
        product_info = [brand_name, product_name, productType, itemId, currentUnitValue, unitName, price_current, price_regular, discount_percent]
        print(product_info)
        products_info.append(product_info)
    return products_info

def receipt_of_goods_by_brand(url, categoryId):
    page = 1
    data_from_all_pages = []
    while True:
        response = request_for_receipt_of_goods_by_brand(url, categoryId, page)
        data_from_page = cleanup_response_page(response)
        data_from_all_pages.append(data_from_page)
        print('ЗАКОНЧИЛАСЬ СТРАНИЦА ', page)
        page = page + 1
        if not response['data']['products']:
            break
    return data_from_all_pages
#database connection

def database_connection():
    try:
    # Установите соединение с базой данных
           connection = psycopg2.connect(
               user="postgres",
               password="mysecretpassword",
               host="localhost",  # или другой адрес сервера
               port="5432",       # стандартный порт PostgreSQL
               database="postgres"
           )
           print("Успешно подключено")
           return connection
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к PostgreSQL", error)

def main():
    url = 'https://goldapple.ru/front/api/catalog/products'
    categoryId = '1000001141',  # catrice
    data_from_all_pages = receipt_of_goods_by_brand(url = url, categoryId = categoryId)
    inserting_values_into_the_database(data_from_all_pages = data_from_all_pages, categoryId = categoryId)
    #cleanup_response_page(request_for_receipt_of_goods_by_brand(url, categoryId, 1))
    #inserting_values_into_the_database()




    return 0

if __name__ == '__main__':
    main()

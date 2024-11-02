from itertools import product

from bs4 import BeautifulSoup
import requests
import re
import json
from  pprint import pprint

def product_name_input():
    product_trash = input("Введите наименование искомого продукта: ")
    product_name_for_url = product_trash.replace(" ", "%")
    return product_name_for_url
def url_creation(product_name_for_url):
    url = 'https://rivegauche.ru/search?text=' + product_name_for_url
    return url

#функция для очистки цены
def price_acquisition(price_trash):
    if price_trash:
        clean_price = re.sub(r'\D', '', price_trash.get_text())
    else:
        clean_price = None
    return clean_price

def trash_data_acquisition(bs):
    products_trash = []
    products_trash_soup = bs.find_all('product-item')
    for item in products_trash_soup:
        id_product_trash = item.get('offer-id')
        discount_trash = (item.find('div', tabindex='0'))
        if discount_trash is not None:
            discount_trash = discount_trash.get_text(strip=True)
        print('discount_trash:  ', discount_trash)
        names_trash = item.find("div", class_=re.compile(r'label')).get_text()
        prices_current_trash = price_acquisition(item.find(class_=re.compile(r'from-price')))
        price_full_trash = price_acquisition(item.find('s', class_='ng-star-inserted'))
        product_trash = [id_product_trash, names_trash, prices_current_trash, discount_trash, price_full_trash]
        products_trash.append(product_trash)
        # products_trash.append([id_product_trash, names_trash, prices_current_trash,discount_, price_full_trash]) #не удалять, потом раскоментить
        print(product_trash)

    print(len(products_trash))

#1076777
# curl 'https://api.rivegauche.ru/rg/v1/newRG/products/ac-search?fields=FULL&offset=0&size=48&st=catrice&tag=8935590043656660'   -H 'accept: application/json, text/plain, */*'   -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'   -H 'origin: https://rivegauche.ru'   -H 'priority: u=1, i'   -H 'referer: https://rivegauche.ru/'   -H 'sec-ch-ua: "Chromium";v="129", "Not=A?Brand";v="8"'   -H 'sec-ch-ua-mobile: ?0'   -H 'sec-ch-ua-platform: "Linux"'   -H 'sec-fetch-dest: empty'   -H 'sec-fetch-mode: cors'   -H 'sec-fetch-site: same-site'   -H 'time-zone: GMT+3'   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'   -H 'x-accept-image-webp: true'
#shiseido

def dick_suck():


    url = "https://goldapple.ru/front/api/home/slots"
    params = {
        "cityId": "9ae64229-9f7b-4149-b27a-d1f6ec74b5ce",
        "customerGroupId": "0",
        "z": "14-46"
    }

    headers = {
        "sec-ch-ua-platform": "\"Linux\"",
        "Referer": "",
        "x-gast": "37068833.637526624,37068833.637526624",
        "sec-ch-ua": "\"Chromium\";v=\"129\", \"Not=A?Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-e1682e56e83d70c34ad69e79538f2844-5444ca8ac6b5d672-01",
        "x-app-version": "1.60.0",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, headers=headers, params=params)

    pprint(response.status_code)
    #pprint(response.json())  # Используйте .json() только если в ответе ожидается JSON
    ga_data = response.json()
    brand = ga_data.get('brand')
    print(type(ga_data))
    # print(brand)
    # pprint(ga_data)
    pprint(response.json())
    print(len(ga_data.items()))
    for i in ga_data.keys():
        print(i)
        for j in ga_data[i]:
            print(j)
            for k in ga_data[i][j]:
                print(k)


def main():
    # product_name_for_url = product_name_input()
    # url = url_creation(product_name_for_url)
    # response = requests.get(url)
    # bs = BeautifulSoup(response.text,"html.parser")
    # trash_data_acquisition(bs)
    dick_suck()



    return 0

if __name__ == '__main__':
    main()

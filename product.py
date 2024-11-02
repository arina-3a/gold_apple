from dataclasses import dataclass
from itertools import product
from typing import Optional
from pprint import pprint

from scraper import request_product_page

@dataclass
class Product:
    brand_name: str
    product_name: str
    product_type: str
    item_id: int
    current_unit_value: float #объем/количество товара в мл/шт и т д
    unit_name: str # название единицы измерения товара
    price_current: float
    price_regular: float
    discount_percent_from_label: str | None
    discount_percent_from_coupon: str | None


def fetch_products_from_page(page_number: str) -> list[Product] | None:
    products_list = []
    response = request_product_page(page_number=page_number)
    #pprint(response)
    if response['data']['products']:
        for product in response['data']['products']:
            product_obj = Product(
                brand_name=product['brand'],
                product_name=product['name'],
                product_type=product['productType'],
                item_id=product['itemId'],
                current_unit_value=product['attributes']['units']['currentUnitValue'], #объем/количество товара в мл/шт и т д
                unit_name=product['attributes']['units']['name'], # название единицы измерения товара
                price_current=product['price']['actual']['amount'],
                price_regular=product['price']['regular']['amount'],
                discount_percent_from_label=product['labels'][0].get('text') if product['labels'] else None,
                discount_percent_from_coupon=product['couponResponse']['discountPercent'] if product['couponResponse'] else None,

            )
            products_list.append(product_obj)
        #pprint(products_list)
        return products_list
    else:
        return None


def fetch_products_by_brand() -> list[Product] | None:
    products_list = []
    page_number = '1'
    while True:
        products = fetch_products_from_page(page_number=page_number)
        if products is None:
            break
        products_list.extend(products)
        print('ЗАКОНЧИЛАСЬ СТР ', page_number)
        page_number = str(int(page_number)+1)
    return products_list

def main():
    products = fetch_products_by_brand()
    pprint(products)
    print(len(products))

    return 0

if __name__ == '__main__':
    main()





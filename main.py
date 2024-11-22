from database import insert_data_into_products_table, get_categories_id, insert_data_into_prices_table
from product import fetch_products_by_brand
from pprint import pprint
import logging


def main():
    categories_id, brands_id = get_categories_id()
    for index, category_id in enumerate(categories_id):
        logging.info(f'Отработка данных по category_id: {category_id}.')
        logging.info(f'В базе данных brand_id: {brands_id[index]}.')
        logging.info('Запуск сбора данных по продуктам.')
        products_list = fetch_products_by_brand(category_id=category_id)
        logging.info(f'Завершен сбор данных по продуктам. Было собрано {len(products_list)} продукта/ов.')
        logging.info('Запуск вставки данных в таблицу "products".')
        insert_data_into_products_table(products_list=products_list, brand_id=brands_id[index])
        logging.info('Запуск вставки данных в таблицу "prices".')
        insert_data_into_prices_table(products_list=products_list)

    return 0


if __name__ == '__main__':
    main()

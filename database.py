import psycopg2
from contextlib import closing
#from loguru import logger
from datetime import datetime
from product import Product
import logging

# damp in postgres in docker:
# docker exec -t gold_apple_2-postgres-1 pg_dump -U airflow gold_apple > /home/wifelly/projects/gold_apple_2/dumps/dump.sql

# ДЛЯ ДОКЕРА
# def database_connection():
#     try:
#         # Установка соединения с базой данных
#         connection = psycopg2.connect(
#             user="postgres",
#             password="arina",
#             host="postgres",  # или другой адрес сервера
#             port="5432",  # стандартный порт PostgreSQL
#             database="postgres"
#         )
#         print("Успешно подключено")
#         return connection
#     except (Exception, psycopg2.Error) as error:
#         print("Ошибка при подключении к PostgreSQL", error)

def database_connection():
    try:
        # Установка соединения с базой данных
        connection = psycopg2.connect(
            user="postgres",
            password="mysecretpassword",
            host="localhost",  # или другой адрес сервера
            port="5432",  # стандартный порт PostgreSQL
            database="postgres"
        )
        print("Успешно подключено")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к PostgreSQL", error)


def insert_data_into_products_table(products_list: list[Product], brand_id: str) -> None:
    # Определяем функцию, которая принимает список продуктов и идентификатор бренда.
    try:
        with closing(database_connection()) as connection, connection.cursor() as cursor:
            for product in products_list:
                cursor.execute(
                    "SELECT productid_goldapple FROM products WHERE productid_goldapple = %s",
                    (product.item_id,)
                )
                result = cursor.fetchone()  # Получаем результат запроса.

                if result is None:
                    # Если результат пустой, то записи нет, и мы вставляем новую.
                    cursor.execute(
                        "INSERT INTO products (brand_id, productid_goldapple, productname, producttype, currentunitvalue, unitname) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (brand_id, product.item_id, product.product_name, product.product_type,
                         product.current_unit_value, product.unit_name)
                    )
                    print(f"Добавлена новая запись: {product.item_id}")  # Логируем успешную вставку.
                else:
                    #logger.info(f"Пропуск вставки, запись уже существует: {product.item_id}")  # Логируем, что запись уже существует.
                    pass

            connection.commit()  # Подтверждаем транзакцию, сохраняем изменения в базе данных.
            print("Все изменения успешно зафиксированы в базе данных.")  # Логируем успешное завершение транзакции.
    except psycopg2.Error as error:
        # Обрабатываем ошибки, специфичные для psycopg2, и логируем их.
        print(f"Ошибка при вставке данных в таблицу products: {error}")


def insert_data_into_prices_table(products_list: list[Product]|None) -> None:
    try:
        with closing(database_connection()) as connection, connection.cursor() as cursor:
            for product in products_list:
                cursor.execute("SELECT productid FROM products WHERE productid_goldapple = %s", (product.item_id,) )
                result = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO prices ("
                    "productid,"
                    "date,"
                    "price_current,"
                    "price_regular,"
                    "discount_percent_from_label,"
                    "discount_percent_from_coupon)" 
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (result,
                     datetime.now(),
                     product.price_current,
                     product.price_regular,
                     product.discount_percent_from_label,
                     product.discount_percent_from_coupon))
            connection.commit()  # Подтверждаем транзакцию, сохраняем изменения в базе данных.
            print("Вставка данных произошла успешно")

    except psycopg2.Error as error:
        print(f"Ошибка при вставке данных в таблицу prices: {error}")
    pass

def get_categories_id() -> tuple[list[str], list[str]] | list:
    try:
        connection = database_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT category_id  FROM brands")
            categories_id = [category_id[0] for category_id in cursor.fetchall()]
            cursor.execute("SELECT brand_id FROM brands")
            brands_id = [brand_id[0] for brand_id in cursor.fetchall()]
        return categories_id, brands_id
    except psycopg2.Error as error:  # Обрабатываем ошибки, специфичные для psycopg2
        print("Ошибка произошла в методе get_categories_id() ")
        print(f"An error occurred: {error}")
        return []

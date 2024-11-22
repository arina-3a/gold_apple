import psycopg2
from contextlib import closing
#from loguru import logger

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

def insert_data_into_brands_table(categories_id: list[tuple[str, str]]):
    try:
        with closing(database_connection()) as connection, connection.cursor() as cursor:
            for category_id in categories_id:
                cursor.execute("SELECT category_id FROM brands WHERE category_id = %s", (category_id[0],))
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO brands(category_id, brand_name) VALUES (%s, %s) ON CONFLICT (brand_id) DO NOTHING", category_id)
                else:
                    pass
            connection.commit()  # Подтверждаем транзакцию, сохраняем изменения в базе данных.
            print("Вставка данных произошла успешно")

    except psycopg2.Error as error:
        print(f"Ошибка при вставке данных в таблицу prices: {error}")
    pass
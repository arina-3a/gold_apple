from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from database import insert_data_into_products_table, get_categories_id, insert_data_into_prices_table
from product import fetch_products_by_brand
import logging
import time
import random

# Ваша основная функция, которую мы будем выполнять через Airflow
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

    #logging.info(categories_id)

# Аргументы по умолчанию для DAG
default_args = {
    'owner': 'yourname',  # Здесь вы можете подставить ваше имя или любого другого владельца
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Определение самого DAG
dag = DAG(
    'daily_product_update',  # Имя вашего DAG
    default_args=default_args,
    description='A daily task to update product data',
    schedule_interval='0 6 * * *',  # Расписание: 06:00 UTC, что соответствует 09:00 по Москве
    start_date=datetime(2023, 11, 6),  # Дата начала - укажите текущую дату или другую дату начала
    catchup=False,  # Указывает, что airfllow не будет запускать DAG-задачи за пропущенные интервалы
)

# Определение задачи, использующей PythonOperator
run_daily_product_update = PythonOperator(
    task_id='run_daily_product_update',
    python_callable=main,  # Функция, которая будет выполняться
    dag=dag,
)

import psycopg2
from pprint import pprint
from contextlib import closing
from typing import Set

from record_categories_id_to_db import database_connection

def get_set_category_id_ga(links: list[str])-> Set[str]:
    categories_id_in_ga = set()
    for link in links:
        categories_id_in_ga.add(link.replace('/brands/', ''))
    return categories_id_in_ga

def get_set_category_id_db() -> Set[str]:
    try:
        with closing(database_connection()) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT brand_name FROM brands")
            rows = cursor.fetchall()
            categories_id_in_db = {rows[0] for rows in rows}
            return categories_id_in_db
    except psycopg2.Error as error:
        print(f"Ошибка получении данных из бд для работыы с множеством: {error}")
    pass

def set_difference(links: list[str]) -> Set[str]:
    categories_id_in_ga = get_set_category_id_ga(links=links)
    categories_id_in_db = get_set_category_id_db()
    sets_difference = categories_id_in_ga - categories_id_in_db
    return sets_difference

def list_of_missing_items(set: Set[str]):
    list_missing_items = [ f'/brands/{item}' for item in set]
    return list_missing_items
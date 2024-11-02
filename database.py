import psycopg2

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
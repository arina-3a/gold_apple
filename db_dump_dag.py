from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


# Аргументы по умолчанию для DAG
default_args = {
    'owner': 'arina',  # Здесь вы можете подставить ваше имя или любого другого владельца
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Определение самого DAG
dag = DAG(
    'db_dump_dag',  # Имя вашего DAG
    default_args=default_args,
    description='Daily database dump',
    schedule_interval='20 6 * * *',  # Запуск в 06:20
    start_date=datetime(2023, 11, 22),  # Дата начала - укажите актуальную дату
    catchup=False,  # Не выполнять DAG задания за пропущенные интервалы
)

# Определение задачи, использующей BashOperator
run_db_dump_dag = BashOperator(
    task_id='run_db_dump_dag',
    bash_command=(
        'docker exec -t gold_apple_2-postgres-1 pg_dump -U airflow gold_apple '
        '> /home/wifelly/projects/gold_apple_2/dumps/dump_{{ ds }}.sql'
    ),
    dag=dag,
)


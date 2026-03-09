from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'house_prices_conversion',
    default_args=default_args,
    description='A simple DAG to convert JSON to CSV',
    schedule_interval=None,
    catchup=False,
)

convert_task = BashOperator(
    task_id='convert_json_to_csv',
    bash_command='python /opt/airflow/convert_json_to_csv.py',
    dag=dag,
)
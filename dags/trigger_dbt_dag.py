from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}
with DAG(
    'trigger_dbt_dag',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False
) as dag:
        dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && dbt run'
    )

        dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && dbt test'
    )

        dbt_run >> dbt_test
    
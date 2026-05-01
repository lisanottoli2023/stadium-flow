from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime


def on_failure_callback(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
    print(f"DAG FAILED: {dag_id} | Task: {task_id} | Date: {execution_date}")


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'on_failure_callback': on_failure_callback
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

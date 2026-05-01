FROM apache/airflow:2.8.1
RUN pip install dbt-core dbt-postgres

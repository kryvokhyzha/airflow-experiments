from multiprocessing import parent_process
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import task, dag

from datetime import datetime, timedelta


@task.python
def extract():
    partner_name = 'netflix'
    partner_path = '/partners/netflix'
    # ti.xcom_push(key="partner_name", value=partner_name)
    return partner_name
    

@task.python
def process(partner_name):
    print(partner_name)


# Using a DAG context manager, you don't have to specify the dag property of each task
@dag(
    description='DAG in charge of processing customer data',
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'],
    max_active_tasks=1,
    catchup=False # enable if you don't want historical dag runs to run
    )
def my_dag_2():
    process(extract())
    

my_dag_2()

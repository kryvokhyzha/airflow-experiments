from multiprocessing import parent_process
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import task, dag

from datetime import datetime, timedelta
from typing import Dict


# @task.python(task_id="extract_partners")
@task.python(task_id="extract_partners", do_xcom_push=False, multiple_outputs=True)
def extract():# -> Dict[str, str]:
    partner_name = 'netflix'
    partner_path = '/partners/netflix'
    # ti.xcom_push(key="partner_name", value=partner_name)
    return {'partner_name': partner_name, 'partner_path': partner_path}
    

@task.python
def process(partner_name, partner_path):
    print(partner_name)
    print(partner_path)


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
def my_dag_3():
    partner_settings = extract()
    process(partner_settings['partner_name'], partner_settings['partner_path'])
    
    
dag = my_dag_3()

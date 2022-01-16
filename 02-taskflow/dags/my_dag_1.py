from multiprocessing import parent_process
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta


def _extract(ti):
    partner_name = 'netflix'
    partner_path = '/partners/netflix'
    # ti.xcom_push(key="partner_name", value=partner_name)
    return {'partner_name': partner_name, 'partner_path': partner_path}
    

def _process(ti):
    # partner_name = ti.xcom_pull(key="partner_name", task_ids="extract")
    partner_settings = ti.xcom_pull(task_ids="extract")
    print(partner_settings['partner_name'])


# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    dag_id='my_dag_1',
    description='DAG in charge of processing customer data',
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'],
    max_active_tasks=1,
    catchup=False # enable if you don't want historical dag runs to run
    ) as dag:
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=_extract,
    )
    
    process = PythonOperator(
        task_id='process',
        python_callable=_process,
    )
    
    extract >> process

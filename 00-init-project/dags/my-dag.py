from airflow import DAG
from datetime import datetime, timedelta


with DAG(
    dag_id="my_dag",
    description="DAG in cgarge of processing customer data",
    start_date=datetime(2021, 1, 1), # date at which tasks star being scheduled
    schedule_interval="@daily", # interval of time from the min(start_date) at which DAG is triggered
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customers"],
    catchup=False,
    max_active_runs=1, # we wouldn't have more than 1 active DAG
    ) as dag:
    
    # following tasks is not idempotent (we can execute task only once, besause the second once gives us an error):
    # PostgersOperator(task_id="create_table", sql="CREATE TABLE my_table ...")
    # BashOperator(task_id="creating_folder", bash_command="mkdir my_folder")
    
    # following task is a deterministic:
    # PostgersOperator(task_id="create_table", sql="CREATE TABLE IF NOT EXISTS my_table ...")
    
    # backfilling:
    # $bash$ airflow backfill -s 2020-01-01 -e 2021-01-01
    
    pass

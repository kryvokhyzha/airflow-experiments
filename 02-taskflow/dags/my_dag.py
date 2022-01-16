from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta


class CustomPostgresOperator(PostgresOperator):
    
    template_fields = ('sql', 'parameters',)


def _extract(partner_name):
    # partner_settings = Variable.get('my_dag_partner', deserialize_json=True)
    # name = partner_settings['name']
    # api_key = partner_settings['api_key_secret']
    # path = partner_settings['path']
    print(partner_name)

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    dag_id='my_dag',
    description='DAG in charge of processing customer data',
    start_date=datetime(2021, 1, 1),
    max_active_runs=3,
    schedule_interval="@daily",  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'],
    max_active_tasks=1,
    catchup=False # enable if you don't want historical dag runs to run
    ) as dag:
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=_extract,
        op_args=["{{ var.json.my_dag_partner.name }}"]
        # op_args=[Variable.get('my_dag_partner', deserialize_json=True)['name']]
    )
    
    fetching_data = CustomPostgresOperator(
        task_id="fetching_data",
        sql="sql/my_request.sql",
        parameters={
            'next_df': '{{ next_ds }}',
            'prev_df': '{{ prev_ds }}',
            'partner_name': '{{ var.json.my_dag_partner.name }}'
            },
    )

from airflow import DAG
from airflow.operators.empty import EmptyOperator

import pendulum

with DAG(
    dag_id="dag_test1",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=None,
) as dag:

    EmptyOperator(task_id="t1", dag=dag)

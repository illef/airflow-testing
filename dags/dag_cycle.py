import airflow.utils.dates
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="dag_cycle",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval=None,
) as dag:

    t1 = EmptyOperator(task_id="t1", dag=dag)
    t2 = EmptyOperator(task_id="t2", dag=dag)
    t3 = EmptyOperator(task_id="t3", dag=dag)

    t1 >> t2 >> t3 >> t1

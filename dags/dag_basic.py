from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pendulum


def return_arg(foo: str) -> str:
    return foo


with DAG(
    dag_id="basic_operators",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=None,
) as dag:
    bash_task = BashOperator(
        task_id="bash_task",
        bash_command="echo 1",
    )

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=lambda: 1,
    )

    python_task_2 = PythonOperator(
        task_id="python_task_2",
        python_callable=return_arg,
        op_kwargs={"foo": "{{ ds }}"},
    )

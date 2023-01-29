from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.utils.state import DagRunState
from airflow.utils.session import provide_session

import pendulum


with DAG(
    dag_id="test_task_decorator_with_session",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=None,
) as dag:

    @task()
    def use_variable():
        return Variable.get("key")

    use_variable()


class TestTaskWithSession:
    @provide_session
    def test_variable(self, session=None):
        assert session is not None
        session.add(Variable(key="key", val="value"))

        dr = dag.create_dagrun(
            state=DagRunState.RUNNING,
            execution_date=pendulum.now("UTC"),
            run_id="dag_run_id",
            session=session,
        )

        # NOTE: task decorator 로 정의된 PythonOperator 는 아래와 같은 방식으로 TaskInstance를 얻어야하며 반드시 session이 필요하다.
        for ti in dr.task_instances:
            ti.refresh_from_task(dag.get_task(ti.task_id))

        ti = dr.get_task_instance(task_id="use_variable", session=session)
        assert ti is not None

        ti.run(test_mode=True)

        assert ti.xcom_pull(task_ids="use_variable") == "value"

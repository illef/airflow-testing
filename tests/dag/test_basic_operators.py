from airflow.utils.state import DagRunState
import pendulum
from airflow.models.taskinstance import TaskInstance
from dags.dag_basic import bash_task, python_task, python_task_2, python_task_3, dag


def test_bash_operator():
    out = bash_task.execute({})
    assert out == "1"


def test_python_operator():
    out = python_task.execute({})
    assert out == 1


def test_python_operator_2():
    out = python_task_2.execute({})
    assert out == "{{ ds }}"

    # NOTE 우리가 원하는 결과는 ds 가 아닌 DAG run 의 logical date 이다.
    # 이를 위해선 task 가 실행되는 과정을 이해해야 한다.

    # 1. Build task instance concext
    # 2. Clear XCom data for current task instance
    # 3. Render templated variables
    # 4. Run operator.pre_execute()
    # 5. Run operator.execute()
    # 6. Push return value to XCom
    # 7. Run operator.post_execute()

    # 여기선 1, 3, 5 로 충분하다.

    # 1. Build task instance concext
    dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=pendulum.now("UTC"),
        run_id="dag_run_id",
    )
    ti = TaskInstance(task=python_task_2, run_id="dag_run_id")
    # 3. Render templated variables
    ti.render_templates()
    assert python_task_2.op_kwargs == {"foo": pendulum.now("UTC").to_date_string()}
    # 5. Run operator.execute()
    out = python_task_2.execute(ti.get_template_context())
    assert out == pendulum.today("UTC").to_date_string()


def test_python_operator_3():
    # python_task_3 는 xcom_push를 실행합니다. 이를 테스트 하기 위해서는 execute 로는 부족합니다.

    dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=pendulum.now("UTC"),
        run_id="dag_run_id_2",
    )
    ti = TaskInstance(task=python_task_3, run_id="dag_run_id")

    # NOTE: 아래 방식으론 python_task_3 를 실행할 수 없다
    # ti.render_templates()
    # python_task_3.execute(ti.get_template_context())
    # assert ti.xcom_pull(key="xcom_push_value") == None

    # 아래와 같이 task instance 를 실행한 후 xcom 값에 접근해야 한다.
    ti.run(test_mode=True)
    assert ti.xcom_pull(key="xcom_push_value") == "test"
    assert (
        ti.xcom_pull(task_ids="python_task_3") == pendulum.now("UTC").to_date_string()
    )

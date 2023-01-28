import glob
import os

from airflow.operators.bash import BashOperator

# from airflow.models.dag import DagBag

import pytest

# from airflow.models import DAG

DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dags/**.py")
DAG_FILES = glob.glob(DAG_PATH)


@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    print(DAG_PATH)
    # print(dag_file)
    # dag_bag = DagBag(dag_folder=dag_file, include_examples=False)
    # for dag in dag_bag.dags:
    # assert dag is not None

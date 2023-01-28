import glob
import os

from airflow.models.dagbag import DagBag

DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dags/")
DAG_FILES = glob.glob(DAG_PATH)


def test_dag_integrity():
    _ = DagBag(dag_folder=DAG_PATH, include_examples=False)

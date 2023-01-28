#!/bin/bash

docker build -t airflow-test .

docker run --rm -t \
    -v $PWD:/opt/dags airflow-test \
    bash -c 'cd /opt/dags && python -m pytest -s -p no:cacheprovider tests'

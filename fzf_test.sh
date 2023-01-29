#!/bin/bash

docker build -t airflow-test .

docker run --rm -it \
    -v $PWD:/opt/dags airflow-test \
    bash -c 'cd /opt/dags && python -m pytest --fzf'

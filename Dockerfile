FROM apache/airflow:2.5.1-python3.8

USER airflow

# 테스트 실행을 위해 airflow db 를 초기화 해야 한다
RUN airflow db init
RUN pip install pytest

ENV SQLALCHEMY_SILENCE_UBER_WARNING=1

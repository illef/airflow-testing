import logging
from typing import Dict

import requests
import pendulum

from airflow.decorators import task
from airflow import DAG

API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"

# NOTE: dag 는 decorators 스타일을 사용하지 않는다
# @dag(schedule="@daily", start_date=datetime(2021, 12, 1), catchup=False)
# def taskflow():

with DAG(
    dag_id="store_bitcoin_data",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule=None,
) as dag:

    @task(retries=2)
    def extract_bitcoin_price() -> Dict[str, float]:
        return requests.get(API).json()["bitcoin"]

    @task(multiple_outputs=True)
    def process_data(response: Dict[str, float]) -> Dict[str, float]:
        logging.info(response)
        return {"usd": response["usd"], "change": response["usd_24h_change"]}

    @task
    def store_data(data: Dict[str, float]):
        logging.info(f"Store: {data['usd']} with change {data['change']}")

    store_data(process_data(extract_bitcoin_price()))

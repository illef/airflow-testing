from airflow.models.xcom_arg import PlainXComArg
from dags.store_bitcoin_data import extract_bitcoin_price, process_data


def test_extract_bitcoin_price():
    out: PlainXComArg = extract_bitcoin_price()
    assert isinstance(out, PlainXComArg)
    data = extract_bitcoin_price.__wrapped__()
    assert list(data.keys()) == [
        "usd",
        "usd_market_cap",
        "usd_24h_vol",
        "usd_24h_change",
        "last_updated_at",
    ]

    data = process_data.__wrapped__(data)
    assert list(data.keys()) == ["usd", "change"]

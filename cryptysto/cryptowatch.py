import requests
import pytz
from datetime import datetime
from typing import Optional

BASEURL = "https://api.cryptowat.ch/markets/%s/%s/ohlc?after=%s&before=%s&periods=7200"


def build_api_key_qarg(apiKey: Optional[str]) -> str:
    return "&apikey=%s" % apiKey if apiKey else ""


def build_query_url(exchange: str, pair: str, date: int, apiKey: Optional[str]) -> str:
    baseurl = BASEURL % (exchange, pair, date, date + 7200) + build_api_key_qarg(apiKey)
    print(baseurl)
    return baseurl


def get_price(exchange: str, pair: str, date: datetime, apiKey: Optional[str]) -> float:
    epoch = pytz.utc.localize(date, is_dst=False).timestamp()
    resp = requests.get(build_query_url(exchange, pair, date=int(epoch), apiKey=apiKey))
    try:
        resp.raise_for_status()
    except Exception as exc:
        print(
            "Warn - [%s/%s] Unable to get ticket price due to %s"
            % (exchange, pair, exc)
        )
        return 0
    data = resp.json()
    if "result" in data and data["result"]["7200"]:
        return data["result"]["7200"][0][4]
    else:
        print("Warn - [%s/%s] No ticker price for that date" % (exchange, pair))
        return 0

import requests
import pytz
from datetime import datetime

BASEURL = "https://api.cryptowat.ch/markets/%s/%s/ohlc?after=%s&before=%s&periods=7200"


def build_query_url(exchange: str, pair: str, date: int) -> str:
    baseurl = BASEURL % (exchange, pair, date, date + 7200)
    print(baseurl)
    return baseurl


def get_price(exchange: str, pair: str, date: datetime) -> float:
    epoch = pytz.utc.localize(date, is_dst=False).timestamp()
    resp = requests.get(build_query_url(exchange, pair, date=int(epoch)))
    try:
        resp.raise_for_status()
    except Exception as exc:
        print("Warn - Unable to get ticket price due to %s" % exc)
        return 0
    data = resp.json()
    if "result" in data:
        return data["result"]["7200"][0][4]
    else:
        raise RuntimeError("Unable to decode exchange response")

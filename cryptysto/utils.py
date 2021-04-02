from typing import List, Union
from csv import reader
from pathlib import Path
from dataclasses import dataclass

from cryptysto.types import *


assets_map = {"XXBT": "BTC", "XXDG": "DOGE", "XETH": "ETH", "ZEUR": "EUR"}


def is_fiat(name: str) -> bool:
    if name in ("EUR", "USD"):
        return True
    else:
        return False


def asset(asset_name: str) -> Asset:
    return Asset(
        name=assets_map.get(asset_name, asset_name),
        _type="fiat" if is_fiat(asset_name) else "crypto",
    )


def read_csv(path: Path) -> List:
    return list(reader(open(path).readlines(), delimiter=","))[1:]

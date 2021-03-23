from dataclasses import dataclass
from datetime import datetime
from typing import List, Callable
from pathlib import Path

from cryptysto.utils import read_csv, asset

from cryptysto.types import *


def load_binance_ledger_file(path: Path) -> BinanceLedger:
    return list(
        map(
            lambda o: BinanceLedgerEntry(
                time=datetime.strptime(o[0], "%Y-%m-%d %H:%M:%S"),
                account=o[1],
                operation=o[2],
                coin=o[3],
                change=float(o[4]),
                remark=o[5],
            ),
            read_csv(path),
        )
    )


def transform_binance_le_to_generic(le: BinanceLedgerEntry) -> GenericOpTypes:
    entry: GenericOpTypes = []
    if le.operation == "Deposit":
        entry.append(
            Deposit(
                exchange="Binance", date=le.time, asset=asset(le.coin), amount=le.change
            )
        )
    return entry

from dataclasses import dataclass
from datetime import datetime
from typing import List, Callable
from pathlib import Path

from cryptysto.utils import read_csv, asset

from cryptysto.types import *


def load_local_ledger_file(path: Path) -> LocalLedger:
    return list(
        map(
            lambda o: LocalLedgerEntry(
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


def transform_local_le_to_generic(le: LocalLedgerEntry) -> GenericOpTypes:
    entry: GenericOpTypes = []
    if le.operation == "Deposit":
        entry.append(
            Deposit(
                exchange="Local", date=le.time, asset=asset(le.coin), amount=le.change
            )
        )
    if le.operation == "Withdrawal":
        entry.append(
            Withdrawal(
                exchange="Local", date=le.time, asset=asset(le.coin), amount=le.change
            )
        )
    return entry

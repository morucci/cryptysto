import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Callable
from pathlib import Path

from cryptysto.utils import read_csv, asset

from cryptysto.types import *


def load_bitfinex_ledger_file(path: Path) -> BitfinexLedger:
    return list(
        map(
            lambda o: BitfinexLedgerEntry(
                _id=o[0],
                desc=o[1],
                currency=o[2],
                amount=float(o[3]),
                balance=float(o[4]),
                date=datetime.strptime(o[5], "%d-%m-%y %H:%M:%S"),
                wallet=o[6],
            ),
            read_csv(path),
        )
    )


def transform_bifinex_le_to_generic(le: BitfinexLedgerEntry) -> GenericOpTypes:
    entry: GenericOpTypes = []
    if re.match("^Deposit \(.*", le.desc):
        entry.append(
            Deposit(
                exchange="Bitfinex",
                date=le.date,
                asset=asset(le.currency),
                amount=abs(le.amount),
            )
        )
    if re.match("^Deposit Fee \(.*", le.desc):
        entry.append(
            DepositFee(
                exchange="Bitfinex",
                date=le.date,
                asset=asset(le.currency),
                amount=abs(le.amount),
            )
        )
    if re.match("^.+ Withdrawal #\d+", le.desc):
        entry.append(
            Withdrawal(
                exchange="Bitfinex",
                date=le.date,
                asset=asset(le.currency),
                amount=abs(le.amount),
            )
        )
    if re.match("^.+ Withdrawal fee", le.desc):
        entry.append(
            WithdrawalFee(
                exchange="Bitfinex",
                date=le.date,
                asset=asset(le.currency),
                amount=abs(le.amount),
            )
        )
    if re.match("^Exchange .+", le.desc):
        entry.append(
            Trade(
                exchange="Bitfinex",
                date=le.date,
                asset=asset(le.currency),
                amount=le.amount,
            )
        )
    if re.match("^Trading fees for .+", le.desc):
        entry.append(
            TradeFee(
                exchange="Bitfinex",
                date=le.date,
                asset=asset(le.currency),
                amount=abs(le.amount),
            )
        )
    return entry

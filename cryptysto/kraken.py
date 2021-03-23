from typing import List, Callable
from datetime import datetime
from pathlib import Path

from cryptysto.utils import read_csv, asset

from cryptysto.types import *


def load_kraken_ledger_file(path: Path) -> KrakenLedger:
    return list(
        map(
            lambda o: KrakenLedgerEntry(
                txid=o[0],
                refid=o[1],
                time=datetime.strptime(o[2], "%Y-%m-%d %H:%M:%S"),
                _type=o[3],
                subtype=o[4],
                aclass=o[5],
                asset=o[6],
                amount=float(o[7]),
                fee=float(o[8]),
                balance=float(0) if o[9] == "" else float(o[9]),
            ),
            read_csv(path),
        )
    )


def transform_kraken_le_to_generic(le: KrakenLedgerEntry) -> GenericOpTypes:
    entry: GenericOpTypes = []
    if le._type == "deposit" and le.txid and le.refid:
        entry.append(
            Deposit(
                exchange="Kraken", date=le.time, asset=asset(le.asset), amount=le.amount
            )
        )
        entry.append(
            DepositFee(
                exchange="Kraken", date=le.time, asset=asset(le.asset), amount=le.fee
            )
        )
    if le._type == "withdrawal" and le.txid and le.refid:
        entry.append(
            Withdrawal(
                exchange="Kraken", date=le.time, asset=asset(le.asset), amount=le.amount
            )
        )
        entry.append(
            WithdrawalFee(
                exchange="Kraken", date=le.time, asset=asset(le.asset), amount=le.fee
            )
        )
    return entry

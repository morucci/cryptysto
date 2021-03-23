from dataclasses import dataclass
from typing import Literal, List, Union
from datetime import datetime
from pathlib import Path

from cryptysto.types import *

from cryptysto.binance import transform_binance_le_to_generic, load_binance_ledger_file
from cryptysto.bitfinex import (
    transform_bifinex_le_to_generic,
    load_bitfinex_ledger_file,
)
from cryptysto.kraken import transform_kraken_le_to_generic, load_kraken_ledger_file


def load_ledger_file(
    _type: LedgerType, path: Path
) -> Union[BitfinexLedger, KrakenLedger, BinanceLedger]:
    if _type == "bitfinex":
        return load_bitfinex_ledger_file(path)
    elif _type == "kraken":
        return load_kraken_ledger_file(path)
    elif _type == "binance":
        return load_binance_ledger_file(path)
    else:
        raise RuntimeError("Ledger type not supported")


def transform_to_generic(ledgers: InputLedgers) -> GenericLedger:
    generic = GenericLedger(ops=[])
    for ledger in ledgers:
        for le in ledger:
            if isinstance(le, KrakenLedgerEntry):
                generic.ops.extend(transform_kraken_le_to_generic(le))
            if isinstance(le, BinanceLedgerEntry):
                generic.ops.extend(transform_binance_le_to_generic(le))
            if isinstance(le, BitfinexLedgerEntry):
                generic.ops.extend(transform_bifinex_le_to_generic(le))
    return generic


def display_ledger(ledger: GenericLedger) -> None:
    for op in sorted(ledger.ops, key=lambda e: e.date):
        print(op.show())


def display_summary(ledger: GenericLedger) -> None:
    exhanges = set([op.exchange for op in ledger.ops])
    assets = set([op.asset.name for op in ledger.ops])

    m = {
        "Deposit": Deposit,
        "Deposit Fee": DepositFee,
        "Withdrawal": Withdrawal,
        "Withdrawal Fee": WithdrawalFee,
    }
    for op_type in m.keys():
        for exchange in exhanges:
            for asset in assets:
                total = sum(
                    [
                        op.amount
                        for op in ledger.ops
                        if isinstance(op, m[op_type])
                        and op.asset.name == asset
                        and op.exchange == exchange
                    ]
                )
                if total != 0:
                    print(
                        "Total %s on %s of %s: %s" % (op_type, exchange, asset, total)
                    )

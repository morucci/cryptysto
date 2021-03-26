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
from cryptysto import utils


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
    balances: Balances = dict()

    m = {
        "Deposit": Deposit,
        "Deposit Fee": DepositFee,
        "Withdrawal": Withdrawal,
        "Withdrawal Fee": WithdrawalFee,
        "Trade": Trade,
        "Trade Fee": TradeFee,
    }

    def get_exchange_balance(exchange: str) -> Balance:
        return balances.get(exchange, Balance(exchange=exchange, assets=[]))

    def set_exchange_balance(exchange: str, balance: Balance) -> None:
        balances[exchange] = balance

    def get_total_buy(
        ledger: GenericLedger, op_type: str, exchange: str, asset: str
    ) -> float:
        return sum(
            [
                abs(op.amount)
                for op in ledger.ops
                if isinstance(op, m[op_type])
                and op.amount > 0
                and op.asset.name == asset
                and op.exchange == exchange
            ]
        )

    def get_total_sell(
        ledger: GenericLedger, op_type: str, exchange: str, asset: str
    ) -> float:
        return sum(
            [
                abs(op.amount)
                for op in ledger.ops
                if isinstance(op, m[op_type])
                and op.amount < 0
                and op.asset.name == asset
                and op.exchange == exchange
            ]
        )

    for op_type in m.keys():
        for exchange in exhanges:
            eb = get_exchange_balance(exchange=exchange)
            for asset in assets:
                if op_type == "Trade":
                    total_sell = get_total_sell(ledger, op_type, exchange, asset)
                    total_buy = get_total_buy(ledger, op_type, exchange, asset)
                    if total_buy or total_sell:
                        print(
                            "Total %s on %s of %s: BUY: %s, SELL: %s"
                            % (op_type, exchange, asset, total_buy, total_sell)
                        )
                        eb.assets.append(
                            AssetBalance(
                                amount=total_buy - total_sell, asset=utils.asset(asset)
                            )
                        )
                else:
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
                            "Total %s on %s of %s: %s"
                            % (op_type, exchange, asset, total)
                        )
            set_exchange_balance(exchange=exchange, balance=eb)

    for balance in balances.values():
        print(balance.show())

#!/bin/env python3

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Union, Final
from csv import reader
import argparse
import yaml
from dacite import from_dict
import re
from datetime import datetime

from cryptysto.ledger import (
    load_ledger_file,
    transform_to_generic,
    display_ledger,
    display_ledger_summary,
    display_last_op,
)
from cryptysto.balance import display_balance

from cryptysto.types import *


# Todo (because it does not appear in my samples)
# - Binance withwdrawal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the configuration file")
    parser.add_argument(
        "--show-ledger-ops", help="Show all ledger operations", action="store_true"
    )
    parser.add_argument(
        "--show-ledger-summary", help="Show ledger summary", action="store_true"
    )
    parser.add_argument("--show-balances", help="Show balances", action="store_true")
    parser.add_argument(
        "--show-last-op", help="Show last known operation", action="store_true"
    )
    parser.add_argument(
        "--compute-usdt-value", help="Add usdt value to balance", action="store_true"
    )
    parser.add_argument(
        "--filter-op-type",
        help="Filter on operation type",
        choices=[
            "Deposit",
            "DepositFee",
            "Withdrawal",
            "WithdrawalFee",
            "Trade",
            "TradeFee",
        ],
    )
    parser.add_argument(
        "--filter-asset-type",
        help="Filter on asset type type",
        choices=[
            "crypto",
            "fiat",
        ],
    )
    parser.add_argument("--compute-until", help="Compute until date")
    args = parser.parse_args()

    input_ledgers: InputLedgers = []

    config = from_dict(data_class=Config, data=yaml.safe_load(open(args.config)))
    for ledger_c in config.ledgers:
        input_ledgers.append(load_ledger_file(ledger_c._type, Path(ledger_c.path)))

    generic_ledger = transform_to_generic(input_ledgers)

    until_dt = datetime.now()

    if args.compute_until:
        until_dt = datetime.strptime(args.compute_until, "%Y-%m-%d")
        generic_ledger.ops = list(
            filter(lambda op: op.date <= until_dt, generic_ledger.ops)
        )

    if args.filter_op_type:
        m = {
            "Deposit": Deposit,
            "DepositFee": DepositFee,
            "Withdrawal": Withdrawal,
            "WithdrawalFee": WithdrawalFee,
            "Trade": Trade,
            "TradeFee": TradeFee,
        }
        generic_ledger.ops = list(
            filter(
                lambda op: isinstance(op, m[args.filter_op_type]), generic_ledger.ops
            )
        )

    if args.filter_asset_type:
        generic_ledger.ops = list(
            filter(
                lambda op: op.asset._type == args.filter_asset_type, generic_ledger.ops
            )
        )

    if args.show_ledger_ops:
        print("LEDGER operations")
        print("=================")
        display_ledger(generic_ledger)

    if args.show_ledger_summary:
        print("LEDGER Summary")
        print("==============")
        display_ledger_summary(generic_ledger)

    if args.show_balances:
        print("BALANCE Summary at %s" % until_dt)
        print("==============")
        display_balance(
            generic_ledger, until_dt, args.compute_usdt_value, config.apikey
        )

    if args.show_last_op:
        print("Last operation")
        print("==============")
        display_last_op(generic_ledger)


main()

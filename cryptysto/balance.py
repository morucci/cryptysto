from cryptysto.types import *
from cryptysto import utils
from typing import Callable


def compute_balance(ledger: GenericLedger) -> Balances:
    balances = Balances(balances=dict())

    for op in ledger.ops:
        if isinstance(op, Trade):
            eb = balances.get_exchange_balance(op.exchange)
            if op.amount < 0:
                eb.remove_from_asset(op.asset, op.amount)
            if op.amount > 0:
                eb.add_to_asset(op.asset, op.amount)
        if isinstance(op, Withdrawal):
            eb = balances.get_exchange_balance(op.exchange)
            eb.remove_from_asset(op.asset, op.amount)
        if isinstance(op, Deposit):
            eb = balances.get_exchange_balance(op.exchange)
            eb.add_to_asset(op.asset, op.amount)

    return balances


def display_balance(ledger: GenericLedger) -> None:
    b = compute_balance(ledger)
    print(b.show())

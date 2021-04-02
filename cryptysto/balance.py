from cryptysto.types import *
from cryptysto import utils
from typing import Callable


def compute_balance(ledger: GenericLedger) -> Balances:
    balances = Balances(balances=dict())

    for op in ledger.ops:
        eb = balances.get_exchange_balance(op.exchange)
        if isinstance(op, Trade):
            if op.amount < 0:
                eb.remove_from_asset(op.asset, op.amount)
            if op.amount > 0:
                eb.add_to_asset(op.asset, op.amount)
        if isinstance(op, Withdrawal):
            eb.remove_from_asset(op.asset, op.amount)
        if isinstance(op, WithdrawalFee):
            eb.remove_from_asset(op.asset, op.amount)
        if isinstance(op, DepositFee):
            eb.remove_from_asset(op.asset, op.amount)
        if isinstance(op, Deposit):
            eb.add_to_asset(op.asset, op.amount)
        if isinstance(op, TradeFee):
            eb.remove_from_asset(op.asset, op.amount)

    return balances


def display_balance(ledger: GenericLedger) -> None:
    b = compute_balance(ledger)
    print(b.show())

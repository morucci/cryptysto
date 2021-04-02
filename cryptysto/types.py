from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Union, Dict


@dataclass(frozen=True)
class KrakenLedgerEntry:
    txid: str
    refid: str
    time: datetime
    _type: str
    subtype: str
    aclass: str
    asset: str
    amount: float
    fee: float
    balance: float


KrakenLedger = List[KrakenLedgerEntry]


@dataclass(frozen=True)
class BitfinexLedgerEntry:
    _id: str
    desc: str
    currency: str
    amount: float
    balance: float
    date: datetime
    wallet: str


BitfinexLedger = List[BitfinexLedgerEntry]


@dataclass(frozen=True)
class BinanceLedgerEntry:
    time: datetime
    account: str
    operation: str
    coin: str
    change: float
    remark: str


BinanceLedger = List[BinanceLedgerEntry]


@dataclass
class Asset:
    name: str
    _type: Literal["crypto", "fiat"]


LedgerType = Literal["bitfinex", "kraken", "binance"]


@dataclass
class LedgerConfig:
    path: str
    _type: LedgerType


@dataclass
class Config:
    ledgers: List[LedgerConfig]


@dataclass(frozen=True)
class DWBase:
    exchange: str
    date: datetime
    asset: Asset
    amount: float

    def get_str(self):
        raise NotImplementedError

    def show(self):
        return self.get_str() % (
            self.date,
            self.exchange,
            self.asset.name,
            self.amount,
        )


@dataclass(frozen=True)
class Deposit(DWBase):
    def get_str(self):
        return "%s: [%s] Deposit [%s] amount: %s"


@dataclass(frozen=True)
class DepositFee(DWBase):
    def get_str(self):
        return "%s: [%s] Deposit Fee [%s] amount: %s"


@dataclass(frozen=True)
class Withdrawal(DWBase):
    def get_str(self):
        return "%s: [%s] Witdrawal [%s] amount: %s"


@dataclass(frozen=True)
class WithdrawalFee(DWBase):
    def get_str(self):
        return "%s: [%s] Withdrawal Fee [%s] amount: %s"


@dataclass(frozen=True)
class Trade(DWBase):
    def get_str(self):
        return "%s: [%s] Trade [%s] amount: %s"


@dataclass(frozen=True)
class TradeFee(DWBase):
    def get_str(self):
        return "%s: [%s] Trade Fee [%s] amount: %s"


GenericOpTypes = List[
    Union[Deposit, DepositFee, Withdrawal, WithdrawalFee, Trade, TradeFee]
]


@dataclass
class GenericLedger:
    ops: GenericOpTypes


InputLedgers = List[Union[BitfinexLedger, KrakenLedger, BinanceLedger]]


@dataclass
class AssetBalance:
    asset: Asset
    amount: float

    def show(self):
        return "[%s]: %s" % (self.asset.name, self.amount)

    def is_low(self):
        if self.amount > 0.00001:
            return False
        else:
            return True

    def add(self, amount: float):
        self.amount += abs(amount)

    def remove(self, amount: float):
        self.amount -= abs(amount)


@dataclass
class ExchangeBalance:
    exchange: str
    assets: Dict[str, AssetBalance]

    def show(self):
        return "\n".join(
            map(
                lambda ab: self.exchange + ab.show(),
                [a for a in self.assets.values() if not a.is_low()],
            )
        )

    def add_to_asset(self, asset: Asset, amount: float):
        if asset.name not in self.assets:
            self.assets[asset.name] = AssetBalance(asset=asset, amount=0)
        ab = self.assets[asset.name]
        ab.add(amount)

    def remove_from_asset(self, asset: Asset, amount: float):
        if asset.name not in self.assets:
            self.assets[asset.name] = AssetBalance(asset=asset, amount=0)
        ab = self.assets[asset.name]
        ab.remove(amount)


@dataclass
class Balances:
    balances: Dict[str, ExchangeBalance]

    def get_exchange_balance(self, exchange: str) -> ExchangeBalance:
        if exchange not in self.balances:
            self.balances[exchange] = ExchangeBalance(exchange=exchange, assets=dict())
        return self.balances[exchange]

    def show(self):
        return "\n".join([eb.show() for eb in self.balances.values()])

# Cryptysto

A small tool to compute assets accros exchanges. Only Bitfinex, Kraken and Binance are supported.

This tool is for demo purpose only. Results might not be accurate.

## Usage

Create a config.yaml file such as:

```YAML
apikey: YOUR-CRYPTOWATCH-API-KEY (Read only - optional - to get historical USDT - higher api rate limit)
ledgers:
  - path: path-to-ledger csv file
    _type: binance|kraken|bitfinex|local
  ...
```

### Show balance

```Shell
[user@781d164145e9 cryptysto]$ ./main.py --config=config.yaml --show-balance --compute-usdt-value
Dedup Warn: 2021-02-09 23:42:24: [Binance] Trade [LTC] amount: XXX
Dedup Warn: 2021-02-09 23:42:24: [Binance] Trade [USDT] amount: XXX
Dedup Warn: 2021-02-02 08:43:57: [Kraken] Trade Fee [EUR] amount: XXX
...
BALANCE Summary at 2021-04-05 08:04:44.875077
==============
Binance[BTC]: XXX USDT:XXX
Binance[LTC]: XXX USDT:XXX
Binance[TOTAL CRYPTO ASSET USDT VALUE]: XXX
Kraken[BTC]: XXX USDT:XXX
Kraken[DOGE]: XXX USDT:XXX
Kraken[TOTAL CRYPTO ASSET USDT VALUE]: XXX
TOTAL CRYPTO ASSET USDT VALUE: XXX
```

### Show ledger summary

Note the filtering capability.

```Shell
[user@781d164145e9 cryptysto]$ ./main.py --config=config.yaml --show-ledger-summary --filter-exchange Kraken --filter-op-type Deposit --filter-asset-type fiat
LEDGER Summary
==============
Total Deposit on Kraken of EUR: XXX
```

### Usage help

```Shell
[user@781d164145e9 cryptysto]$ ./main.py -h
usage: main.py [-h] [--config CONFIG] [--show-ledger-ops] [--show-ledger-summary] [--show-balances] [--show-last-op] [--compute-usdt-value]
               [--filter-op-type {Deposit,DepositFee,Withdrawal,WithdrawalFee,Trade,TradeFee}] [--filter-asset-type {crypto,fiat}]
               [--filter-exchange {Binance,Bitfinex,Kraken,Local}] [--compute-until COMPUTE_UNTIL]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the configuration file
  --show-ledger-ops     Show all ledger operations
  --show-ledger-summary
                        Show ledger summary
  --show-balances       Show balances
  --show-last-op        Show last known operation
  --compute-usdt-value  Add usdt value to balance
  --filter-op-type {Deposit,DepositFee,Withdrawal,WithdrawalFee,Trade,TradeFee}
                        Filter on operation type
  --filter-asset-type {crypto,fiat}
                        Filter on asset type type
  --filter-exchange {Binance,Bitfinex,Kraken,Local}
                        Filter on exchange name
  --compute-until COMPUTE_UNTIL
                        Compute until date
```

## Contribute

Any help welcome via Pull Request

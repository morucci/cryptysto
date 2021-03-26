from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Union, Final
from csv import reader
import argparse
import yaml
from dacite import from_dict
import re

from cryptysto.ledger import (
    load_ledger_file,
    transform_to_generic,
    display_ledger,
    display_ledger_summary,
)
from cryptysto.balance import display_balance

from cryptysto.types import *


# Todo (because it does not appear in my samples)
# - Binance deposit fee
# - Binance withwdrawal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the configuration file")
    args = parser.parse_args()

    input_ledgers: InputLedgers = []

    config = from_dict(data_class=Config, data=yaml.safe_load(open(args.config)))
    for ledger_c in config.ledgers:
        input_ledgers.append(load_ledger_file(ledger_c._type, Path(ledger_c.path)))

    generic_ledger = transform_to_generic(input_ledgers)

    display_ledger(generic_ledger)
    display_ledger_summary(generic_ledger)
    display_balance(generic_ledger)


main()

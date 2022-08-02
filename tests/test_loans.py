# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 23:29:08 2020

@author: PaulJ
"""

from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import logging
from typing import Any
from cashflowsim.loans import Loan

# from tests.test_board import GAME_DATA_DIR, LOG_DIR

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
LOG_DIR: str = "game_logs"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)

this_fn: str = __file__.split("\\")[-1].split(".")[0]
logfile_fn: str = "".join([this_fn, "_log.txt"])

logfile_path_fn: str = join(base_path, APP_DIR, LOG_DIR, logfile_fn)

logging.basicConfig(
    filename=logfile_path_fn,
    # level=logging.DEBUG,
    level=logging.ERROR,
    filemode="w",
    format="%(asctime)s - (%(levelname)s) %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    force=True,
)
logging.info(
    f"\n\n\nStart of new test run: {dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
)


TESTS: list[dict[str, Any]] = [
    {
        "name": "Mortgage",
        "initial_balance": 105000,
        "monthly_payment": 1500,
        "partial_payment_allowed": False,
        "payment": 50000,
        "result": False,
        "new_balance": 105000,
    },
    {
        "name": "Mortgage",
        "initial_balance": 105000,
        "monthly_payment": 1500,
        "partial_payment_allowed": False,
        "payment": 105000,
        "result": True,
        "new_balance": 0,
    },
    {
        "name": "Bank Loan",
        "initial_balance": 100000,
        "monthly_payment": 10000,
        "partial_payment_allowed": True,
        "payment": 6500,
        "result": False,
        "new_balance": 100000,
    },
    {
        "name": "Bank Loan",
        "initial_balance": 100000,
        "monthly_payment": 10000,
        "partial_payment_allowed": True,
        "payment": 500,
        "result": False,
        "new_balance": 100000,
    },
    {
        "name": "Bank Loan",
        "initial_balance": 100000,
        "monthly_payment": 10000,
        "partial_payment_allowed": True,
        "payment": 10100,
        "result": False,
        "new_balance": 100000,
    },
    {
        "name": "Bank Loan",
        "initial_balance": 100000,
        "monthly_payment": 10000,
        "partial_payment_allowed": True,
        "payment": 10000,
        "result": True,
        "new_balance": 90000,
    },
]


def test_loan_and_payment():
    """General test using list of tests above."""
    for a_test in TESTS:
        my_loan: Loan = Loan(
            name=a_test["name"],
            balance=a_test["initial_balance"],
            monthly_payment=a_test["monthly_payment"],
            partial_payment_allowed=a_test["partial_payment_allowed"],
        )

        logging.info(f"\nAble to create loan:\n{my_loan}")
        result = my_loan.make_payment(payment=a_test["payment"])
        assert result == a_test["result"]
        logging.info(
            f"Able to make payment ({a_test['payment']}) "
            f"on loan and got correct result ({result})"
        )
        assert my_loan.balance == a_test["new_balance"]

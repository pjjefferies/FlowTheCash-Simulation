# -*- coding: utf-8 -*-
"""
Created on Sun May  8 22:03:33 2022

@author: PaulJ
"""

from os.path import join, abspath
from os import listdir
from inspect import getsourcefile
import datetime as dt
import logging
import pytest

from cashflowsim.strategy import Strategy, get_strategy_defs

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
STRATEGIES_DIR = "simulation_strategies"
TESTS_DIR = "tests"
LOG_DIR: str = "game_logs"

BAD_JSON_FILE_NO_DATA_FN: str = "dummy_file_for_test.json"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)

this_fn: str = __file__.split("\\")[-1].split(".")[0]
logfile_fn: str = "".join([this_fn, "_log.txt"])

logfile_path_fn: str = join(base_path, APP_DIR, LOG_DIR, logfile_fn)
bad_json_file_no_data_path_fn: str = join(
    base_path, TESTS_DIR, BAD_JSON_FILE_NO_DATA_FN
)

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


@pytest.fixture
def strategies() -> dict[str, Strategy]:
    base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
    strategies_path: str = join(base_path, APP_DIR, STRATEGIES_DIR)
    strategies_fn_list: list[str] = [
        f for f in listdir(strategies_path) if f.endswith(".json")
    ]
    all_strategies: dict[str, Strategy] = {}
    for a_strategy_fn in strategies_fn_list:
        strategy_defs_fn: str = join(base_path, APP_DIR, STRATEGIES_DIR, a_strategy_fn)
        some_strategies: dict[str, Strategy] = get_strategy_defs(
            strategy_defs_fn=strategy_defs_fn
        )
        all_strategies.update(some_strategies)
    return all_strategies


def test_strategy_name(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert (
            isinstance(strategies[a_strategy].name, str)
            and len(strategies[a_strategy].name) > 0
        )


def test_strategy_manual(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].manual, bool)


def test_roi_threshold(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].roi_threshold, float)
        assert strategies[a_strategy].roi_threshold >= 0.0
        assert strategies[a_strategy].roi_threshold <= 1.0


def test_price_ratio_threshold(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].price_ratio_threshold, float)
        assert strategies[a_strategy].price_ratio_threshold >= -1.0
        assert strategies[a_strategy].price_ratio_threshold <= 1.0


def test_take_downpayment_loans(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].take_downpayment_loans, bool)


def test_take_any_loans(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].take_any_loans, bool)


def test_charitable(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].charitable, bool)


def test_loan_payback(strategies: dict[str, Strategy]) -> None:
    for a_strategy in strategies:
        assert isinstance(strategies[a_strategy].loan_payback, str)
        assert strategies[a_strategy].loan_payback in [
            "Smallest",
            "Largest",
            "Never",
            "Highest Interest",
        ]


def test_load_strategies_bad_filename() -> None:
    bad_strategy_cards_path_fn = join(game_data_path, "on_the_moon.json")
    try:
        get_strategy_defs(strategy_defs_fn=bad_strategy_cards_path_fn)
    except OSError as e:
        logging.info(
            f"Strategy filename: {bad_strategy_cards_path_fn} correctly not found "
            f"with message: {e}"
        )
        return
    err_msg = (
        f"Bad Strategy filename: {bad_strategy_cards_path_fn} not reported as unfound"
    )
    logging.error(err_msg)
    raise OSError(err_msg)


def test_load_strategies_bad_json_data() -> None:
    try:
        get_strategy_defs(strategy_defs_fn=bad_json_file_no_data_path_fn)
    except ValueError as e:
        logging.info(
            f"Strategies filename: {bad_json_file_no_data_path_fn} correctly identified as bad json data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad strategies filename: {bad_json_file_no_data_path_fn} not reported as having bad json data"
    logging.error(err_msg)
    raise ValueError(err_msg)

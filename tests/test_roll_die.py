# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:48:03 2022

@author: PaulJ
"""
from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import statistics
from typing import Callable
import logging

from _pytest.monkeypatch import MonkeyPatch

from cashflowsim.roll_die import roll_die

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
    filemode="a",
    format="%(asctime)s - (%(levelname)s) %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    force=True,
)
logging.info(
    f"\n\n\nStart of new test run: {dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
)


hit_enter: Callable[[str], str] = lambda _: ""


def test_die_roll_100_auto():
    """Test 100 Automatic Die Rolls"""
    die_rolls: list[int] = []
    logging.info("\n100 Automatic Rolls of one die in verbose mode")
    for _ in range(100):  # Try 100 automatic rolls in verbose
        die_result = roll_die(strategy="Automatic", no_of_dice=1)
        die_rolls.append(die_result)
    mean_die_roll = statistics.mean(die_rolls)
    std_dev_die_roll = statistics.stdev(die_rolls)
    logging.info(
        f"For 100 Automatic Die Rolls: Mean = {mean_die_roll}"
        f"\nStd. Dev. = {std_dev_die_roll}"
    )


def test_die_roll_5_manual(monkeypatch: MonkeyPatch):
    logging.info("\n5 Manual Rolls of one die in verbose mode")

    die_rolls: list[int] = []
    for _ in range(5):
        with monkeypatch.context() as m:
            # m.setattr("builtins.input", lambda _: "")
            m.setattr("builtins.input", hit_enter)
            die_result = roll_die(strategy="Manual", no_of_dice=1)
        die_rolls.append(die_result)
    mean_die_roll = statistics.mean(die_rolls)
    std_dev_die_roll = statistics.stdev(die_rolls)
    logging.info(
        f"For 5 Manual Rolls of 2 Dice: Mean = {mean_die_roll}"
        f"\nStd. Dev. = {std_dev_die_roll}"
    )


def test_dice_roll_100_auto():
    """Test 100 Automatic Die Rolls"""
    die_rolls: list[int] = []
    logging.info("\n100 Automatic Rolls of 2 dice in verbose mode")
    for _ in range(100):  # Try 100 automatic rolls in verbose
        die_result = roll_die(strategy="Automatic", no_of_dice=2)
        die_rolls.append(die_result)
    mean_die_roll = statistics.mean(die_rolls)
    std_dev_die_roll = statistics.stdev(die_rolls)
    logging.info(
        f"For 100 Automatic Die Rolls: Mean = {mean_die_roll}"
        f"\nStd. Dev. = {std_dev_die_roll}"
    )


def test_dice_roll_5_manual(monkeypatch: MonkeyPatch):
    logging.info("\n5 Manual Rolls of 2 dice in verbose mode")

    die_rolls: list[int] = []
    for _ in range(5):
        with monkeypatch.context() as m:
            # m.setattr("builtins.input", lambda _: "")
            m.setattr("builtins.input", hit_enter)
            die_result = roll_die(strategy="Manual", no_of_dice=2)
        die_rolls.append(die_result)
    mean_die_roll = statistics.mean(die_rolls)
    std_dev_die_roll = statistics.stdev(die_rolls)
    logging.info(
        f"For 5 Manual Rolls of 2 Dice: Mean = {mean_die_roll}"
        f"\nStd. Dev. = {std_dev_die_roll}"
    )

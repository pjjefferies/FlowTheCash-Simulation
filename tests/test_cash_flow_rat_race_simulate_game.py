# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:06:05 2022

@author: PaulJ
"""

from os.path import join, abspath
import datetime as dt
from inspect import getsourcefile
import time
import random
import logging

from cashflowsim.cash_flow_rat_race_simulate_game import (
    cash_flow_rat_race_simulate_game,
)
from cashflowsim.profession import Profession, get_profession_defs
from cashflowsim.strategy import Strategy, get_strategy_defs


APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
STRATEGIES_DIR: str = "simulation_strategies"
LOG_DIR: str = "game_logs"

PROFESSIONS_FN = "ProfessionsList.json"
STRATEGIES_FN = "Strategies.json"

NO_SIMS: int = 5
PROFESSION_TEST_NAME: str = "Engineer"
"""
STRATEGY_TEST_NAME: list[str] = ["Super Conservative",
                                 "Dave Ramsey",
                                 "Standard Auto",
                                 "LowBDT, LowPRT, HighHighROIT"]
"""

VERBOSE = False

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)
profession_data_path_fn: str = join(game_data_path, PROFESSIONS_FN)
strategies_data_path: str = join(base_path, APP_DIR, STRATEGIES_DIR)
strategies_data_path_fn: str = join(strategies_data_path, STRATEGIES_FN)

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

strategies_dict: dict[str, Strategy] = get_strategy_defs(
    strategy_defs_fn=strategies_data_path_fn
)
strategy_names: list[str] = list(strategies_dict.keys())


def test_cash_flow_rat_race_simulate_game():
    total_time: float = 0.0
    for test in range(0, NO_SIMS):
        start_time = time.time()
        random.seed(test)

        # Load list of professions and create empty list of players

        profession_dict: dict[str, Profession] = get_profession_defs(
            profession_data_path_fn
        )

        strategy_dict: dict[str, Strategy] = get_strategy_defs(
            strategy_defs_fn=strategies_data_path_fn
        )

        am_i_rich: bool
        am_i_broke: bool
        turn_counter: int

        am_i_rich, am_i_broke, turn_counter = cash_flow_rat_race_simulate_game(
            a_profession=profession_dict[PROFESSION_TEST_NAME],
            a_strategy=strategy_dict[strategy_names[test % len(strategy_names)]],
            almost_empty_decks=(test == 0),
        )

        test_time: float = time.time() - start_time
        total_time += test_time

        logging.info(
            f"Test #: {test}"
            f"\n    Am I Rich: {am_i_rich}"
            f"\n    Am I Poor: {am_i_broke}"
            f"\n    No of Turns: {turn_counter}"
            f"\n    Time: {test_time} seconds\n"
        )
    logging.info(
        f"Total simulations run:   {NO_SIMS}"
        f"\nTotal simulations time:  {round(total_time,1)} seconds"
        f"\nAverage Simulation Time: {round(total_time/NO_SIMS, 3)} seconds"
    )


if __name__ == "__main__":
    test_cash_flow_rat_race_simulate_game()

# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:06:05 2022

@author: PaulJ
"""

import time
import random
import unittest
from cashflowsim.cash_flow_rat_race_simulate_game import (
    cash_flow_rat_race_simulate_game)

PROFESSIONS_FN = '../game_data/ProfessionsList.json'
STRATEGIES_FN = '../simulation_strategies/Strategies.json'
PROFESSION_TEST_NAME = 'Engineer'
STRATEGY_TEST_NAME = 'Standard Auto'
VERBOSE = False



class TestCashFlowRatRaceSimulateGame(unittest.TestCase):
    """Test Class to test Simulate a Game."""

    import profession
    import strategy


    def test_cash_flow_rat_race_simulate_game(self):
        for test in range(0, 500):
            start_time = time.time()
            random.seed(test)

            # Load list of professions and create empty list of players

            profession_dict = (
                TestCashFlowRatRaceSimulateGame.profession.get_profession_defs(
                PROFESSIONS_FN))

            # Create a player to test in manual mode/strategy
            strategy_dict = (
                TestCashFlowRatRaceSimulateGame.strategy.get_strategy_defs(
                STRATEGIES_FN))

            # Example settings to test

            am_i_rich, am_i_broke, turn_counter = (
                cash_flow_rat_race_simulate_game(
                    profession_dict[PROFESSION_TEST_NAME],
                    strategy_dict[STRATEGY_TEST_NAME],
                    VERBOSE))

            if VERBOSE:
                print('Test #:', test, '\n    Am I Rich:', am_i_rich,
                      '\n    Am I Poor:', am_i_broke, '\n    No of Turns:',
                      turn_counter, '\n        Time:', (time.time()-start_time),
                      'seconds\n')

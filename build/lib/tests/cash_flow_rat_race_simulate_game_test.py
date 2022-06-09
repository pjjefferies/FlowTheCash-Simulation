# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:06:05 2022

@author: PaulJ
"""

import time
import random
import unittest
from cash_flow_rat_race_simulate_game import cash_flow_rat_race_simulate_game

class TestCashFlowRatRaceSimulateGame(unittest.TestCase):
    """Test Class to test Simulate a Game."""
    for test in range(0, 500):
        start_time = time.time()
        random.seed(test)
        import profession
        import strategy

        # Load list of professions and create empty list of players

        profession_dict = profession.get_profession_defs(
            '../game_data/ProfessionsList.json')

        # Create a player to test in manual mode/strategy
        strategy_dict = strategy.get_strategy_defs(
            '../simulation_strategies/Strategies.json')

        # Example settings to test
        profession_name = 'Engineer'
        strategy_name = 'Standard Auto'
        verbose = False

        am_i_rich, am_i_broke, turn_counter = (
            cash_flow_rat_race_simulate_game(
                profession_dict[profession_name],
                strategy_dict[strategy_name],
                verbose))

        if verbose:
            print('Test #:', test, '\n    Am I Rich:', am_i_rich,
                  '\n    Am I Poor:', am_i_broke, '\n    No of Turns:',
                  turn_counter, '\n        Time:', (time.time()-start_time),
                  'seconds\n')

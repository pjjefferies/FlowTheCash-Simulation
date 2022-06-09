# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:57:35 2020

@author: PaulJ
"""

import unittest

PROFESSIONS_FN = '../game_data/ProfessionsList.json'
STRATEGIES_FN = '../simulation_strategies/Strategies.json'


class TestPlayer(unittest.TestCase):
    """Test Class to test Player objects in player module."""

    import cashflowsim.player as player
    import cashflowsim.profession as profession
    import cashflowsim.strategy as strategy


    PROFESSION_DEFS = profession.get_profession_defs(PROFESSIONS_FN)
    STRATEGY_DEFS = strategy.get_strategy_defs(STRATEGIES_FN)

    # Make Available Strategies to Test
    # tests = [{'

    def test_create_each_player_type(self):
        """General test using list of tests above."""
        list_of_player = []
        for a_profession in self.PROFESSION_DEFS:  # create player example for
            name = a_profession + ' Player'
            list_of_player.append(TestPlayer.player.Player(
                name,
                self.PROFESSION_DEFS[a_profession],
                self.STRATEGY_DEFS['Standard Auto']))
        for a_player in list_of_player:
            self.assertIsInstance(a_player, TestPlayer.player.Player)

    def test_earn_salary(self):
        a_player = TestPlayer.player.Player(
            'Player Name',
            self.PROFESSION_DEFS[list(self.PROFESSION_DEFS.keys())[0]],
            self.STRATEGY_DEFS['Standard Auto'])
        old_savings = a_player.savings
        monthly_cash_flow = a_player.monthly_cash_flow
        a_player.earn_salary()
        self.assertEqual(a_player.savings,
                         old_savings + monthly_cash_flow)

    def test_passive_income(self):
        a_player = TestPlayer.player.Player(
            'Player Name',
            self.PROFESSION_DEFS[list(self.PROFESSION_DEFS.keys())[0]],
            self.STRATEGY_DEFS['Standard Auto'])
        self.assertTrue(isinstance(a_player.passive_income, int))

    def test_monthly_cash_flow(self):
        a_player = TestPlayer.player.Player(
            'Player Name',
            self.PROFESSION_DEFS[list(self.PROFESSION_DEFS.keys())[0]],
            self.STRATEGY_DEFS['Standard Auto'])
        self.assertEqual(a_player.monthly_cash_flow,
                         a_player.total_income - a_player.total_expenses)

    def test_total_income(self):
        a_player = TestPlayer.player.Player(
            'Player Name',
            self.PROFESSION_DEFS[list(self.PROFESSION_DEFS.keys())[0]],
            self.STRATEGY_DEFS['Standard Auto'])
        self.assertEqual(a_player.total_income,
                         a_player.salary + a_player.passive_income)


if __name__ == '__main__':
    unittest.main(verbosity=2)

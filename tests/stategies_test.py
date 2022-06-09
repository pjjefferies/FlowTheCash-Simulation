# -*- coding: utf-8 -*-
"""
Created on Sun May  8 22:03:33 2022

@author: PaulJ
"""

import unittest

STRATEGIES_FN = '../simulation_strategies/Strategies.json'

class TestStrategies(unittest.TestCase):
    """Test Class to test Strategies objects in strategy module."""

    import cashflowsim.strategy as strategy

    STRATEGY_DEFS = strategy.get_strategy_defs(STRATEGIES_FN)

    def test_strategy_name(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].name, str)
                and bool(TestStrategies.STRATEGY_DEFS[a_strategy].name))

    def test_strategy_manual(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].manual, bool))

    def test_roi_threshold(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].roi_threshold, float))
            self.assertGreaterEqual(
                TestStrategies.STRATEGY_DEFS[a_strategy].roi_threshold, 0.0)
            self.assertLessEqual(
                TestStrategies.STRATEGY_DEFS[a_strategy].roi_threshold, 1.0)

    def test_price_ratio_threshold(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].price_ratio_threshold,
                float))
            self.assertGreaterEqual(
                TestStrategies.STRATEGY_DEFS[a_strategy].price_ratio_threshold,
                0.0)
            self.assertLessEqual(
                TestStrategies.STRATEGY_DEFS[a_strategy].price_ratio_threshold,
                1.0)

    def test_take_downpayment_loans(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].take_downpayment_loans,
                bool))

    def test_take_any_loans(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].take_any_loans, bool))

    def test_charitable(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].charitable, bool))

    def test_loan_payback(self):
        for a_strategy in TestStrategies.STRATEGY_DEFS:
            self.assertTrue(isinstance(
                TestStrategies.STRATEGY_DEFS[a_strategy].loan_payback, str))
            self.assertIn(
                TestStrategies.STRATEGY_DEFS[a_strategy].loan_payback,
                ["Smallest", "Largest", "Never", "Highest Interest"])


if __name__ == '__main__':
    unittest.main(verbosity=2)

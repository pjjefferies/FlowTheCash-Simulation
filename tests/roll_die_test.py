# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:48:03 2022

@author: PaulJ
"""
import statistics
import unittest

class TestDieRoll(unittest.TestCase):
    """Test Class to test Asset objects in assets module."""

    from cashflowsim.roll_die import roll_die

    def test_die_roll_100_auto_verbose(self):
        """Test 100 Automatic Die Rolls"""
        die_rolls = []
        print("\n100 Automatic Rolls in verbose mode")
        for _ in range(100):  # Try 100 automatic rolls in verbose
            die_result = TestDieRoll.roll_die(strategy="Automatic",
                                              no_of_dice=1,
                                              verbose=True)
            die_rolls.append(die_result)
        mean_die_roll = statistics.mean(die_rolls)
        std_dev_die_roll = statistics.stdev(die_rolls)
        print("For 100 Automatic Die Rolls: Mean =", str(mean_die_roll),
              "Std. Dev. =", str(std_dev_die_roll))


    def test_die_roll_100_auto_non_verbose(self):
        print("\n100 Automatic Rolls in non-verbose mode")
        die_rolls = []
        for _ in range(100):  # Try 100 automatic rolls in quiet
            die_result = TestDieRoll.roll_die(strategy="Automatic",
                                              no_of_dice=1,
                                              verbose=False)
            die_rolls.append(die_result)
        mean_die_roll = statistics.mean(die_rolls)
        std_dev_die_roll = statistics.stdev(die_rolls)
        print("For 100 Automatic Die Rolls: Mean =", str(mean_die_roll),
              "Std. Dev. =", str(std_dev_die_roll))

    def test_die_roll_5_manual_verbose(self):
        print("\n5 Manual Rolls in verbose mode")
        die_rolls = []
        for _ in range(5):
            die_result = TestDieRoll.roll_die(strategy="Manual",
                                              no_of_dice=1,
                                              verbose=True)
            die_rolls.append(die_result)
        mean_die_roll = statistics.mean(die_rolls)
        std_dev_die_roll = statistics.stdev(die_rolls)
        print("For 5 Manual Rolls of 2 Dice: Mean =", str(mean_die_roll),
              "Std. Dev. =", str(std_dev_die_roll))

    def test_die_roll_5_manual_non_verbose(self):
        print("\n5 Manual Rolls of two dice in non-verbose mode")
        die_rolls = []
        for _ in range(5):
            die_result = TestDieRoll.roll_die(strategy="Manual",
                                              no_of_dice=2,
                                              verbose=False)
            die_rolls.append(die_result)
        mean_die_roll = statistics.mean(die_rolls)
        std_dev_die_roll = statistics.stdev(die_rolls)
        print("For 5 Manual Rolls of 2 Dice: Mean =", str(mean_die_roll),
              "Std. Dev. =", str(std_dev_die_roll))


if __name__ == '__main__':
    unittest.main(verbosity=2)

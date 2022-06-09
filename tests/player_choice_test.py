# -*- coding: utf-8 -*-
"""
Created on Thu May  5 23:44:45 2022

@author: PaulJ
"""

PROFESSIONS_FN = '../game_data/ProfessionsList.json'
STRATEGIES_FN = '../simulation_strategies/Strategies.json'

import unittest


class TestAssets(unittest.TestCase):
    """Test Class to test Asset objects in assets module."""

    from cashflowsim import player_choice
    from cashflowsim import profession
    from cashflowsim import strategy
    from cashflowsim import player


    PROFESSION_DICT = profession.get_profession_defs(PROFESSIONS_FN)
    # Make Available Strategies to Test

    STRATEGY_DICT = strategy.get_strategy_defs(STRATEGIES_FN)

    ME = player.Player("PaulCool", PROFESSION_DICT["Engineer"],
                       STRATEGY_DICT["Standard Auto"])
    SHE = player.Player("LynnHot", PROFESSION_DICT["Doctor"],
                        STRATEGY_DICT["Standard Auto"])
    HER = player.Player("KatieCute", PROFESSION_DICT["Business Manager"],
                        STRATEGY_DICT["Dave Ramsey"])
    print(ME.strategy)
    print(SHE.strategy)
    print(player_choice.choose_small_or_big_deal_card(SHE, True))
    SHE.earn_salary()
    SHE.earn_salary()
    print(SHE.savings)
    print(player_choice.choose_small_or_big_deal_card(SHE, True))

    ME.make_payment(-50000)      # add some cash to test paying-off loans
    SHE.make_payment(-100000)
    HER.make_payment(-25000)
    print(ME.savings)
    print(SHE.savings)

    print("me loan payoff result:", player_choice.choose_to_pay_off_loan(ME,
                                                                         True))
    print("me loans remaining:", ME.loan_list)
    print("she loan payoff result:",
          player_choice.choose_to_pay_off_loan(SHE, True))
    print("she loans remaining:", SHE.loan_list)
    print("Kaie loan payoff result:",
          player_choice.choose_to_pay_off_loan(HER, True))
    print("Katie loans remaining:", HER.loan_list)

# -*- coding: utf-8 -*-
"""
Created on Sun May  8 23:52:26 2022

@author: PaulJ
"""

import unittest

class Test_board_space_action(unittest.TestCase):
    """Test Class to test board_space_action functions
    in board_space_action module."""

    import cashflowsim.board_space_action as board_space_action
    import cashflowsim.player_choice as player_choice
    import cashflowsim.board as board
    import cashflowsim.cards as cards
    import cashflowsim.player as player
    import cashflowsim.profession as profession
    import cashflowsim.strategy as strategy
    import cashflowsim.roll_die as roll_die
    import copy
    import sys
    import random

    BOARDSPACES_FN = '../game_data/RatRaceBoardSpaces.json'
    PROFESSIONS_FN = '../game_data/ProfessionsList.json'
    SMALLDEALCARDS_FN = '../game_data/SmallDealCards.json'
    BIGDEALCARDS_FN = '../game_data/BigDealCards.json'
    DOODADCARDS_FN = '../game_data/DoodadCards.json'
    MARKETCARDS_FN = '../game_data/MarketCards.json'
    PLAYER1_NAME = 'PaulCool'
    PLAYER1_PROF = 'Engineer'
    PLAYER2_NAME = 'YohanAmI'
    PLAYER2_PROF = 'Business Manager'

    random.seed(2)
    rat_race_board = board.load_board_spaces(BOARDSPACES_FN)

    small_deal_card_deck_master = cards.load_all_small_deal_cards(
        SMALLDEALCARDS_FN)
    big_deal_card_deck_master = cards.load_all_big_deal_cards(BIGDEALCARDS_FN)
    doodad_card_deck_master = cards.load_all_doodad_cards(DOODADCARDS_FN)
    market_card_deck_master = cards.load_all_market_cards(MARKETCARDS_FN)
    small_deal_card_deck = copy.copy(small_deal_card_deck_master)
    big_deal_card_deck = copy.copy(big_deal_card_deck_master)
    doodad_card_deck = copy.copy(doodad_card_deck_master)
    market_card_deck = copy.copy(market_card_deck_master)

    turn_history = []

    small_deal_card_deck.shuffle()
    big_deal_card_deck.shuffle()
    doodad_card_deck.shuffle()
    market_card_deck.shuffle()

    # Make Available Strategies to Test
    manual_strategy = strategy.Strategy(name="Manual", manual=True)
    standard_auto_strategy = strategy.Strategy(name="Standard Auto",
                                               manual=False)
    dave_ramsey_auto_atrategy = strategy.Strategy(name="Dave Ramsey",
                                                  manual=True,
                                                  roi_threshold=0.20,
                                                  price_ratio_threshold=0.5,
                                                  take_downpayment_loans=False,
                                                  take_any_loans=False)
    no_down_payment_loan_auto_strategy = strategy.Strategy(
        name="No Down Payment Loans",
        manual=True,
        roi_threshold=0.20,
        price_ratio_threshold=0.5,
        take_downpayment_loans=False,
        take_any_loans=True)
    profession_dict = profession.get_profession_defs(PROFESSIONS_FN)
    me = player.Player("Paulcool", profession_dict["Engineer"],
                       standard_auto_strategy)
    rat_race_board.add_player(me, 0)
    me_on_board = rat_race_board.next_player
    verbose = True
    verbose_loc = ""
    # verbose_loc = "test_logfile.txt"
    if verbose_loc != "":
        saveout = sys.stdout
        output_file = open(verbose_loc, 'w')
        sys.stdout = output_file
    turn = 0
    while True:
        turn += 1
        single_turn_detail = [turn]
        single_turn_detail.append(me_on_board[0].name)
        single_turn_detail.append(me_on_board[0].profession)
        single_turn_detail.append(me_on_board[0].strategy.name)
        single_turn_detail.append(me_on_board[0].salary)
        single_turn_detail.append(me_on_board[0].passive_income)
        single_turn_detail.append(me_on_board[0].taxes)
        single_turn_detail.append(me_on_board[0].expense_other)
        single_turn_detail.append(me_on_board[0].total_expenses)
        single_turn_detail.append(me_on_board[0].cost_per_child)
        single_turn_detail.append(me_on_board[0].savings)
        single_turn_detail.append(len(me_on_board[0].loan_list))
        single_turn_detail.append(len(me_on_board[0].sold_assets))
        single_turn_detail.append(me_on_board[0].no_children)
        single_turn_detail.append(me_on_board[0].monthly_cash_flow)
        single_turn_detail.append(len(me_on_board[0].stock_assets))
        single_turn_detail.append(len(me_on_board[0].real_estate_assets))
        single_turn_detail.append(len(me_on_board[0].business_assets))
        if verbose:
            print("\nSample Turn:", turn, str(me_on_board[0]))
        if me_on_board[0].charity_turns_remaining > 0:
            me_on_board[0].use_charity_turn()
            no_of_dice = player_choice.choose_no_die([1, 2],
                                                     me_on_board[0].strategy,
                                                     verbose)
        else:
            no_of_dice = 1
        single_turn_detail.append(no_of_dice)
        if me_on_board[0].skipped_turns_remaining > 0:
            if verbose:
                print("Using a layoff day, " +
                      str(me_on_board[0].skipped_turns_remaining) +
                      " turns remaining")
            me_on_board[0].use_layoff()
            single_turn_detail.append("Use Layoff")
            turn_history.append(single_turn_detail)
            continue
        a_die_roll = roll_die.roll_die(me_on_board[0].strategy, no_of_dice,
                                       verbose)
        single_turn_detail.append(a_die_roll)
        single_turn_detail.append(me_on_board[1])
        me_on_board[1], passed_paycheck, new_board_space = (
            rat_race_board.move_player_board_spaces(me_on_board, a_die_roll))
        single_turn_detail.append(me_on_board[1])
        single_turn_detail.append(passed_paycheck)
        single_turn_detail.append(new_board_space.board_space_type)
        if passed_paycheck:
            if verbose:
                print("Passed payday")
            me_on_board[0].earn_salary()
        board_space_action.board_space_action(me_on_board,
                                              new_board_space,
                                              verbose,
                                              small_deal_card_deck,
                                              big_deal_card_deck,
                                              doodad_card_deck,
                                              market_card_deck,
                                              rat_race_board)
        am_i_rich, am_i_broke = me.refresh()
        if am_i_rich:
            print("After", turn, "turns, Player", me.name,
                  "is rich and wins")
            print(me)
            print("Sold Assets\n\n", me.sold_assets)
            break
        elif am_i_broke:
            print("After", turn, "turns, Player", me.name,
                  "is broke and looses")
            print(me)
            print("Sold Assets\n\n", me.sold_assets)
            break

        if doodad_card_deck.no_cards == 0:
            if verbose:
                print("At the bottom of Doodad Deck, shuffling...")
            doodad_card_deck = copy.copy(doodad_card_deck_master)
            doodad_card_deck.shuffle()
            if verbose:
                print("After shuffling, cards now in Doodad Deck:",
                      doodad_card_deck.no_cards)
        elif small_deal_card_deck.no_cards == 0:
            if verbose:
                print("At the bottom of Small Deal Deck, shuffling...")
            small_deal_card_deck = copy.copy(small_deal_card_deck_master)
            small_deal_card_deck.shuffle()
            if verbose:
                print("After shuffling, cards now in Small Deal Deck:",
                      small_deal_card_deck.no_cards)
        elif big_deal_card_deck.no_cards == 0:
            if verbose:
                print("At the bottom of Big Deal Deck, shuffling...")
            big_deal_card_deck = copy.copy(big_deal_card_deck_master)
            big_deal_card_deck.shuffle()
            if verbose:
                print("After shuffling, cards now in Big Deal Deck:",
                      big_deal_card_deck.no_cards)
        elif market_card_deck.no_cards == 0:
            if verbose:
                print("At the bottom of Market Deck, shuffling...")
            market_card_deck = copy.copy(market_card_deck_master)
            market_card_deck.shuffle()
            if verbose:
                print("After shuffling, cards now in Market Deck:",
                      market_card_deck.no_cards)
        turn_history.append(single_turn_detail)
    single_turn_detail = [turn]
    single_turn_detail.append(me_on_board[0].name)
    single_turn_detail.append(me_on_board[0].profession)
    single_turn_detail.append(me_on_board[0].strategy.name)
    single_turn_detail.append(me_on_board[0].salary)
    single_turn_detail.append(me_on_board[0].passive_income)
    single_turn_detail.append(me_on_board[0].taxes)
    single_turn_detail.append(me_on_board[0].expense_other)
    single_turn_detail.append(me_on_board[0].total_expenses)
    single_turn_detail.append(me_on_board[0].cost_per_child)
    single_turn_detail.append(me_on_board[0].savings)
    single_turn_detail.append(len(me_on_board[0].loan_list))
    single_turn_detail.append(len(me_on_board[0].sold_assets))
    single_turn_detail.append(me_on_board[0].no_children)
    single_turn_detail.append(me_on_board[0].monthly_cash_flow)
    single_turn_detail.append(len(me_on_board[0].stock_assets))
    single_turn_detail.append(len(me_on_board[0].real_estate_assets))
    single_turn_detail.append(len(me_on_board[0].business_assets))
    single_turn_detail.append(no_of_dice)
    single_turn_detail.append(roll_die)
    single_turn_detail.append(me_on_board[1])
    single_turn_detail.append(me_on_board[1])
    single_turn_detail.append(passed_paycheck)
    single_turn_detail.append(new_board_space.board_space_type)
    turn_history.append(single_turn_detail)
    turn_history.append("End of simulation")

    print("Entries in Turn Detail List", len(turn_history), "\n",
          turn_history[:5], "\n", turn_history[-5:])
    if verbose_loc != "":
        sys.stdout = saveout
        output_file.close()

    import csv
    import datetime
    oneGameFileLogFilename = ("GameLog-" +
                              datetime.datetime.now().strftime(
                                  "%Y%m%d-%H%M%S") + ".csv")
    with open(oneGameFileLogFilename, "w") as output_file:
        writer = csv.writer(output_file, delimiter=",")
        writer.writerow(["Turn", "Player Name", "Profession", "Strategy",
                         "Salary", "Passive Income", "Taxes", "Other Expenses",
                         "Total Expenses", "Child Cost", "Savings", "Loans",
                         "Sold Assets", "No. Children", "Cashflow",
                         "Stock Assets", "Real Estate Assets",
                         "Business Assets", "No. Dice", "Die Roll",
                         "Board Space No. Before", "Board Space No. After",
                         "Passed Paycheck", "Board Space After"])
        for turn in turn_history:
            writer.writerow(turn)
        output_file.close()
"""Main module for running Cash Flow Rat Race Simulation."""

import board
import cards
import player
import player_choice
import die_roll
import board_space_action
import random
import copy
import time


def cash_flow_rat_race_game_simulation(a_profession,
                                       a_strategy,
                                       verbose=False):
    """Initiate Cash Flow Rat Race Simulation."""
    # Create Rat Race Board
    rat_race_board = board.load_board_spaces('RatRaceBoardSpaces.json')

    # Create 4 Card Decks - not used except as starting points
    small_deal_card_deck_master = cards.load_all_small_deal_cards(
        'SmallDealCards.json')
    big_deal_card_deck_master = cards.load_all_big_deal_cards(
        'BigDealCards.json')
    doodad_card_deckMaster = cards.load_all_doodad_cards('DoodadCards.json')
    market_card_deck_master = cards.load_all_market_cards('MarketCards.json')

    # Start Main Loop, initiate decks to be used, shuffle and
    # create turn counter

    small_deal_card_deck = copy.copy(small_deal_card_deck_master)
    big_deal_card_deck = copy.copy(big_deal_card_deck_master)
    doodad_card_deck = copy.copy(doodad_card_deckMaster)
    market_card_deck = copy.copy(market_card_deck_master)

    small_deal_card_deck.shuffle()
    big_deal_card_deck.shuffle()
    doodad_card_deck.shuffle()
    market_card_deck.shuffle()

    # Create player and add to Board, starting at space 0
    player_name = a_profession.name + '_Player'
    a_player = player.Player(player_name, a_profession, a_strategy)
    rat_race_board.add_player(a_player, 0)

    turn_counter = 0
    while True:
        turn_counter += 1
        player_on_board = rat_race_board.next_player
        am_i_rich, am_i_broke = player_on_board[0].refresh()
        if verbose:
            print('After first refresh')
            print(a_player)
        if verbose:
            print(player_on_board[0].name, ', Turn:', turn_counter)

        # Offer to allow pay-off any loans pre-roll
        if player_choice.choose_to_pay_off_loan(player_on_board[0]):
            am_i_rich, am_i_broke = player_on_board[0].refresh()
            if am_i_rich:
                print('After', turn_counter, 'turns, Player',
                      player_on_board[0].name, 'is rich and wins')
                print('Passive income:',
                      player_on_board[0].passive_income,
                      '\nExpenses      :',
                      player_on_board[0].total_expenses)
                print(player_on_board[0])
                print('Sold Assets\n\n', player_on_board[0].sold_assets)
                break
            elif am_i_broke:
                print('Player', player_on_board[0].name,
                      'is broke and looses')
                break  # Replace with remove player later for multiple player

        # If have charity, roll 1 or 2 dice, otherwise, roll 1
        if player_on_board[0].charity_turns_remaining > 0:
            player_on_board[0].use_charity_turn()
            no_of_dice = player_choice.choose_no_die(
                [1, 2], player_on_board[0].strategy, verbose)
        else:
            no_of_dice = 1

        # If layed-off, skip turn
        if player_on_board[0].skipped_turns_remaining > 0:
            if verbose:
                print('Using a layoff day, ' + str(
                    player_on_board[0].skipped_turns_remaining) +
                    ' turns remaining')
            player_on_board[0].use_layoff()
            continue

        # Roll the die
        a_die_roll = die_roll.roll_die(player_on_board[0].strategy,
                                       no_of_dice,
                                       verbose)

        # Move based on dice roll
        player_on_board[1], passed_paycheck, new_board_space = (
            rat_race_board.move_player_board_spaces(player_on_board,
                                                    a_die_roll))

        # If passed paycheck, show me the money
        if passed_paycheck:
            player_on_board[0].earn_salary()

        # Take action based on board space
        board_space_action.board_space_action(
            player_on_board, new_board_space, verbose,
            small_deal_card_deck, big_deal_card_deck, doodad_card_deck,
            market_card_deck, rat_race_board)

        am_i_rich, am_i_broke = player_on_board[0].refresh()
        if am_i_rich:
            if verbose:
                print('After', turn_counter, 'turns, Player',
                      player_on_board[0].name, 'is rich and wins')
                print('Passive income:',
                      player_on_board[0].passive_income,
                      '\nExpenses      :',
                      player_on_board[0].total_expenses)
                print(player_on_board[0])
                print('Sold Assets\n\n', player_on_board[0].sold_assets)
            break
        elif am_i_broke:
            if verbose:
                print('After', turn_counter, 'turns, Player',
                      player_on_board[0].name, 'is broke and looses')
                print(player_on_board[0])
                print('Sold Assets\n\n', player_on_board[0].sold_assets)
            break

        # Offer to allow pay-off any loans post-roll
        if player_choice.choose_to_pay_off_loan(player_on_board[0], verbose):
            am_i_rich, am_i_broke = player_on_board[0].refresh()
            if am_i_rich:
                if verbose:
                    print('After', turn_counter, 'turns, Player',
                          player_on_board[0].name, 'is rich and wins')
                    print('Passive income:',
                          player_on_board[0].passive_income,
                          '\nExpenses      :',
                          player_on_board[0].total_expenses)
                    print(player_on_board[0])
                    print('Sold Assets\n\n',
                          player_on_board[0].sold_assets)
                break
            elif am_i_broke:
                if verbose:
                    print('Player', player_on_board[0].get_name,
                          'is broke and looses')
                break  # Replace with remove player later for multiple player

        # Check if any card decks need to be shuffled
        if verbose:
            print('Entering check if any card decks need to be shuffled')
        if doodad_card_deck.no_cards == 0:
            if verbose:
                print('At the bottom of Doodad Deck, shuffling...')
            doodad_card_deck = copy.copy(doodad_card_deckMaster)
            doodad_card_deck.shuffle()
            if verbose:
                print('After shuffling, cards now in Doodad Deck:',
                      doodad_card_deck.no_cards)
        elif small_deal_card_deck.no_cards == 0:
            if verbose:
                print('At the bottom of Small Deal Deck, shuffling...')
            small_deal_card_deck = copy.copy(small_deal_card_deck_master)
            small_deal_card_deck.shuffle()
            if verbose:
                print('After shuffling, cards now in Small Deal Deck:',
                      small_deal_card_deck.no_cards)
        elif big_deal_card_deck.no_cards == 0:
            if verbose:
                print('At the bottom of Big Deal Deck, shuffling...')
            big_deal_card_deck = copy.copy(big_deal_card_deck_master)
            big_deal_card_deck.shuffle()
            if verbose:
                print('After shuffling, cards now in Big Deal Deck:',
                      big_deal_card_deck.no_cards)
        elif market_card_deck.no_cards == 0:
            if verbose:
                print('At the bottom of Market Deck, shuffling...')
            market_card_deck = copy.copy(market_card_deck_master)
            market_card_deck.shuffle()
            if verbose:
                print('After shuffling, cards now in Market Deck:',
                      market_card_deck.no_cards)

        # End of Game Play Loop
    return am_i_rich, am_i_broke, turn_counter


if __name__ == '__main__':
    for test in range(0, 500):
        start_time = time.time()
        random.seed(test)
        import profession
        import strategy

        # Load list of professions and create empty list of players

        profession_dict = profession.get_profession_defs(
            'ProfessionsList.json')

        # Create a player to test in manual mode/strategy
        strategy_dict = strategy.get_strategy_defs('Strategies.json')

        # Example settings to test
        profession_name = 'Engineer'
        strategy_name = 'Standard Auto'
        verbose = False

        am_i_rich, am_i_broke, turn_counter = (
            cash_flow_rat_race_game_simulation(
                profession_dict[profession_name],
                strategy_dict[strategy_name],
                verbose))

        if verbose:
            print('Test #:', test, '\n    Am I Rich:', am_i_rich,
                  '\n    Am I Poor:', am_i_broke, '\n    No of Turns:',
                  turn_counter, '\n        Time:', (time.time()-start_time),
                  'seconds\n')

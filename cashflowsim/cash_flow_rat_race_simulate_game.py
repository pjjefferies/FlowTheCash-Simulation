"""Main module for running Cash Flow Rat Race Simulation."""

from os.path import join, abspath
from inspect import getsourcefile
from copy import deepcopy
import logging


from cashflowsim.board import Board, BoardSpace, load_board_spaces
from cashflowsim.cards import (
    CardDeck,
    load_all_big_deal_cards,
    load_all_small_deal_cards,
    load_all_market_cards,
    load_all_doodad_cards,
)
from cashflowsim.player import Player
from cashflowsim.profession import Profession
from cashflowsim.strategy import Strategy
from cashflowsim.player_choice import (
    choose_to_pay_off_loan,
    choose_no_die,
)
from cashflowsim.roll_die import roll_die
from cashflowsim.board_space_action import board_space_action


# import time
APP_DIR: str = "cashflowsim"
LOG_DIR: str = "game_logs"
GAME_DATA_DIR: str = "game_data"
STRATEGIES_DIR: str = "simulation_strategies"

# STRATEGIES_FN: str = "Strategies.json"
# PROFESSIONS_FN: str = "ProfessionsList.json"
BOARD_FN: str = "RatRaceBoardSpaces.json"
SMALL_DEAL_CARDS_FN: str = "SmallDealCards.json"
BIG_DEAL_CARDS_FN: str = "BigDealCards.json"
DOODAD_CARDS_FN: str = "DoodadCards.json"
MARKET_CARDS_FN: str = "MarketCards.json"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])

game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)

board_path_fn: str = join(game_data_path, BOARD_FN)
small_deal_card_deck_path_fn: str = join(game_data_path, SMALL_DEAL_CARDS_FN)
big_deal_card_deck_path_fn: str = join(game_data_path, BIG_DEAL_CARDS_FN)
doodad_card_deck_path_fn: str = join(game_data_path, DOODAD_CARDS_FN)
market_card_path_fn: str = join(game_data_path, MARKET_CARDS_FN)

log: logging.Logger = logging.getLogger(__name__)


def cash_flow_rat_race_simulate_game(
    *,
    a_profession: Profession,
    a_strategy: Strategy,
    almost_empty_decks: bool = False,
) -> tuple[bool, bool, int]:
    """Initiate Cash Flow Rat Race Simulation.
    amost_empty_decks added for testing purposes to ensure shuffle for all deck types accessed"""
    # Create Rat Race Board
    rat_race_board: Board = load_board_spaces(board_spaces_filename=board_path_fn)

    # Create 4 Card Decks - not used except as starting points
    small_deal_card_deck_master: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_card_deck_path_fn
    )
    big_deal_card_deck_master: CardDeck = load_all_big_deal_cards(
        big_deal_cards_filename=big_deal_card_deck_path_fn
    )
    doodad_card_deckMaster: CardDeck = load_all_doodad_cards(
        doodad_cards_filename=doodad_card_deck_path_fn
    )
    market_card_deck_master: CardDeck = load_all_market_cards(
        market_cards_filename=market_card_path_fn
    )

    # Start Main Loop, initiate decks to be used, shuffle and
    # create turn counter

    small_deal_card_deck = deepcopy(small_deal_card_deck_master)
    big_deal_card_deck = deepcopy(big_deal_card_deck_master)
    doodad_card_deck = deepcopy(doodad_card_deckMaster)
    market_card_deck = deepcopy(market_card_deck_master)

    small_deal_card_deck.shuffle()
    big_deal_card_deck.shuffle()
    doodad_card_deck.shuffle()
    market_card_deck.shuffle()

    if almost_empty_decks:
        small_deal_card_deck.cards = small_deal_card_deck.cards[0:1]
        big_deal_card_deck.cards = big_deal_card_deck.cards[0:1]
        doodad_card_deck.cards = doodad_card_deck.cards[0:1]
        market_card_deck.cards = market_card_deck.cards[0:1]

    # Create player and add to Board, starting at space 0
    player_name: str = "_".join([a_profession.name, "Player"])
    a_player: Player = Player(
        name=player_name, profession=a_profession, strategy=a_strategy
    )
    rat_race_board.add_player(a_player=a_player, board_space=0)

    turn_counter: int = 0
    passed_paycheck: bool
    new_board_space: BoardSpace
    am_i_rich: bool
    am_i_broke: bool

    while True:
        turn_counter += 1
        player_on_board: Player = rat_race_board.next_player

        am_i_rich, am_i_broke = player_on_board.refresh()
        log.info(f"At beginning of turn: {turn_counter}")
        log.info(f"player_on_board:\n{player_on_board.name}")

        # Offer to allow pay-off any loans pre-roll
        choose_to_pay_off_loan(a_player=player_on_board)

        # If layed-off, skip turn
        if player_on_board.skipped_turns_remaining > 0:
            log.info(
                f"Using a layoff day, {player_on_board.skipped_turns_remaining} turns remaining"
            )
            player_on_board.use_layoff()
            continue

        # If have charity, roll 1 or 2 dice, otherwise, roll 1
        if player_on_board.charity_turns_remaining > 0:
            player_on_board.use_charity_turn()
            no_of_dice: int = choose_no_die(
                no_die_choice_list=[1, 2],
                a_strategy=player_on_board.strategy,
            )
        else:
            no_of_dice = 1

        # Roll the die
        a_die_roll: int = roll_die(strategy="Automatic", no_of_dice=no_of_dice)

        # Move based on dice roll
        (
            _,
            passed_paycheck,
            new_board_space,
        ) = rat_race_board.move_player_board_spaces(
            a_player=player_on_board, move_spaces=a_die_roll
        )

        # If passed paycheck, show me the money
        if passed_paycheck:
            player_on_board.earn_salary()

        # Take action based on board space
        board_space_action(
            player=player_on_board,
            new_board_space=new_board_space,
            small_deal_card_deck=small_deal_card_deck,
            big_deal_card_deck=big_deal_card_deck,
            doodad_card_deck=doodad_card_deck,
            market_card_deck=market_card_deck,
            board=rat_race_board,
        )

        am_i_rich, am_i_broke = player_on_board.refresh()
        if am_i_rich:
            log.info(
                f"After {turn_counter} turns, Player {player_on_board.name} is rich and wins"
                f"\nPassive income: {player_on_board.passive_income}"
                f"\nExpenses      : {player_on_board.total_expenses}"
                f"\n{player_on_board}"
                f"\nSold Assets\n\n{player_on_board.sold_assets}"
            )
            break
        if am_i_broke:
            log.info(
                f"After {turn_counter} turns, Player {player_on_board.name} is broke and loses"
                f"\n{player_on_board}"
                f"\nSold Assets\n\n{player_on_board.sold_assets}"
            )
            break

        # Check if any card decks need to be shuffled
        log.info("Entering check if any card decks need to be shuffled")
        log.info(f"Doodad Card Deck has {doodad_card_deck.no_cards} cards left.")
        if doodad_card_deck.no_cards == 0:
            log.info(f"At the bottom of Doodad Deck, shuffling...")
            doodad_card_deck = deepcopy(doodad_card_deckMaster)
            doodad_card_deck.shuffle()
            log.info(
                f"After shuffling, cards now in Doodad Deck: {doodad_card_deck.no_cards}"
            )
        log.info(
            f"Small Deal Card Deck has {small_deal_card_deck.no_cards} cards left."
        )
        if small_deal_card_deck.no_cards == 0:
            log.info("At the bottom of Small Deal Deck, shuffling...")
            small_deal_card_deck = deepcopy(small_deal_card_deck_master)
            small_deal_card_deck.shuffle()
            log.info(
                f"After shuffling, cards now in Small Deal Deck: {small_deal_card_deck.no_cards}"
            )
        log.info(f"Big Deal Card Deck has {big_deal_card_deck.no_cards} cards left.")
        if big_deal_card_deck.no_cards == 0:
            log.info(f"At the bottom of Big Deal Deck, shuffling...")
            big_deal_card_deck = deepcopy(big_deal_card_deck_master)
            big_deal_card_deck.shuffle()
            log.info(
                f"After shuffling, cards now in Big Deal Deck: {big_deal_card_deck.no_cards}"
            )
        log.info(f"Market Card Deck has {market_card_deck.no_cards} cards left.")
        if market_card_deck.no_cards == 0:
            log.info(f"At the bottom of Market Deck, shuffling...")
            market_card_deck = deepcopy(market_card_deck_master)
            market_card_deck.shuffle()
            log.info(
                f"After shuffling, cards now in Market Deck: {market_card_deck.no_cards}"
            )

        # End of Game Play Loop
    return am_i_rich, am_i_broke, turn_counter

# -*- coding: utf-8 -*-
"""
Created on Sun May  8 23:52:26 2022

@author: PaulJ
"""

from __future__ import annotations
import datetime as dt
import logging
from os.path import join, abspath
from inspect import getsourcefile

from typing import Any

import pytest
import cashflowsim.board_space_action as cfs_board_space_action

# import cashflowsim.player_choice as cfs_player_choice
import cashflowsim.board as cfs_board
import cashflowsim.cards as cfs_cards
import cashflowsim.player as cfs_player
import cashflowsim.profession as cfs_profession
import cashflowsim.strategy as cfs_strategy

# import cashflowsim.roll_die as cfs_roll_die
from copy import deepcopy
from random import seed

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
LOG_DIR: str = "game_logs"

SMALLDEALCARDS_FN: str = "SmallDealCards.json"
BIGDEALCARDS_FN: str = "BigDealCards.json"
DOODADCARDS_FN: str = "DoodadCards.json"
MARKETCARDS_FN: str = "MarketCards.json"
STRATEGIES_DIR: str = "simulation_strategies"
STRATEGIES_FN: str = "strategies.json"
BOARDSPACES_FN: str = "RatRaceBoardSpaces.json"
PROFESSIONS_FN: str = "ProfessionsList.json"

PLAYER1_NAME: str = "Player1"
PLAYER1_PROF: str = "Engineer"
PLAYER1_STRATEGY: str = "Dave Ramsey"
PLAYER2_NAME: str = "Player2"
PLAYER2_PROF: str = "Business Manager"
PLAYER2_STRATEGY: str = "Standard Auto"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)
profession_data_path_fn: str = join(game_data_path, PROFESSIONS_FN)
strategies_data_path: str = join(base_path, APP_DIR, STRATEGIES_DIR)
strategies_data_path_fn: str = join(strategies_data_path, STRATEGIES_FN)
boardspaces_path_fn: str = join(game_data_path, BOARDSPACES_FN)
small_deal_card_deck_path_fn: str = join(game_data_path, SMALLDEALCARDS_FN)
big_deal_card_deck_path_fn: str = join(game_data_path, BIGDEALCARDS_FN)
doodad_card_deck_path_fn: str = join(game_data_path, DOODADCARDS_FN)
market_card_deck_path_fn: str = join(game_data_path, MARKETCARDS_FN)

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


seed(2)


@pytest.fixture
def rat_race_board() -> cfs_board.Board:
    return cfs_board.load_board_spaces(board_spaces_filename=boardspaces_path_fn)


small_deal_card_deck_master: cfs_cards.CardDeck = cfs_cards.load_all_small_deal_cards(
    small_deal_cards_filename=small_deal_card_deck_path_fn
)


@pytest.fixture
def small_deal_card_deck() -> cfs_cards.CardDeck:
    return deepcopy(small_deal_card_deck_master)


big_deal_card_deck_master: cfs_cards.CardDeck = cfs_cards.load_all_big_deal_cards(
    big_deal_cards_filename=big_deal_card_deck_path_fn
)


@pytest.fixture
def big_deal_card_deck() -> cfs_cards.CardDeck:
    return deepcopy(big_deal_card_deck_master)


doodad_card_deck_master: cfs_cards.CardDeck = cfs_cards.load_all_doodad_cards(
    doodad_cards_filename=doodad_card_deck_path_fn
)


@pytest.fixture
def doodad_card_deck() -> cfs_cards.CardDeck:
    return deepcopy(doodad_card_deck_master)


market_card_deck_master: cfs_cards.CardDeck = cfs_cards.load_all_market_cards(
    market_cards_filename=market_card_deck_path_fn
)


@pytest.fixture
def market_card_deck() -> cfs_cards.CardDeck:
    return deepcopy(market_card_deck_master)


turn_history: list[list[Any]] = []

PROFESSION_DEFS: dict[
    str, cfs_profession.Profession
] = cfs_profession.get_profession_defs(profession_data_path_fn)
STRATEGY_DEFS: dict[str, cfs_strategy.Strategy] = cfs_strategy.get_strategy_defs(
    strategy_defs_fn=strategies_data_path_fn
)


def test_board_space_action_one_time_around_board(
    rat_race_board: cfs_board.Board,
    small_deal_card_deck: cfs_cards.CardDeck,
    big_deal_card_deck: cfs_cards.CardDeck,
    doodad_card_deck: cfs_cards.CardDeck,
    market_card_deck: cfs_cards.CardDeck,
) -> None:
    player1 = cfs_player.Player(
        name=PLAYER1_NAME,
        profession=PROFESSION_DEFS[PLAYER1_PROF],
        strategy=STRATEGY_DEFS[PLAYER1_STRATEGY],
    )
    rat_race_board.add_player(a_player=player1, board_space=0)
    player1_on_board: cfs_player.Player = rat_race_board.next_player

    logging.info(f"Player: {player1_on_board.name}")
    logging.info(f"Profession: {player1_on_board.profession}")
    logging.info(f"Strategy: {player1_on_board.strategy.name}")
    logging.info(f"Salary: {player1_on_board.salary}")
    logging.info(f"Cost per child: {player1_on_board.cost_per_child}")

    for a_boardspace in rat_race_board.board_spaces:
        logging.info(f"\n\nBoardspace name: {a_boardspace.board_space_type}")
        logging.info(f"Passive income: {player1_on_board.passive_income}")
        logging.info(f"Other expenses: {player1_on_board.expense_other}")
        logging.info(f"Total expenses: {player1_on_board.total_expenses}")
        logging.info(f"Savings: {player1_on_board.savings}")
        logging.info(f"No. Loans: {len(player1_on_board.loan_list)}")
        logging.info(f"No. Sold Assets: {len(player1_on_board.sold_assets)}")
        logging.info(f"No. children: {player1_on_board.no_children}")
        logging.info(f"Cash flow: {player1_on_board.monthly_cash_flow}")
        logging.info(f"No. Stocks: {len(player1_on_board.stock_assets)}")
        logging.info(f"No. Real Estates: {len(player1_on_board.real_estate_assets)}")
        logging.info(f"No. Businesses: {len(player1_on_board.business_assets)}")

        if player1_on_board.charity_turns_remaining > 0:
            logging.info(
                f"Using charity turn. {player1_on_board.charity_turns_remaining} charity turns remaining."
            )
            player1_on_board.use_charity_turn()

        if player1_on_board.skipped_turns_remaining > 0:
            logging.info(
                f"Using a layoff day, {player1_on_board.skipped_turns_remaining} turns remaining"
            )
            player1_on_board.use_layoff()
            logging.info(f"Use Layoff")

        if a_boardspace.board_space_type == "Pay Check":
            logging.info("Passed payday")
            player1_on_board.earn_salary()

        cfs_board_space_action.board_space_action(
            player=player1_on_board,
            new_board_space=a_boardspace,
            small_deal_card_deck=small_deal_card_deck,
            big_deal_card_deck=big_deal_card_deck,
            doodad_card_deck=doodad_card_deck,
            market_card_deck=market_card_deck,
            board=rat_race_board,
        )
        am_i_rich, am_i_broke = player1_on_board.refresh()
        if am_i_rich:
            logging.info(
                "\n".join(
                    [
                        f"Player {player1_on_board.name} is rich and wins",
                        f"Sold Assets\n\n{player1_on_board.sold_assets}",
                    ]
                )
            )
            break
        elif am_i_broke:
            logging.info(
                "\n".join(
                    [
                        f"Player {player1_on_board.name} is broke and looses",
                        f"{player1_on_board}",
                        f"Sold Assets\n\n{player1_on_board.sold_assets}",
                    ]
                )
            )
            break

        if doodad_card_deck.no_cards == 0:
            logging.info("At the bottom of Doodad Deck, shuffling...")
            doodad_card_deck = deepcopy(doodad_card_deck_master)
            doodad_card_deck.shuffle()
            logging.info(
                f"After shuffling, {doodad_card_deck.no_cards} cards now in Doodad Deck:"
            )
        elif small_deal_card_deck.no_cards == 0:
            logging.info("At the bottom of Small Deal Deck, shuffling...")
            small_deal_card_deck = deepcopy(small_deal_card_deck_master)
            small_deal_card_deck.shuffle()
            logging.info(
                f"After shuffling, {small_deal_card_deck.no_cards} cards now in Small Deal Deck:"
            )
        elif big_deal_card_deck.no_cards == 0:
            logging.info("At the bottom of Big Deal Deck, shuffling...")
            big_deal_card_deck = deepcopy(big_deal_card_deck_master)
            big_deal_card_deck.shuffle()
            logging.info(
                f"After shuffling, {big_deal_card_deck.no_cards} cards now in Big Deal Deck:"
            )
        elif market_card_deck.no_cards == 0:
            logging.info("At the bottom of Market Deck, shuffling...")
            market_card_deck = deepcopy(market_card_deck_master)
            market_card_deck.shuffle()
            logging.info(
                f"After shuffling, {market_card_deck.no_cards} cards now in Market Deck:"
            )
    logging.info("End of simulation")


def test_board_space_action_bad_board_space(
    rat_race_board: cfs_board.Board,
    small_deal_card_deck: cfs_cards.CardDeck,
    big_deal_card_deck: cfs_cards.CardDeck,
    doodad_card_deck: cfs_cards.CardDeck,
    market_card_deck: cfs_cards.CardDeck,
) -> None:

    player1 = cfs_player.Player(
        name=PLAYER1_NAME,
        profession=PROFESSION_DEFS[PLAYER1_PROF],
        strategy=STRATEGY_DEFS[PLAYER1_STRATEGY],
    )
    rat_race_board.add_player(a_player=player1, board_space=0)
    player1_on_board: cfs_player.Player = rat_race_board.next_player

    a_boardspace = cfs_board.BoardSpace(
        board_space_type="On the Moon", description="Seeking the Cheese that is Green"
    )

    try:
        cfs_board_space_action.board_space_action(
            player=player1_on_board,
            new_board_space=a_boardspace,
            small_deal_card_deck=small_deal_card_deck,
            big_deal_card_deck=big_deal_card_deck,
            doodad_card_deck=doodad_card_deck,
            market_card_deck=market_card_deck,
            board=rat_race_board,
        )
    except ValueError:
        logging.info(f"Correctly detected incorrect board space")
        return

    raise ValueError(f"Incorrectly did not detect incorrect board space")


def test_board_space_action_small_business_improves(
    rat_race_board: cfs_board.Board,
) -> None:

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 5_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Start a Company Part Time",
        card_type="StartCompany",
        price=3_000,
        down_payment=3_000,
        cash_flow=0,
        price_range_high=10_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Rare Silver Coin",
        card_type="Asset",
        price=500,
        down_payment=500,
        cash_flow=0,
        price_range_high=4_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=b_card, board=rat_race_board
    )

    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Small Business Improves",
        increased_cash_flow=250,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert player2.business_assets[0].cash_flow == 250


def test_board_space_action_keep_sell_condo(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_condo_keep_condo")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 5_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Condo For Sale - 2Br/1Ba",
        card_type="HouseForSale",
        house_or_condo="Condo",
        price=40_000,
        down_payment=4_000,
        cash_flow=140,
        price_range_high=65_000,
        price_range_low=45_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    logging.info(
        f"Player2 Real Estate Assets After Buying Condo, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Condo Buyer - 2Br/1Ba",
        house_or_condo="Condo",
        price=15000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 1

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Condo Buyer - 2Br/1Ba",
        house_or_condo="Condo",
        price=45000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 0


def test_board_space_action_keep_sell_shopping_mall(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_keep_shopping_mall")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 65_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Small Shopping Mall for Sale",
        card_type="Business",
        price=50_000,
        down_payment=50_000,
        cash_flow=800,
        price_range_high=150_000,
        price_range_low=35_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    a1_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Automated Business for Sale",
        card_type="Business",
        price=100_000,
        down_payment=20_000,
        cash_flow=1600,
        price_range_high=100_000,
        price_range_low=100_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a1_card)

    logging.info(
        f"Player2 Business Assets After Buying Shopping Mall+, before Market Action:"
        f"\n{player2.business_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Shopping Mall Wanted",
        price=10_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 2

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Shopping Mall Wanted",
        price=100_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 1


def test_board_space_action_keep_sell_20_acres(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_condo_keep_20_acres")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 20_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="20 Acres for Sale",
        card_type="Land",
        price=20_000,
        down_payment=20_000,
        cash_flow=0,
        price_range_low=0,
        price_range_high=100_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(
        f"Player2 Real Estate Assets After Buying 20 Acres, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Buyer for 20 Acres",
        price=15_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 1

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Buyer for 20 Acres",
        price=100_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 0


def test_board_space_action_keep_sell_rare_gold_coin(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_keep_rare_gold_coin")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 65_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Rare Gold Coin",
        card_type="Asset",
        price=500,
        down_payment=500,
        cash_flow=0,
        price_range_low=0,
        price_range_high=4_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    a1_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Automated Business for Sale",
        card_type="Business",
        price=100_000,
        down_payment=20_000,
        cash_flow=1600,
        price_range_high=100_000,
        price_range_low=100_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a1_card)

    logging.info(
        f"Player2 Business Assets After Buying Gold Coin+, before Market Action:"
        f"\n{player2.business_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Price of Gold Soars",
        price=490,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 2

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Price of Gold Soars",
        price=600,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 1


def test_board_space_action_not_buy_buy_keep_sell_car_wash(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(
        f"\n\n\nStarting: test_board_space_action_not_buy_buy_sell_keep_car_wash"
    )

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 65_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Car Wash for Sale",
        card_type="Business",
        price=450_000,
        down_payment=50_000,
        cash_flow=200,
        price_range_low=216_000,
        price_range_high=450_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 0

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Car Wash for Sale",
        card_type="Business",
        price=350_000,
        down_payment=50_000,
        cash_flow=1_500,
        price_range_low=216_000,
        price_range_high=450_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    a1_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Automated Business for Sale",
        card_type="Business",
        price=100_000,
        down_payment=20_000,
        cash_flow=1600,
        price_range_high=100_000,
        price_range_low=100_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a1_card)

    logging.info(
        f"Player2 Business Assets After Buying Car Wash+, before Market Action:"
        f"\n{player2.business_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Car Wash Buyer",
        price=225_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 2

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Car Wash Buyer",
        price=450_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 1


def test_board_space_action_keep_sell_software_co(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_keep_software_co")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 65_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Start a Company Part Time",
        card_type="StartCompany",
        price=3_000,
        down_payment=3_000,
        cash_flow=0,
        price_range_low=0,
        price_range_high=1_000_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    a1_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Automated Business for Sale",
        card_type="Business",
        price=100_000,
        down_payment=20_000,
        cash_flow=1600,
        price_range_high=100_000,
        price_range_low=100_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a1_card)

    logging.info(
        f"Player2 Business Assets After Starting Company+, before Market Action:"
        f"\n{player2.business_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Software Company Buyer",
        price=1_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 2

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Software Company Buyer",
        price=100_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 1


def test_board_space_action_dont_buy_buy_keep_sell_Apartment_House(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(
        f"\n\n\nStarting: test_board_space_action_dont_buy_buy_keep_sell_Apartment House"
    )

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 70_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Apartment House for Sale",
        card_type="ApartmentHouseForSale",
        units=12,
        price=400_000,
        down_payment=50_000,
        cash_flow=200,
        price_range_low=300_000,
        price_range_high=480_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(
        f"Player2 Real Estate Assets After Not Buying Apartment House, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )
    assert len(player2.real_estate_assets) == 0

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Apartment House for Sale",
        card_type="ApartmentHouseForSale",
        units=12,
        price=350_000,
        down_payment=50_000,
        cash_flow=2_400,
        price_range_low=300_000,
        price_range_high=480_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(
        f"Player2 Real Estate Assets After Buying Apartment House, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Apartment House Buyer",
        price=2_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 1

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Apartment House Buyer",
        price=40_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 0


def test_board_space_action_keep_sell_House_3Br_2Ba(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(
        f"\n\n\nStarting: test_board_space_action_sell_condo_keep_House_3Br_2Ba"
    )

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 70_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="House for Sale - 3Br/2Ba",
        card_type="HouseForSale",
        price=65_000,
        down_payment=7_000,
        cash_flow=150,
        price_range_low=65_000,
        price_range_high=135_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(
        f"Player2 Real Estate Assets After Buying House - 3Br/2Ba, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="House Buyer - 3Br/2Ba",
        price=60_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 1

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="House Buyer - 3Br/2Ba",
        price=90_000,
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 0


def test_board_space_action_keep_sell_Plex(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_keep_Plex")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 70_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="4-plex for Sale",
        card_type="XPlex",
        units=4,
        price=90_000,
        down_payment=14_000,
        cash_flow=500,
        price_range_low=100_000,
        price_range_high=140_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(
        f"Player2 Real Estate Assets After Buying 4-plex, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Plex Buyer",
        price=25_000,  # Per unit
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 1

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Plex Buyer",
        price=40_000,  # Per unit
        must_sell=False,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    assert len(player2.real_estate_assets) == 0


def test_board_space_action_sell_limited_partnership(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_sell_limited_partnership")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 65_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Limited Partner Wanted",
        card_type="Business",
        price=25_000,
        down_payment=25_000,
        cash_flow=1_000,
        price_range_low=50_000,
        price_range_high=75_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Limited Partnership Sold",
        price=2,
        must_sell=True,
        self_only=False,
    )

    cfs_board_space_action.do_market_action(
        a_player=player2,
        board=rat_race_board,
        picked_card=b_card,
    )
    logging.info(f"Player2 Business Assets:\n{player2.business_assets}")
    assert len(player2.business_assets) == 0


def test_board_space_action_invalid_market_cart_type(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_invalid_market_cart_type")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Market",
        title="Price of Foo skyrockets!",
        price=1_000_000,
        must_sell=False,
        self_only=False,
    )

    try:
        cfs_board_space_action.do_market_action(
            a_player=player2,
            board=rat_race_board,
            picked_card=b_card,
        )
        logging.info(f"You really shouldn't be here, should you?")
    except ValueError as e:
        logging.info(f"Correctly detected incorrect market card type with message: {e}")
        return

    err_msg = f"Incorrectly did not detect market card type: {b_card.title}"
    logging.info(err_msg)
    raise ValueError(err_msg)


def test_board_space_action_Tenant_Damages_Your_Property() -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_Tenant_Damages_Your_Propert")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    player2.savings = 100_000

    # Trying damage with no real estate assets - should do nothing
    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Tenant Damages Your Property",
        card_type="Expense",
        cost_if_have_8plex=0,
        cost_if_have_real_estate=1000,
    )

    cfs_board_space_action.do_big_deal_action(
        a_player=player2,
        picked_card=b_card,
    )

    # Trying damage with real estate assets
    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Apartment House for Sale",
        card_type="ApartmentHouseForSale",
        units=12,
        price=350_000,
        down_payment=50_000,
        cash_flow=2_400,
        price_range_low=300_000,
        price_range_high=480_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="20 Acres for Sale",
        card_type="Land",
        acres=20,
        price=20_000,
        down_payment=20_000,
        cash_flow=0,
        price_range_high=2_000,
        price_range_low=100_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    logging.info(
        f"Player2 Real Estate Assets After Buying Apartment House, before Market Action:"
        f"\n{player2.real_estate_assets}"
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Tenant Damages Your Property",
        card_type="Expense",
        cost_if_have_8plex=0,
        cost_if_have_real_estate=1000,
    )

    cfs_board_space_action.do_big_deal_action(
        a_player=player2,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    logging.info(f"Player2 Savings: {player2.savings}")
    assert player2.savings == 100_000 - 50_000 - 20_000 - 1_000


def test_board_space_action_Sewer_Line_Breaks() -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_Sewer_Line_Breaks")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    player2.savings = 100_000

    # Trying damage with no real estate assets - should do nothing
    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Sewer Line Breaks",
        card_type="Expense",
        cost_if_have_8plex=2000,
        cost_if_have_real_estate=0,
    )

    cfs_board_space_action.do_big_deal_action(
        a_player=player2,
        picked_card=b_card,
    )

    # Trying damage with real estate assets
    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="8-plex for Sale",
        card_type="XPlex",
        units=8,
        price=160_000,
        down_payment=32_000,
        cash_flow=1_700,
        price_range_low=200_000,
        price_range_high=280_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_big_deal_action(a_player=player2, picked_card=a_card)

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Sewer Line Breaks",
        card_type="Expense",
        cost_if_have_8plex=2000,
        cost_if_have_real_estate=0,
    )

    cfs_board_space_action.do_big_deal_action(
        a_player=player2,
        picked_card=b_card,
    )
    logging.info(f"Player2 Real Estate Assets:\n{player2.real_estate_assets}")
    logging.info(f"Player2 Savings: {player2.savings}")
    assert player2.savings == 100_000 - 32_000 - 2_000


def test_board_space_action_Bad_Big_Deal_Expense() -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_Bad_Big_Deal_Expense")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    player2.savings = 100_000

    # Trying damage with no real estate assets - should do nothing
    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="A Foo goes Bar",
        card_type="Expense",
        cost_if_have_8plex=0,
        cost_if_have_real_estate=0,
    )

    try:
        cfs_board_space_action.do_big_deal_action(
            a_player=player2,
            picked_card=b_card,
        )
    except ValueError as e:
        logging.info(f"Bad Big Deal Expense card correctly detected with message: {e}")
        return

    err_msg = f"Incorrectly did not detect bad Big Deal Expense card"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_board_space_action_Big_Deal_8_Plex_Expense_Without_Real_Estate() -> None:

    logging.info(
        f"\n\n\nStarting: test_board_space_action_Big_Deal_8_Plex_Expense_Without_Real_Estate"
    )

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    orig_savings: int = 100_000
    player2.savings = orig_savings
    player2.real_estate_assets = []

    # Trying damage with no real estate assets - should do nothing
    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Sewer Line Breaks",
        card_type="Expense",
        cost_if_have_8plex=2_000,
        cost_if_have_real_estate=0,
    )

    cfs_board_space_action.do_big_deal_action(
        a_player=player2,
        picked_card=b_card,
    )
    if player2.savings == orig_savings:
        logging.info(f"Correctly didtnt' pay expense without real estate assets")
    else:
        err_msg = f"Incorrectly paid expense without real estate assets"
        logging.info(err_msg)
        raise ValueError(err_msg)


def test_board_space_action_Big_Deal_Any_real_estate_Expense_Without_Real_Estate() -> None:

    logging.info(
        f"\n\n\nStarting: test_board_space_action_Big_Deal_Any_real_estate_Expense_Without_Real_Estate"
    )

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    orig_savings: int = 100_000
    player2.savings = orig_savings
    player2.real_estate_assets = []

    # Trying damage with no real estate assets - should do nothing
    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="Tenant Damages Your Property",
        card_type="Expense",
        cost_if_have_8plex=0,
        cost_if_have_real_estate=1_000,
    )

    cfs_board_space_action.do_big_deal_action(
        a_player=player2,
        picked_card=b_card,
    )
    if player2.savings == orig_savings:
        logging.info(f"Correctly didtnt' pay expense without real estate assets")
    else:
        err_msg = f"Incorrectly paid expense without real estate assets"
        logging.info(err_msg)
        raise ValueError(err_msg)


def test_board_space_action_Bad_Big_Deal_Card() -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_Bad_Big_Deal_Card")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    player2.savings = 100_000

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Big Deal",
        title="A Foo goes Bar",
        card_type="Fooish Bar",
    )

    try:
        cfs_board_space_action.do_big_deal_action(
            a_player=player2,
            picked_card=b_card,
        )
    except ValueError as e:
        logging.info(f"Bad Big Deal card correctly detected with message: {e}")
        return

    err_msg = f"Incorrectly did not detect bad Big Deal card"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_board_space_action_not_buy_buy_house_for_sale(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_House for Sale")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 5_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="House For Sale - 3BR/2Ba",
        card_type="HouseForSale",
        price=100_000,
        down_payment=10_000,
        cash_flow=100,
        price_range_low=40_000,
        price_range_high=135_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="House For Sale - 3BR/2Ba",
        card_type="HouseForSale",
        price=50_000,
        down_payment=10_000,
        cash_flow=200,
        price_range_low=40_000,
        price_range_high=135_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )


def test_board_space_action_not_buy_buy_10_Acres_Raw_Lane(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_10_Acres_Raw_Lane")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 5_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="10 Acres Raw Lane",
        card_type="Land",
        price=5_000,
        down_payment=5_000,
        cash_flow=0,
        acres=10,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="10 Acres Raw Lane",
        card_type="Land",
        price=5_000,
        down_payment=5_000,
        cash_flow=0,
        acres=10,
        price_range_low=5_000,
        price_range_high=50_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )


def test_board_space_action_Small_Deal_Tenant_Damages_Your_Property(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(
        f"\n\n\nStarting: test_board_space_action_Small_Deal_Tenant_Damages_Your_Property"
    )

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    rat_race_board.add_player(a_player=player2)

    player2.savings = 4_000

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Condo For Sale - 2Br/1Ba",
        card_type="HouseForSale",
        house_or_condo="Condo",
        price=40_000,
        down_payment=4_000,
        cash_flow=140,
        price_range_low=45_000,
        price_range_high=65_000,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )

    a_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="Tenant Damages Your Property",
        card_type="CostIfRentalProperty",
        price=500,
    )
    logging.info(f"Picked card:\n{a_card}")
    cfs_board_space_action.do_small_deal_action(
        a_player=player2, picked_card=a_card, board=rat_race_board
    )


def test_board_space_action_Bad_Small_Deal_Card(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_Bad_Small_Deal_Card")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Small Deal",
        title="A Foo goes Bar",
        card_type="Fooish Bar",
    )

    try:
        cfs_board_space_action.do_small_deal_action(
            a_player=player2,
            picked_card=b_card,
            board=rat_race_board,
        )
    except ValueError as e:
        logging.info(f"Bad Small Deal card correctly detected with message: {e}")
        return

    err_msg = f"Incorrectly did not detect bad Small Deal card"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_board_space_action_Bad_Doodad_Card(
    rat_race_board: cfs_board.Board,
) -> None:

    logging.info(f"\n\n\nStarting: test_board_space_action_Bad_Doodad_Card")

    player2 = cfs_player.Player(
        name=PLAYER2_NAME,
        profession=PROFESSION_DEFS[PLAYER2_PROF],
        strategy=STRATEGY_DEFS[PLAYER2_STRATEGY],
    )

    b_card: cfs_cards.Card = cfs_cards.Card(
        category="Doodad",
        title="A Foo goes Bar",
        card_type="Fooish Bar",
    )

    try:
        cfs_board_space_action.do_doodad_action(
            player=player2,
            picked_card=b_card,
        )
    except ValueError as e:
        logging.info(f"Bad Doodad card correctly detected with message: {e}")
        return

    err_msg = f"Incorrectly did not detect bad Doodad card"
    logging.error(err_msg)
    raise ValueError(err_msg)

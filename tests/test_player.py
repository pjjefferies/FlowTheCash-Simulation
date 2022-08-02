# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:57:35 2020

@author: PaulJ
"""
from __future__ import annotations
from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import logging

import cashflowsim.player as cfs_player
import cashflowsim.profession as cfs_profession
import cashflowsim.strategy as cfs_strategy
import cashflowsim.assets as cfs_assets

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
STRATEGIES_DIR: str = "simulation_strategies"
LOG_DIR: str = "game_logs"

PROFESSIONS_FN: str = "ProfessionsList.json"
STRATEGIES_FN: str = "Strategies.json"
# BOARDSPACES_FN: str = "RatRaceBoardSpaces.json"

PLAYER1_NAME: str = "Player1"
PLAYER1_PROF: str = "Engineer"
PLAYER2_NAME: str = "Player2"
PLAYER2_PROF: str = "Business Manager"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)
profession_data_path_fn: str = join(game_data_path, PROFESSIONS_FN)
strategies_data_path: str = join(base_path, APP_DIR, STRATEGIES_DIR)
strategies_data_path_fn: str = join(strategies_data_path, STRATEGIES_FN)
# boardspaces_path_fn: str = join(game_data_path, BOARDSPACES_FN)

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

profession_defs: dict[
    str, cfs_profession.Profession
] = cfs_profession.get_profession_defs(profession_data_path_fn)
strategy_defs: dict[str, cfs_strategy.Strategy] = cfs_strategy.get_strategy_defs(
    strategy_defs_fn=strategies_data_path_fn
)

"""
@pytest.fixture
def strategies() -> dict[str, cfs_strategy.Strategy]:
    strategies_fn_list: list[str] = [
        f for f in listdir(strategies_data_path) if f.endswith(".json")
    ]
    all_strategies: dict[str, cfs_strategy.Strategy] = {}
    for a_strategy_fn in strategies_fn_list:
        strategy_defs_fn: str = join(strategies_data_path, a_strategy_fn)
        some_strategies: dict[
            str, cfs_strategy.Strategy
        ] = cfs_strategy.get_strategy_defs(strategy_defs_fn)
        all_strategies.update(some_strategies)
    return all_strategies
"""


def test_create_each_player_type():
    """General test using list of tests above."""
    list_of_players: list[cfs_player.Player] = []
    for a_profession in profession_defs:  # create player example for
        name: str = a_profession + " Player"
        list_of_players.append(
            cfs_player.Player(
                name=name,
                profession=profession_defs[a_profession],
                strategy=strategy_defs["Standard Auto"],
            )
        )
    for a_player in list_of_players:
        assert isinstance(a_player, cfs_player.Player)


def test_earn_salary():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )
    old_savings = a_player.savings
    monthly_cash_flow = a_player.monthly_cash_flow
    a_player.earn_salary()
    assert a_player.savings == old_savings + monthly_cash_flow


def test_passive_income():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )
    assert isinstance(a_player.passive_income, int)


def test_monthly_cash_flow():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )
    assert a_player.monthly_cash_flow == a_player.total_income - a_player.total_expenses


def test_total_income():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )
    assert a_player.total_income == a_player.salary + a_player.passive_income


"""
def test_buy_stock_zero_cost_given():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    new_stock: cfs_assets.Stock = cfs_assets.Stock(
        name="ABC",
        asset_type="Stock",
        shares=100,
        cost_per_share=20,
        cash_flow=5,
        price_range_low=19,
        price_range_high=21,
    )

    a_player.buy_stock(stock_asset=new_stock, cost_per_share=0)
"""


def test_buy_sell_stock_need_loan():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    a_player.savings = 0

    new_stock: cfs_assets.Stock = cfs_assets.Stock(
        name="ABC",
        asset_type="Stock",
        shares=100,
        cost_per_share=20,
        dividend_interest=5,
        price_range_low=19,
        price_range_high=21,
    )

    a_player.buy_stock(stock_asset=new_stock, cost_per_share=0)

    a_player.sell_stock(asset=new_stock, price=21, no_shares=50)


def test_buy_stock_needing_but_wont_take_loan():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Dave Ramsey"],
    )

    a_player.savings = 0

    new_stock: cfs_assets.Stock = cfs_assets.Stock(
        name="ABC",
        asset_type="Stock",
        shares=100,
        cost_per_share=20,
        dividend_interest=5,
        price_range_low=19,
        price_range_high=21,
    )

    a_player.buy_stock(stock_asset=new_stock, cost_per_share=0)


def test_sell_stock_not_owned():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    new_stock: cfs_assets.Stock = cfs_assets.Stock(
        name="ABC",
        asset_type="Stock",
        shares=100,
        cost_per_share=20,
        dividend_interest=5,
        price_range_low=19,
        price_range_high=21,
    )

    try:
        a_player.sell_stock(asset=new_stock, price=21, no_shares=50)
    except ValueError as e:
        logging.info(
            f"Correctly detected than an unowned stock was attemmpted to be sold with message {e}. No short selling allowed."
        )
        return
    raise ValueError(f"Trying to sell unowned stock was not detected")


def test_sell_more_stock_than_owned():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    new_stock: cfs_assets.Stock = cfs_assets.Stock(
        name="ABC",
        asset_type="Stock",
        shares=100,
        cost_per_share=20,
        dividend_interest=5,
        price_range_low=19,
        price_range_high=21,
    )

    a_player.buy_stock(stock_asset=new_stock, cost_per_share=0)

    a_player.sell_stock(asset=new_stock, price=21, no_shares=500)


def test_buy_sell_real_estate_need_loan():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    a_player.savings = 0

    new_real_estate: cfs_assets.RealEstate = cfs_assets.RealEstate(
        name="ABC",
        asset_type="House",
        house_or_condo="House",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )

    a_player.buy_real_estate(real_estate_asset=new_real_estate)

    a_player.sell_real_estate(asset=new_real_estate, price=200000)


def test_sell_real_estate_not_owned_by_player():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    new_real_estate: cfs_assets.RealEstate = cfs_assets.RealEstate(
        name="ABC",
        asset_type="House",
        house_or_condo="House",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )

    try:
        a_player.sell_real_estate(asset=new_real_estate, price=200000)
    except ValueError as e:
        logging.info(
            f"Correctly detected than an unowned real estate was attemmpted to be sold with message {e}. No short selling allowed."
        )
        return
    raise ValueError(f"Trying to sell unowned real estate was not detected")


def test_buy_sell_business_need_loan():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    a_player.savings = 0

    new_business: cfs_assets.Business = cfs_assets.Business(
        name="TBO",
        asset_type="Great Company",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )

    a_player.buy_business(business_asset=new_business)

    a_player.sell_business(asset=new_business, price=200000)


def test_sell_business_not_owned_by_player():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    new_business: cfs_assets.Business = cfs_assets.Business(
        name="TBO",
        asset_type="Great Company",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )

    try:
        a_player.sell_business(asset=new_business, price=200000)
    except ValueError as e:
        logging.info(
            f"Correctly detected than an unowned business was attemmpted to be sold with message {e}. No short selling allowed."
        )
        return
    raise ValueError(f"Trying to sell unowned business was not detected")


def test_have_too_many_children():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    for _ in range(4):
        a_player.have_child()


def test_passive_income_calc():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )
    a_player.savings = 2_500

    new_business: cfs_assets.Business = cfs_assets.Business(
        name="TBO",
        asset_type="Great Company",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )
    new_real_estate: cfs_assets.RealEstate = cfs_assets.RealEstate(
        name="ABC",
        asset_type="House",
        house_or_condo="House",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )
    new_stock: cfs_assets.Stock = cfs_assets.Stock(
        name="ABC",
        asset_type="Stock",
        shares=100,
        cost_per_share=20,
        dividend_interest=5,
        price_range_low=19,
        price_range_high=21,
    )
    a_player.buy_business(business_asset=new_business)
    a_player.buy_real_estate(real_estate_asset=new_real_estate)
    a_player.buy_stock(stock_asset=new_stock)

    assert a_player.passive_income == (500 + 500 + 5)


def test_decide_not_to_get_loan_to_buy_business():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Dave Ramsey"],
    )
    a_player.savings = 0

    new_business: cfs_assets.Business = cfs_assets.Business(
        name="TBO",
        asset_type="Great Company",
        down_payment=2000,
        cost=10000,
        cash_flow=500,
        price_range_low=5000,
        price_range_high=30000,
    )

    a_player.buy_business(business_asset=new_business)


def test_using_charity():
    a_player = cfs_player.Player(
        name="Player Name",
        profession=profession_defs[list(profession_defs.keys())[0]],
        strategy=strategy_defs["Standard Auto"],
    )

    a_player.start_charity_turns()

    assert a_player.charity_turns_remaining == 3

    a_player.use_charity_turn()

    assert a_player.charity_turns_remaining == 2

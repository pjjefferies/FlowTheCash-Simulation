# -*- coding: utf-8 -*-
"""
Created on Thu May  5 23:44:45 2022

@author: PaulJ
"""
from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
from typing import Callable
import logging
import pytest
from _pytest.monkeypatch import MonkeyPatch

# from cashflowsim.roll_die import roll_die
from cashflowsim.assets import Asset, Stock
from cashflowsim.loans import Loan
from cashflowsim.player import Player
from cashflowsim.profession import Profession, get_profession_defs
from cashflowsim.strategy import Strategy, get_strategy_defs
from cashflowsim.player_choice import (
    choose_no_die,
    choose_small_or_big_deal_card,
    choose_to_donate_to_charity,
    choose_to_buy_stock_asset,
    choose_to_buy_asset,
    choose_to_sell_asset,
    choose_to_get_loan_to_buy_asset,
    choose_to_pay_off_loan,
    # choose_to_donate_to_charity,
)

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
STRATEGIES_DIR = "simulation_strategies"
LOG_DIR: str = "game_logs"

BOARDSPACES_FN = "RatRaceBoardSpaces.json"
PROFESSIONS_FN = "ProfessionsList.json"
PLAYER1_NAME = "Player1"
PLAYER1_PROF = "Engineer"
PLAYER1_STRATEGY: str = "Dave Ramsey"
PLAYER2_NAME = "Player2"
PLAYER2_PROF: str = "Doctor"
PLAYER2_STRATEGY: str = "Standard Auto"
PLAYER3_NAME: str = "Player3"
PLAYER3_PROF: str = "Business Manager"
PLAYER3_STRATEGY: str = "LowBDT, LowPRT, HighHighROIT"
STRATEGIES_FN: str = "Strategies.json"


base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)
boardspace_path_fn: str = join(game_data_path, BOARDSPACES_FN)
profession_data_path_fn: str = join(game_data_path, PROFESSIONS_FN)
strategies_data_path: str = join(base_path, APP_DIR, STRATEGIES_DIR)
strategies_data_path_fn: str = join(strategies_data_path, STRATEGIES_FN)

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

try:
    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
except OSError:
    err_msg = f"No good Professions json file found, file not found, please fix"
    logging.error(f"{err_msg}\nFile name: {profession_data_path_fn}")
    raise OSError(err_msg)
except ValueError:
    err_msg = f"No good Professions Cards json file found, ValueError, please fix"
    logging.error(f"{err_msg}\nFile name: {profession_data_path_fn}")
    raise ValueError(err_msg)

try:
    strategy_defs: dict[str, Strategy] = get_strategy_defs(
        strategy_defs_fn=strategies_data_path_fn
    )
except OSError:
    err_msg = f"No good Strategies json file found, file not found, please fix"
    logging.error(f"{err_msg}\nFile name: {strategies_data_path_fn}")
    raise OSError(err_msg)
except ValueError:
    err_msg = f"No good Strategies Cards json file found, ValueError, please fix"
    logging.error(f"{err_msg}\nFile name: {strategies_data_path_fn}")
    raise ValueError(err_msg)


@pytest.fixture
def player1() -> Player:
    return Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=strategy_defs[PLAYER1_STRATEGY],
    )


@pytest.fixture
def player2() -> Player:
    return Player(
        name=PLAYER2_NAME,
        profession=profession_defs[PLAYER2_PROF],
        strategy=strategy_defs[PLAYER2_STRATEGY],
    )


@pytest.fixture
def player3() -> Player:
    return Player(
        name=PLAYER3_NAME,
        profession=profession_defs[PLAYER3_PROF],
        strategy=strategy_defs[PLAYER3_STRATEGY],
    )


def test_choose_small_or_big_deal_card_auto(
    player1: Player, player2: Player, player3: Player
) -> None:
    logging.info("Testing Player1 test_choose_small_or_big_deal_card")
    logging.info(
        f"Player1 savings: {player1.savings}"
        f"\nPlayer1 big deal threshold: {player1.strategy.big_deal_small_deal_threshold}"
    )
    assert choose_small_or_big_deal_card(a_player=player1) == "small"
    for _ in range(3):
        player1.earn_salary()
    logging.info(f"Player1 earned salary x 3")
    logging.info(
        f"Player1 savings: {player1.savings}"
        f"\nPlayer1 big deal threshold: {player1.strategy.big_deal_small_deal_threshold}"
    )
    assert choose_small_or_big_deal_card(a_player=player1) == "big"
    logging.info(f"Player1 chose correct big and small deal cards")

    logging.info("Testing Player2 test_choose_small_or_big_deal_card")
    logging.info(
        f"Player2 savings: {player2.savings}"
        f"\nPlayer2 big deal threshold: {player2.strategy.big_deal_small_deal_threshold}"
    )
    assert choose_small_or_big_deal_card(a_player=player2) == "small"
    for _ in range(2):
        player2.earn_salary()
    logging.info(f"Player2 earned salary x 2")
    logging.info(
        f"Player2 savings: {player2.savings}"
        f"\nPlayer2 big deal threshold: {player2.strategy.big_deal_small_deal_threshold}"
    )
    assert choose_small_or_big_deal_card(a_player=player2) == "big"
    logging.info(f"Player2 chose correct big and small deal cards")

    logging.info("Testing Player3 test_choose_small_or_big_deal_card")
    logging.info(
        f"Player3 savings: {player3.savings}"
        f"\nPlayer3 big deal threshold: {player3.strategy.big_deal_small_deal_threshold}"
    )
    assert choose_small_or_big_deal_card(a_player=player3) == "small"
    for _ in range(2):
        player3.earn_salary()
    logging.info(f"Player3 earned salary x 2")
    logging.info(
        f"Player3 savings: {player3.savings}"
        f"\nPlayer3 big deal threshold: {player3.strategy.big_deal_small_deal_threshold}"
    )
    assert choose_small_or_big_deal_card(a_player=player3) == "big"
    logging.info(f"Player3 chose correct big and small deal cards")


def test_choose_small_or_big_deal_card_manual(
    player1: Player, monkeypatch: MonkeyPatch
) -> None:
    logging.info("\n\nTesting test_choose_small_or_big_deal_card_manual")

    choose_small_deal: list[Callable[[str], str]] = [
        lambda _: "s",
        lambda _: "S",
        lambda _: "small",
        lambda _: "Small",
    ]

    responses = iter(["Foo", "B"])

    choose_big_deal: list[Callable[[str], str]] = [
        lambda _: "b",
        lambda _: "B",
        lambda _: "big",
        lambda _: "Big",
        lambda _: next(responses),
    ]

    player1.strategy.manual = True
    for a_small_choice in choose_small_deal:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_small_choice)
            assert choose_small_or_big_deal_card(a_player=player1) == "small"

    for a_big_choice in choose_big_deal:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_big_choice)
            assert choose_small_or_big_deal_card(a_player=player1) == "big"


def test_choose_to_donate_to_charity_manual(
    player1: Player, monkeypatch: MonkeyPatch
) -> None:
    logging.info("\n\nTesting test_choose_to_donate_to_charity_manual")

    donate_charity_no: list[Callable[[str], str]] = [
        lambda _: "n",
        lambda _: "N",
        lambda _: "no",
        lambda _: "No",
    ]

    responses = iter(["Foo", "yes"])

    donate_charity_yes: list[Callable[[str], str]] = [
        lambda _: "y",
        lambda _: "Y",
        lambda _: "yes",
        lambda _: "Yes",
        lambda _: next(responses),
    ]

    player1.strategy.manual = True

    for a_no in donate_charity_no:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no)
            assert not choose_to_donate_to_charity(a_strategy=player1.strategy)

    for a_yes in donate_charity_yes:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_yes)
            assert choose_to_donate_to_charity(a_strategy=player1.strategy)


def test_choose_no_dice_manual(player1: Player, monkeypatch: MonkeyPatch) -> None:
    logging.info("\n\nTesting test_choose_no_dice_manual")

    responses1 = iter(["foo", "45", "1"])
    responses2 = iter(["702", "2"])

    no_dice_opts: list[Callable[[str], str]] = [
        lambda _: "1",
        lambda _: "2",
        lambda _: next(responses1),
        lambda _: next(responses2),
    ]

    no_dice_answers: list[int] = [1, 2, 1, 2]

    player1.strategy.manual = True

    for n, a_no_dice in enumerate(no_dice_opts):
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no_dice)
            # logging.info(f"a_no_dice: {a_no_dice('')}, answer: {no_dice_answers[n]}")
            no_dice_chosen = choose_no_die(
                no_die_choice_list=[1, 2], a_strategy=player1.strategy
            )
            assert no_dice_chosen == no_dice_answers[n]
            logging.info(f"{no_dice_chosen} == {no_dice_answers[n]}")


def test_choose_no_stock_shares_to_buy_manual(
    player1: Player, monkeypatch: MonkeyPatch
) -> None:
    logging.info("\n\nTesting test_choose_no_stock_shares_to_buy_manual")

    a_new_stock = Stock(
        name="TBO",
        asset_type="Stock",
        shares=0,
        dividend_interest=5,
        price_range_low=50,
        price_range_high=500,
        cost_per_share=100,
    )

    responses1 = iter(["foo", "-1", "0"])
    responses2 = iter(["bar", "-100", "100"])

    no_shares_opts: list[Callable[[str], str]] = [
        lambda _: "0",
        lambda _: "1",
        lambda _: "10",
        lambda _: "100",
        lambda _: "1000000",
        lambda _: next(responses1),
        lambda _: next(responses2),
    ]

    no_shares_answers: list[tuple[bool, int]] = [
        (False, 0),
        (True, 1),
        (True, 10),
        (True, 100),
        (True, 1000000),
        (False, 0),
        (True, 100),
    ]

    player1.strategy.manual = True

    for n, a_no_shares_response in enumerate(no_shares_opts):
        a_new_stock.shares = 0
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no_shares_response)
            buy_stock = choose_to_buy_stock_asset(
                a_player=player1, new_stock=a_new_stock
            )
            logging.info(f"buy_stock: {buy_stock}")
            assert buy_stock == no_shares_answers[n][0]
            logging.info(f"{buy_stock} == {no_shares_answers[n][0]}")
            assert a_new_stock.shares == no_shares_answers[n][1]
            logging.info(f"{a_new_stock.shares} == {no_shares_answers[n][1]}")


def test_choose_no_stock_shares_to_buy_auto(player1: Player) -> None:
    logging.info("\n\nTesting test_choose_no_stock_shares_to_buy_auto")

    a_new_stock = Stock(
        name="TBO",
        asset_type="Stock",
        shares=0,
        dividend_interest=5,
        price_range_low=50,
        price_range_high=500,
        cost_per_share=100,
    )

    player1.strategy.manual = False
    player1.strategy.roi_threshold = 0.20
    player1.savings = 10
    player1.strategy.take_any_loans = False

    # Try to buy stock with not enough money
    decide_to_buy_stock: bool = choose_to_buy_stock_asset(
        a_player=player1, new_stock=a_new_stock
    )
    try:
        assert not decide_to_buy_stock
        logging.info(f"Properly decided not to by shares without enough money")
    except AssertionError:
        logging.info(f"Improperly decided to shares without enough money")
        raise

    # Try to buy stock with enough money
    player1.savings = 10_000
    no_shares_should_buy: int = player1.savings // a_new_stock.cost_per_share
    decide_to_buy_stock: bool = choose_to_buy_stock_asset(
        a_player=player1, new_stock=a_new_stock
    )
    try:
        assert decide_to_buy_stock
        assert a_new_stock.shares == no_shares_should_buy
        logging.info(
            f"Properly decided to buy {a_new_stock.shares} shares with enough money"
        )
    except AssertionError:
        logging.info(f"Improperly decided to not buy shares with enough money")
        raise

    # Try to not buy stock with enough money but too low roi
    player1.savings = 10_000
    player1.strategy.roi_threshold = 0.9
    player1.strategy.price_ratio_threshold = 0.1
    no_shares_should_buy: int = player1.savings // a_new_stock.cost_per_share
    decide_to_buy_stock: bool = choose_to_buy_stock_asset(
        a_player=player1, new_stock=a_new_stock
    )
    try:
        assert not decide_to_buy_stock
        logging.info(
            f"Properly decided not to buy stock with enough money but too low roi"
        )
    except AssertionError:
        logging.info(
            f"Improperly decided to buy shares with enough money but too low roi"
        )
        raise


def test_choose_to_buy_asset_manual(player1: Player, monkeypatch: MonkeyPatch) -> None:
    logging.info("\n\nTesting test_choose_to_buy_asset_manual")

    an_asset = Asset(
        name="Rare Gold Coin",
        asset_type="Asset",
        cost=500,
        cash_flow=0,
        price_range_low=0,
        price_range_high=4000,
    )

    no_list: list[Callable[[str], str]] = [
        lambda _: "n",
        lambda _: "N",
        lambda _: "no",
        lambda _: "No",
    ]

    eventual_yes = iter(["Foo", "yes"])

    yes_list: list[Callable[[str], str]] = [
        lambda _: "y",
        lambda _: "Y",
        lambda _: "yes",
        lambda _: "Yes",
        lambda _: next(eventual_yes),
    ]

    player1.strategy.manual = True

    for a_no in no_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no)
            assert not choose_to_buy_asset(a_player=player1, asset=an_asset)

    for a_yes in yes_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_yes)
            assert choose_to_buy_asset(a_player=player1, asset=an_asset)


def test_choose_to_sell_stock_auto(player1: Player) -> None:
    logging.info("\n\nTesting test_choose_to_buy_stock_auto")

    an_asset = Stock(
        name="MYT4U",
        asset_type="Stock",
        cost=1,
        shares=100,
        dividend_interest=0,
        price_range_low=0,
        price_range_high=30,
    )

    player1.strategy.manual = False
    player1.savings = 100

    player1.buy_stock(stock_asset=an_asset, cost_per_share=1)

    choose_to_sell_asset(a_player=player1, asset=an_asset, price=2, delta_price=3)


def test_choose_to_sell_stock_manual(player1: Player, monkeypatch: MonkeyPatch) -> None:
    logging.info("\n\nTesting test_choose_to_buy_stock_manual")

    no_list: list[Callable[[str], str]] = [
        lambda _: "n",
        lambda _: "N",
        lambda _: "no",
        lambda _: "No",
    ]

    eventual_yes = iter(["Foo", "yes"])

    yes_list: list[Callable[[str], str]] = [
        lambda _: "y",
        lambda _: "Y",
        lambda _: "yes",
        lambda _: "Yes",
        lambda _: next(eventual_yes),
    ]

    an_asset = Stock(
        name="MYT4U",
        asset_type="Stock",
        cost=1,
        shares=100,
        dividend_interest=0,
        price_range_low=0,
        price_range_high=30,
    )

    player1.strategy.manual = False
    player1.savings = 100

    player1.buy_stock(stock_asset=an_asset, cost_per_share=1)

    player1.strategy.manual = True

    for a_no in no_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no)
            assert not choose_to_sell_asset(a_player=player1, asset=an_asset, price=50)

    for a_yes in yes_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_yes)
            assert choose_to_sell_asset(a_player=player1, asset=an_asset, price=50)
            # Reset for next try
            player1.strategy.manual = False
            player1.savings = 100
            player1.buy_stock(stock_asset=an_asset, cost_per_share=1)
            player1.strategy.manual = True


def test_choose_to_get_loan_to_buy_asset_manual(
    player1: Player, monkeypatch: MonkeyPatch
) -> None:
    logging.info("\n\nTesting choose_to_get_loan_to_buy_asset_manual")

    an_asset = Asset(
        name="Rare Gold Coin",
        asset_type="Asset",
        cost=500,
        cash_flow=0,
        price_range_low=0,
        price_range_high=4000,
    )

    player1.savings = 0

    no_list: list[Callable[[str], str]] = [
        lambda _: "n",
        lambda _: "N",
        lambda _: "no",
        lambda _: "No",
    ]

    eventual_yes = iter(["Foo", "yes"])

    yes_list: list[Callable[[str], str]] = [
        lambda _: "y",
        lambda _: "Y",
        lambda _: "yes",
        lambda _: "Yes",
        lambda _: next(eventual_yes),
    ]

    player1.strategy.manual = True

    for a_no in no_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no)
            assert not choose_to_get_loan_to_buy_asset(
                a_player=player1, asset=an_asset, loan_amount=500
            )

    for a_yes in yes_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_yes)
            assert choose_to_get_loan_to_buy_asset(
                a_player=player1, asset=an_asset, loan_amount=500
            )


def test_choose_to_pay_off_loan_manual(
    player1: Player, monkeypatch: MonkeyPatch
) -> None:
    logging.info("\n\nTesting choose_to_pay_off_loan_manual")

    a_loan: Loan = Loan(
        name="a_loan",
        balance=10_000,
        monthly_payment=1000,
        partial_payment_allowed=True,
    )
    b_loan: Loan = Loan(
        name="b_loan",
        balance=10_000,
        monthly_payment=1000,
        partial_payment_allowed=False,
    )
    player1.loan_list = []
    player1.make_loan(loan=a_loan)
    player1.make_loan(loan=b_loan)

    eventual_no_1 = iter(["Foo", "-1", "3", "0"])
    eventual_no_2 = iter(["2", "5_000"])
    eventual_no_3 = iter(["2", "10_000"])

    no_list: list[Callable[[str], str]] = [
        lambda _: "0",
        lambda _: next(eventual_no_1),
        lambda _: next(eventual_no_2),
        lambda _: next(eventual_no_3),
    ]

    eventual_yes_1 = iter(["1", "1000"])
    eventual_yes_2 = iter(["Foo", "15", "1", "apple", "50", "1000"])
    eventual_yes_3 = iter(["2", "10_000"])

    yes_list: list[Callable[[str], str]] = [
        lambda _: next(eventual_yes_1),
        lambda _: next(eventual_yes_2),
        lambda _: next(eventual_yes_3),
    ]

    player1.strategy.loan_payback = "Manual"

    player1.savings = 5_000

    for a_no in no_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_no)
            try:
                assert not choose_to_pay_off_loan(a_player=player1)
                logging.info(f"Corrrectly chose not to pay off loan")
            except AssertionError:
                logging.info(f"Incorrectly chose to pay off loan")
                raise
            # Re-take loan for next iteration
            if a_loan not in player1.loan_list:
                player1.make_loan(loan=a_loan)
            if b_loan not in player1.loan_list:
                player1.make_loan(loan=b_loan)

    player1.savings = 15_000

    for a_yes in yes_list:
        with monkeypatch.context() as m:
            m.setattr("builtins.input", a_yes)
            try:
                assert choose_to_pay_off_loan(a_player=player1)
                logging.info(f"Correctly chose to pay off loan")
            except AssertionError:
                logging.info(f"Incorrectly chose not to pay off loan")
                raise
            # Re-take loan for next iteration
            if a_loan not in player1.loan_list:
                player1.make_loan(loan=a_loan)
            if b_loan not in player1.loan_list:
                player1.make_loan(loan=b_loan)


def test_choose_to_pay_off_loan_auto(player1: Player) -> None:
    logging.info(f"\n\nTesting choose_to_pay_off_loan_auto")
    logging.info(f"Player Savings: {player1.savings}")
    some_loans: list[Loan] = [
        Loan(
            name="a_loan",
            balance=1_000,
            monthly_payment=10,
            partial_payment_allowed=True,
        ),
        Loan(
            name="b_loan",
            balance=10_000,
            monthly_payment=100,
            partial_payment_allowed=True,
        ),
        Loan(
            name="c_loan",
            balance=9_000,
            monthly_payment=500,
            partial_payment_allowed=True,
        ),
    ]

    loan_choice_methods: list[tuple[str, int]] = [
        ("Largest", 1),
        ("Smallest", 0),
        ("Highest Interest", 2),
    ]

    logging.info(f"Testing to pay-off loans that should be paid-off")
    for loan_choice_method in loan_choice_methods:
        logging.info(f"\nloan_choice_method: {loan_choice_method}")
        player1.loan_list = []
        for a_loan in some_loans:
            player1.make_loan(loan=a_loan)

        player1.savings = 10_000
        logging.info(f"player1.savings = {player1.savings}")
        player1.strategy.loan_payback = loan_choice_method[0]

        try:
            assert choose_to_pay_off_loan(a_player=player1)
            assert some_loans[loan_choice_method[1]] not in player1.loan_list
            logging.info(f"Corrrectly chose loan to pay off")
        except AssertionError:
            logging.info(f"Incorrectly chose wrong loan to pay-off")
            raise

    logging.info(f"Testing to pay-off loans that should not be paid-off")
    for loan_choice_method in loan_choice_methods:
        logging.info(f"\nloan_choice_method: {loan_choice_method}")
        player1.loan_list = []
        for a_loan in some_loans:
            player1.make_loan(loan=a_loan)

        player1.savings = 500
        logging.info(f"player1.savings = {player1.savings}")
        player1.strategy.loan_payback = loan_choice_method[0]

        try:
            assert not choose_to_pay_off_loan(a_player=player1)
            assert some_loans[loan_choice_method[1]] in player1.loan_list
            logging.info(f"Corrrectly chose not to pay-off loan")
        except AssertionError:
            logging.info(f"Incorrectly chose to pay-off loan")
            raise

    logging.info(f"Testing to pay-down loan that should be paid-down")
    loan_choice_method: tuple[str, int] = ("Largest", 1)
    logging.info(f"\nloan_choice_method: {loan_choice_method}")
    player1.loan_list = [some_loans[loan_choice_method[1]]]

    player1.savings = 1_500
    logging.info(f"player1.savings = {player1.savings}")
    player1.strategy.loan_payback = loan_choice_method[0]

    try:
        assert choose_to_pay_off_loan(a_player=player1)
        logging.info(f"Corrrectly chose to pay-down loan")
    except AssertionError:
        logging.info(f"Incorrectly chose to not pay-down loan")
        raise

    logging.info(f"\nTesting choosing to pay-off loan with no loans")
    player1.loan_list = []
    loan_payed_off = choose_to_pay_off_loan(a_player=player1)
    logging.info(f"Result: {loan_payed_off}")
    assert not loan_payed_off
    logging.info(f"Correct!")

    logging.info(f"\nTesting choosing to pay-off loan with bad strategy name")
    player1.loan_list = []
    for a_loan in some_loans:
        player1.make_loan(loan=a_loan)
    try:
        player1.strategy.loan_payback = "Biggest Unit"
        choose_to_pay_off_loan(a_player=player1)
    except ValueError:
        info_msg = f"Correctly chose not to pay-off loan."
        logging.info(info_msg)
        return
    err_msg = f"Incorrectly chose to pay-off loan"
    logging.error(err_msg)

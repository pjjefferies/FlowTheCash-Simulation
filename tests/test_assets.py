# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""


from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
from typing import List
import logging

from cashflowsim.assets import Asset, Stock, RealEstate, Business
from cashflowsim.cards import (
    Card,
    EmptyDeckError,
    load_all_small_deal_cards,
    load_all_big_deal_cards,
    CardDeck,
)

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR = "game_data"
LOG_DIR: str = "game_logs"

SMALLDEALCARDS_FN = "SmallDealCards.json"
BIGDEALCARDS_FN = "BigDealCards.json"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)

this_fn: str = __file__.split("\\")[-1].split(".")[0]
logfile_fn: str = "".join([this_fn, "_log.txt"])

logfile_path_fn: str = join(base_path, APP_DIR, LOG_DIR, logfile_fn)

logging.basicConfig(
    filename=logfile_path_fn,
    # level=logging.DEBUG,
    level=logging.ERROR,
    filemode="a",
    format="%(asctime)s - (%(levelname)s) %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    force=True,
)
logging.info(
    f"\n\n\nStart of new test run: {dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
)


def test_add_assets_in_small_deal_card_deck() -> None:
    small_deal_card_deck_fn = join(game_data_path, SMALLDEALCARDS_FN)
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_card_deck_fn
    )
    small_deal_card_deck.shuffle()

    asset_list: List[Asset] = []

    while True:
        try:
            small_deal_card: Card = small_deal_card_deck.take_top_card()  # type: ignore
        except EmptyDeckError:
            break
        match small_deal_card.card_type:
            case "Stock" | "CD":
                asset_list.append(
                    Stock(
                        name=small_deal_card.symbol,
                        asset_type=small_deal_card.card_type,
                        shares=100,
                        cost=small_deal_card.price,
                        cash_flow=small_deal_card.dividend,
                        price_range_low=small_deal_card.price_range_low,
                        price_range_high=small_deal_card.price_range_high,
                    )
                )
            case "HouseForSale":
                asset_list.append(
                    RealEstate(
                        name=small_deal_card.title,
                        asset_type=small_deal_card.card_type,
                        house_or_condo=small_deal_card.house_or_condo,
                        cost=small_deal_card.price,
                        down_payment=small_deal_card.down_payment,
                        cash_flow=small_deal_card.cash_flow,
                        price_range_low=small_deal_card.price_range_low,
                        price_range_high=small_deal_card.price_range_high,
                    )
                )
            case "StartCompany":
                asset_list.append(
                    Business(
                        name=small_deal_card.title,
                        asset_type=small_deal_card.card_type,
                        cost=small_deal_card.price,
                        down_payment=small_deal_card.down_payment,
                    )
                )  # no Price Range for Small Deal Co.
            case "Land":
                asset_list.append(
                    RealEstate(
                        name=small_deal_card.title,
                        asset_type=small_deal_card.card_type,
                        house_or_condo=small_deal_card.house_or_condo,
                        cost=small_deal_card.price,
                        down_payment=small_deal_card.down_payment,
                        acres=small_deal_card.acres,
                    )
                )
            case "Asset":
                asset_list.append(
                    Asset(
                        name=small_deal_card.title,
                        asset_type=small_deal_card.card_type,
                        cost=small_deal_card.price,
                        cash_flow=small_deal_card.cash_flow,
                        price_range_low=small_deal_card.price_range_low,
                        price_range_high=small_deal_card.price_range_high,
                    )
                )
            case "StockSplit" | "CostIfRentalProperty" | "LoanNotToBeRepaid":
                logging.info(f"{small_deal_card.card_type} drew. No asset to save.")
            case _:
                logging.error(f"Small Card type: {small_deal_card.card_type} not found")

    for asset in asset_list:
        logging.info(asset)


def test_add_assets_in_big_deal_card_deck():
    big_deal_card_deck_fn = join(game_data_path, BIGDEALCARDS_FN)
    big_deal_card_deck: CardDeck = load_all_big_deal_cards(
        big_deal_cards_filename=big_deal_card_deck_fn
    )
    big_deal_card_deck.shuffle()
    asset_list: List[Asset] = []

    while True:
        try:
            big_deal_card: Card = big_deal_card_deck.take_top_card()  # type: ignore
        except EmptyDeckError:
            break
        match big_deal_card.card_type:
            case "ApartmentHouseForSale" | "XPlex":
                asset_list.append(
                    RealEstate(
                        name=big_deal_card.title,
                        asset_type=big_deal_card.card_type,
                        house_or_condo=big_deal_card.house_or_condo,
                        cost=big_deal_card.price,
                        down_payment=big_deal_card.down_payment,
                        cash_flow=big_deal_card.cash_flow,
                        price_range_low=big_deal_card.price_range_low,
                        price_range_high=big_deal_card.price_range_high,
                        units=big_deal_card.units,
                    )
                )
            case "HouseForSale":
                asset_list.append(
                    RealEstate(
                        name=big_deal_card.title,
                        asset_type=big_deal_card.card_type,
                        house_or_condo=big_deal_card.house_or_condo,
                        cost=big_deal_card.price,
                        down_payment=big_deal_card.down_payment,
                        cash_flow=big_deal_card.cash_flow,
                        price_range_low=big_deal_card.price_range_low,
                        price_range_high=big_deal_card.price_range_high,
                    )
                )
            case "Partnership" | "Business":
                asset_list.append(
                    Business(
                        name=big_deal_card.title,
                        asset_type=big_deal_card.card_type,
                        cost=big_deal_card.price,
                        down_payment=big_deal_card.down_payment,
                        cash_flow=big_deal_card.cash_flow,
                        price_range_low=big_deal_card.price_range_low,
                        price_range_high=big_deal_card.price_range_high,
                    )
                )
            case "Land":
                asset_list.append(
                    RealEstate(
                        name=big_deal_card.title,
                        asset_type=big_deal_card.card_type,
                        house_or_condo=big_deal_card.house_or_condo,
                        cost=big_deal_card.price,
                        down_payment=big_deal_card.down_payment,
                        cash_flow=big_deal_card.cash_flow,
                        price_range_low=big_deal_card.price_range_low,
                        price_range_high=big_deal_card.price_range_high,
                        acres=big_deal_card.acres,
                    )
                )
            case "Expense":
                logging.info(f"{big_deal_card.card_type} drew. No asset to save.")
            case _:
                logging.error(f"Big Card type: {big_deal_card.card_type} not found")

    for asset in asset_list:
        logging.info(asset)


def test_reduce_stock_shares():
    a_stock: Stock = Stock(
        name="TBO",
        asset_type="Stock",
        cost_per_share=100,
        dividend_interest=10,
        price_range_low=50,
        price_range_high=500,
        shares=50,
    )

    logging.info(f"Shares before reducing: {a_stock.shares}")
    no_shares_to_reduce: int = 10
    logging.info(f"Shares to reduce: {no_shares_to_reduce}")

    a_stock.reduce_no_shares(shares_to_reduce=no_shares_to_reduce)
    logging.info(f"Shares after reducing: {a_stock.shares}")


def test_reduce_too_many_stock_shares():
    a_stock: Stock = Stock(
        name="TBO",
        asset_type="Stock",
        cost_per_share=100,
        dividend_interest=10,
        price_range_low=50,
        price_range_high=500,
        shares=50,
    )

    logging.info(f"Shares before reducing: {a_stock.shares}")
    no_shares_to_reduce: int = 100
    logging.info(f"Shares to reduce: {no_shares_to_reduce}")

    a_stock.reduce_no_shares(shares_to_reduce=no_shares_to_reduce)
    logging.info(f"Shares after reducing: {a_stock.shares}")


def test_calculate_stock_roi():
    a_stock: Stock = Stock(
        name="TBO",
        asset_type="Stock",
        cost_per_share=100,
        dividend_interest=10,
        price_range_low=50,
        price_range_high=500,
        shares=50,
    )
    # Calculate ROI as part of printing stock string
    logging.info(f"Stock:\n{a_stock}")


def test_calculate_stock_roi_with_dividends_but_no_cost():
    a_stock: Stock = Stock(
        name="TBO",
        asset_type="Stock",
        cost_per_share=0,
        dividend_interest=10,
        price_range_low=50,
        price_range_high=500,
        shares=50,
    )
    # Calculate ROI as part of printing stock string
    logging.info(f"Stock:\n{a_stock}")


def test_increase_business_cash_flow():
    a_business: Business = Business(
        name="TBO",
        asset_type="Busisness",
        cost=100_000,
        down_payment=10_000,
        cash_flow=1_000,
        price_range_low=50,
        price_range_high=500,
    )

    logging.info(f"Cash flow before increasing: {a_business.cash_flow}")
    cash_flow_increase: int = 500
    logging.info(f"Cash flow increase: {cash_flow_increase}")

    a_business.increase_cash_flow(increase_amount=cash_flow_increase)
    logging.info(f"Cash flow after increasing: {a_business.cash_flow}")

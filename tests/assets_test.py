# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

SMALLDEALCARDS_FN = "../game_data/SmallDealCards.json"
BIGDEALCARDS_FN = "../game_data/BigDealCards.json"

import copy
import unittest


class TestAssets(unittest.TestCase):
    """Test Class to test Asset objects in assets module."""

    from cashflowsim.assets import Asset, Stock, RealEstate, Business
    from cashflowsim.cards import (
        Card,
        DoodadCard,
        MarketCard,
        DealCard,
        SmallDealCard,
        BigDealCard,
        load_all_doodad_cards,
        load_all_market_cards,
        load_all_small_deal_cards,
        load_all_big_deal_cards,
        Deck,
    )

    #    small_deal_card_deck.shuffle()
    #    big_deal_card-deck.shuffle()

    def test_add_assets_in_small_deal_card_deck(self) -> None:
        small_deal_card_deck_master = TestAssets.load_all_small_deal_cards(
            SMALLDEALCARDS_FN
        )
        small_deal_card_deck = copy.copy(small_deal_card_deck_master)

        asset_list = []

        while True:
            small_deal_card = small_deal_card_deck.take_top_card()
            if small_deal_card is None:
                break
            #        print("Small Deal Card Type: ", small_deal_card.card_type)
            if small_deal_card.card_type in ["Stock", "CD"]:
                asset_list.append(
                    TestAssets.Stock(
                        small_deal_card.symbol,
                        100,  # shares
                        small_deal_card.price,
                        small_deal_card.dividend,
                        small_deal_card.price_range_low,
                        small_deal_card.price_range_high,
                    )
                )
            elif small_deal_card.card_type == "HouseForSale":
                asset_list.append(
                    TestAssets.RealEstate(
                        small_deal_card.title,
                        small_deal_card.card_type,
                        small_deal_card.house_or_condo,
                        small_deal_card.price,
                        small_deal_card.down_payment,
                        small_deal_card.cash_flow,
                        small_deal_card.price_range_low,
                        small_deal_card.price_range_high,
                        0,
                        0,
                    )
                )
            elif small_deal_card.card_type == "StartCompany":
                asset_list.append(
                    TestAssets.Business(
                        small_deal_card.title,
                        small_deal_card.card_type,
                        small_deal_card.price,
                        small_deal_card.down_payment,
                        small_deal_card.cash_flow,
                        0,  # no Price Range for Small Deal Co.
                        0,
                    )
                )  # no Price Range for Small Deal Co.
            elif small_deal_card.card_type == "Land":
                asset_list.append(
                    TestAssets.RealEstate(
                        small_deal_card.title,
                        small_deal_card.card_type,
                        small_deal_card.house_or_condo,
                        small_deal_card.price,
                        small_deal_card.down_payment,
                        0,  # no cash flow
                        0,  # no Price Range Low
                        0,  # no Price Range High,
                        0,  # no units
                        small_deal_card.acres,
                    )
                )
            elif small_deal_card.card_type == "Asset":
                asset_list.append(
                    TestAssets.Asset(
                        small_deal_card.title,
                        small_deal_card.card_type,
                        small_deal_card.price,
                        0,  # no Down Payment on Small Deal Assets
                        small_deal_card.cash_flow,
                        small_deal_card.price_range_low,
                        small_deal_card.price_range_high,
                    )
                )
            else:
                print("Small Card type:", small_deal_card.card_type, "not found")

        for asset in asset_list:
            print(asset)

    def test_add_assets_in_big_deal_card_deck(self):
        big_deal_card_deck_master = TestAssets.load_all_big_deal_cards(BIGDEALCARDS_FN)

        big_deal_card_deck = copy.copy(big_deal_card_deck_master)

        asset_list = []

        while True:
            big_deal_card = big_deal_card_deck.take_top_card()
            if big_deal_card is None:
                break
            if big_deal_card.card_type in ["ApartmentHouseForSale", "XPlex"]:
                asset_list.append(
                    TestAssets.RealEstate(
                        big_deal_card.title,
                        big_deal_card.card_type,
                        big_deal_card.house_or_condo,
                        big_deal_card.price,
                        big_deal_card.down_payment,
                        big_deal_card.cash_flow,
                        big_deal_card.price_range_low,
                        big_deal_card.price_range_high,
                        big_deal_card.units,
                        0,
                    )
                )  # no acres
            elif big_deal_card.card_type == "HouseForSale":
                asset_list.append(
                    TestAssets.RealEstate(
                        big_deal_card.title,
                        big_deal_card.card_type,
                        big_deal_card.house_or_condo,
                        big_deal_card.price,
                        big_deal_card.down_payment,
                        big_deal_card.cash_flow,
                        big_deal_card.price_range_low,
                        big_deal_card.price_range_high,
                        0,  # no units
                        0,
                    )
                )  # no acres
            elif big_deal_card.card_type in ["Partnership", "Business"]:
                asset_list.append(
                    TestAssets.Business(
                        big_deal_card.title,
                        big_deal_card.card_type,
                        big_deal_card.price,
                        big_deal_card.down_payment,
                        big_deal_card.cash_flow,
                        big_deal_card.price_range_low,
                        big_deal_card.price_range_high,
                    )
                )
            elif big_deal_card.card_type == "Land":
                asset_list.append(
                    TestAssets.RealEstate(
                        big_deal_card.title,
                        big_deal_card.card_type,
                        big_deal_card.price,
                        big_deal_card.down_payment,
                        big_deal_card.cash_flow,
                        big_deal_card.price_range_low,
                        big_deal_card.price_range_high,
                        0,  # no units
                        big_deal_card.acres,
                    )
                )
            else:
                print("Big Card type:", big_deal_card.card_type, "not found")

        for asset in asset_list:
            print(asset)


if __name__ == "__main__":
    unittest.main(verbosity=2)

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""
# from .context import cashflowsim

import unittest

class TestAssets(unittest.TestCase):
    """Test Class to test Asset objects in assets module."""
    from cashflowsim.assets import Stock
    from cashflowsim.assets import Asset, Stock, RealEstate, Business
    import cards
    import copy
    small_deal_card_deck_master = (
        cards.load_all_small_deal_cards("SmallDealCards.json"))
    big_deal_card_deck_master = (
        cards.load_all_big_deal_cards("BigDealCards.json"))

    small_deal_card_deck = copy.copy(small_deal_card_deck_master)
    big_deal_card_deck = copy.copy(big_deal_card_deck_master)

#    small_deal_card_deck.shuffle()
#    big_deal_card-deck.shuffle()

    asset_list = []

    while True:
        small_deal_card = small_deal_card_deck.take_top_card()
        if small_deal_card is None:
            break
#        print("Small Deal Card Type: ", small_deal_card.card_type)
        if small_deal_card.card_type in ["Stock", "CD"]:
            asset_list.append(Stock(small_deal_card.symbol,
                                    100,     # shares
                                    small_deal_card.price,
                                    small_deal_card.dividend,
                                    small_deal_card.price_range_low,
                                    small_deal_card.price_range_high))
        elif small_deal_card.card_type == "HouseForSale":
            asset_list.append(RealEstate(small_deal_card.title,
                                         small_deal_card.card_type,
                                         small_deal_card.house_or_condo,
                                         small_deal_card.price,
                                         small_deal_card.down_payment,
                                         small_deal_card.cash_flow,
                                         small_deal_card.price_range_low,
                                         small_deal_card.price_range_high,
                                         0, 0))
        elif small_deal_card.card_type == "StartCompany":
            asset_list.append(Business(small_deal_card.title,
                                       small_deal_card.card_type,
                                       small_deal_card.price,
                                       small_deal_card.down_payment,
                                       small_deal_card.cash_flow,
                                       0,  # no Price Range for Small Deal Co.
                                       0))  # no Price Range for Small Deal Co.
        elif small_deal_card.card_type == "Land":
            asset_list.append(RealEstate(small_deal_card.title,
                                         small_deal_card.card_type,
                                         small_deal_card.house_or_condo,
                                         small_deal_card.price,
                                         small_deal_card.down_payment,
                                         0,  # no cash flow
                                         0,  # no Price Range Low
                                         0,  # no Price Range High,
                                         0,  # no units
                                         small_deal_card.acres))
        elif small_deal_card.card_type == "Asset":
            asset_list.append(Asset(small_deal_card.title,
                                    small_deal_card.card_type,
                                    small_deal_card.price,
                                    0,  # no Down Payment on Small Deal Assets
                                    small_deal_card.cash_flow,
                                    small_deal_card.price_range_low,
                                    small_deal_card.price_range_high))
        else:
            print("Small Card type:", small_deal_card.card_type, "not found")

    while True:
        big_deal_card = big_deal_card_deck.take_top_card()
        if big_deal_card is None:
            break
#        print("Big Deal Card Type: ", big_deal_card.card_type)
        if big_deal_card.card_type in ["ApartmentHouseForSale", "XPlex"]:
            asset_list.append(RealEstate(big_deal_card.title,
                                         big_deal_card.card_type,
                                         big_deal_card.house_or_condo,
                                         big_deal_card.price,
                                         big_deal_card.down_payment,
                                         big_deal_card.cash_flow,
                                         big_deal_card.price_range_low,
                                         big_deal_card.price_range_high,
                                         big_deal_card.units,
                                         0))  # no acres
        elif big_deal_card.card_type == "HouseForSale":
            asset_list.append(RealEstate(big_deal_card.title,
                                         big_deal_card.card_type,
                                         big_deal_card.house_or_condo,
                                         big_deal_card.price,
                                         big_deal_card.down_payment,
                                         big_deal_card.cash_flow,
                                         big_deal_card.price_range_low,
                                         big_deal_card.price_range_high,
                                         0,  # no units
                                         0))  # no acres
        elif big_deal_card.card_type in ["Partnership", "Business"]:
            asset_list.append(Business(big_deal_card.title,
                                       big_deal_card.card_type,
                                       big_deal_card.price,
                                       big_deal_card.down_payment,
                                       big_deal_card.cash_flow,
                                       big_deal_card.price_range_low,
                                       big_deal_card.price_range_high))
        elif big_deal_card.card_type == "Land":
            asset_list.append(RealEstate(big_deal_card.title,
                                         big_deal_card.card_type,
                                         big_deal_card.price,
                                         big_deal_card.down_payment,
                                         big_deal_card.cash_flow,
                                         big_deal_card.price_range_low,
                                         big_deal_card.price_range_high,
                                         0,  # no units
                                         big_deal_card.acres))
        else:
            print("Big Card type:", big_deal_card.card_type, "not found")

    for asset in asset_list:
        print(asset)

if __name__ == '__main__':
    unittest.main(verbosity=2)

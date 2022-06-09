# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

SMALLDEALCARDS_FN = '../game_data/SmallDealCards.json'
BIGDEALCARDS_FN = '../game_data/BigDealCards.json'
DOODADCARDS_FN = '../game_data/DoodadCards.json'
MARKETCARDS_FN = '../game_data/MarketCards.json'


import unittest

class TestCards(unittest.TestCase):
    """Test Class to test Card and Deck objects in cards module."""
    from cashflowsim.cards import (Card, Deck, DoodadCard, MarketCard,
                                   DealCard, SmallDealCard, BigDealCard,
                                   load_all_doodad_cards,load_all_market_cards,
                                   load_all_small_deal_cards,
                                   load_all_big_deal_cards)

    def test_load_card_decks(self):
        print('test_load_card_decks')
        small_deal_card_deck = TestCards.load_all_small_deal_cards(
            SMALLDEALCARDS_FN)
        big_deal_card_deck = TestCards.load_all_big_deal_cards(BIGDEALCARDS_FN)
        doodad_card_deck = TestCards.load_all_doodad_cards(DOODADCARDS_FN)
        market_card_deck = TestCards.load_all_market_cards(MARKETCARDS_FN)

        print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards)
        #    print(small_deal_card_deck)
        print("No. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
        #    print(big_deal_card_deck)
        print("No. of Doodad     Cards: ", doodad_card_deck.no_cards)
        #    print(doodad_card_deck)
        print("No. of Market     Cards: ", market_card_deck.no_cards)
        #    print(market_card_deck)
        print('end test_load_card_decks')

    def test_deal_all_big_deal_cards(self):
        print('test_deal_all_beig_deal_cards')
        big_deal_card_deck = TestCards.load_all_big_deal_cards(BIGDEALCARDS_FN)
        big_deal_card_deck.shuffle()
        while big_deal_card_deck.no_cards > 0:
            card = big_deal_card_deck.take_top_card()
            if card != None:
                print(card)
                print("Number of cards remaining:",
                      big_deal_card_deck.no_cards)
            else:
                raise AttributeError('Ran out of big deal cards unexpectedly')

        big_deal_card_deck = TestCards.load_all_big_deal_cards(BIGDEALCARDS_FN)
        bDCPR = []
        # bDCPRError = []
        bDCROI = []
        while big_deal_card_deck.no_cards > 0:
            big_deal_card = big_deal_card_deck.take_top_card()
            print(big_deal_card.price_range_high,' : ',
                  big_deal_card.price_range_low)
            try:
                bDCPR.append((big_deal_card.price -
                              big_deal_card.price_range_low) /
                             (big_deal_card.price_range_high -
                              big_deal_card.price_range_low))
            except AttributeError:
                print('No Market Value, MAX or MIN on card: ',big_deal_card)
            except ZeroDivisionError:
                print(str(big_deal_card.down_payment)
                      +': No Price Range. Card: ' +
                      big_deal_card.title)
            try:
                bDCROI.append(big_deal_card.cash_flow * 12 /
                              big_deal_card.down_payment)
            except AttributeError:
                print('No ROI on card: ' + big_deal_card.title)
            except ZeroDivisionError:
                print('Zero Down Payement:' + big_deal_card.title)

        """
        bDCPR.sort()
        for aPR in bDCPR:
            print("{:.3f}".format(aPR))
        print("\n\n")
        for aPR in bDCPRError:
            print(aPR)

        bDCROI.sort()

        for anROI in bDCROI:
            print("{:.3f}".format(anROI))
        """
        print('end test_deal_all_beig_deal_cards')

    def test_deal_all_small_deal_cards(self):
        print("test_deal_all_small_deal_cards")
        small_deal_card_deck = TestCards.load_all_small_deal_cards(
            SMALLDEALCARDS_FN)
        while small_deal_card_deck.no_cards > 0:
            card = small_deal_card_deck.take_top_card()
            if card != None:
                print(card)
                print("Number of cards remaining:",
                      small_deal_card_deck.no_cards)
            else:
                raise AttributeError(
                    'Ran out of small deal cards unexpectedly')

        small_deal_card_deck = TestCards.load_all_small_deal_cards(
            SMALLDEALCARDS_FN)
        small_deal_card_deck.shuffle()
        sDCPR = []
        # bDCPRError = []
        sDCROI = []
        while small_deal_card_deck.no_cards > 0:
            small_deal_card = small_deal_card_deck.take_top_card()
            try:
                sDCPR.append((small_deal_card.price -
                              small_deal_card.price_range_low) /
                             (small_deal_card.price_range_high -
                              small_deal_card.price_range_low))
            except AttributeError:
                print('No Market Value, MAX or MIN on card: ' +
                      small_deal_card)
            except ZeroDivisionError:
                print(str(small_deal_card.down_payment) +
                       'No Price Range. Card: ' + small_deal_card.title)
            try:
                sDCROI.append(small_deal_card.cash_flow * 12 /
                              small_deal_card.down_payment)
            except AttributeError:
                print('No ROI on card: ' + small_deal_card.title)
            except ZeroDivisionError:
                print('Zero Down Payement:' + small_deal_card.title)
        print("end test_deal_all_small_deal_cards")

if __name__ == '__main__':
    unittest.main(verbosity=2)

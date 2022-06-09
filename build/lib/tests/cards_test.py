# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

import unittest

class TestCards(unittest.TestCase):
    """Test Class to test Card and Deck objects in cards module."""
    from cards import (Card, Deck, DoodadCard, MarketCard, DealCard,
                       SmallDealCard, BigDealCard, load_all_doodad_cards,
                       load_all_market_cards, load_all_small_deal_cards,
                       load_all_big_deal_cards, )
    small_deal_card_deck = load_all_small_deal_cards("SmallDealCards.json")
    big_deal_card_deck = load_all_big_deal_cards("BigDealCards.json")
    doodad_card_deck = load_all_doodad_cards("DoodadCards.json")
    market_card_deck = load_all_market_cards("MarketCards.json")

    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards)
#    print(small_deal_card_deck)
    print("No. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
#    print(big_deal_card_deck)
    print("No. of Doodad     Cards: ", doodad_card_deck.no_cards)
#    print(doodad_card_deck)
    print("No. of Market     Cards: ", market_card_deck.no_cards)
#    print(market_card_deck)

    bDCPR = []
    bDCPRError = []
    while True:
        big_deal_card = big_deal_card_deck.take_top_card()
        try:
            bDCPR.append((big_deal_card.price -
                          big_deal_card.price_range_low) /
                         (big_deal_card.price_range_high -
                          big_deal_card.price_range_low))
        except AttributeError:
            print("No Market Value, MAX or MIN on card:",
                  big_deal_card)
        except ZeroDivisionError:
            bDCPRError.append((big_deal_card.down_payment,
                               'No Price Range', "Card:" +
                               big_deal_card.title))
        if big_deal_card_deck.no_cards == 0:
            break

    bDCPR.sort()

    for aPR in bDCPR:
        print("{:.3f}".format(aPR))
    print("\n\n")
    for aPR in bDCPRError:
        print(aPR)

    print("\n\n\n")

    bDCROI = []
    big_deal_card_deck = load_all_big_deal_cards("BigDealCards.json")
    while True:
        big_deal_card = big_deal_card_deck.take_top_card()
        try:
            bDCROI.append(big_deal_card.cash_flow * 12 /
                          big_deal_card.down_payment)
        except AttributeError:
            print("No ROI on card:", big_deal_card.title)
        except ZeroDivisionError:
            print("Zero Down Payement:", big_deal_card.title)
        if big_deal_card_deck.no_cards == 0:
            break

    bDCROI.sort()

    for anROI in bDCROI:
        print("{:.3f}".format(anROI))


# TO DO - NEXT TO TRY - DECK METHODS - SHUFFLE, DEAL CARD, ETC. - COMPLETE
"""
    while True:
        card = small_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:",
            small_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    small_deal_card_deck = load_all_small_deal_cards("SmallDealCards.txt")
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = small_deal_card_deck.take_random_card()
        if card != None:
            print(card)
            print("Number of cards remaining:",
            small_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)

    while True:
        card = big_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:", big_deal_card_deck.no_cards)
        else:
            break

    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    big_deal_card_deck = load_all_big_deal_cards("big_deal_cards.txt")
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = big_deal_card_deck.take_random_card()
        if card != None:
            print(card)
            print("Number of cards remaining:", big_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)

    small_deal_card_deck = load_all_small_deal_cards("SmallDealCards.txt")
    big_deal_card_deck = load_all_big_deal_cards("big_deal_cards.txt")
    small_deal_card_deck.shuffle()
    big_deal_card_deck.shuffle()
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = small_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:",
            small_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = big_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:", big_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    print("Small Deck Type:", small_deal_card_deck.getDeckType(),
          "\nBig   Deck Type:", big_deal_card_deck.getDeckType())

"""


if __name__ == '__main__':
    unittest.main(verbosity=2)

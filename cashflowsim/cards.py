"""Manage cards for Game simulation."""
from __future__ import annotations  # requried to create a Deck from Deck method
from cashflowsim.json_read_write_file import load_json
from dataclasses import dataclass, field
from typing import List
import random


@dataclass(slots=True, kw_only=True)
class Card(object):
    """Create card object."""

    title: str


@dataclass(slots=True, kw_only=True)
class DoodadCard(Card):
    """Object to manage Doodad Cards."""

    card_type: str
    one_time_payment: int = 0
    any_child_payment: int = 0
    each_child_payment: int = 0
    loan_title: str = ""
    loan_amount: int = 0
    loan_payment: int = 0

    def __post_init__(self):
        """Create Doodad Card Object."""
        assert (
            (self.card_type == 'OneTimeExpense' and self.one_time_payment > 0)
            or (
                self.card_type == 'ChildCost'
                and ((self.any_child_payment > 0) or (self.each_child_payment > 0))
            )
            or (
                self.card_type == 'NewLoan'
                and self.loan_title != ""
                and self.loan_amount > 0
                and self.loan_payment > 0
            )
        )
        if self.card_type not in ['OneTimeExpense', 'ChildCost', 'NewLoan']:
            print('Card Type: ', self.card_type, 'not found in Card creation')

    def __str__(self):
        """Create string to be returned when str method is called."""
        # Create General part first
        str_text = (
            f'\nTitle:            {self.title}'
            f'\nType:             {self.card_type}'
        )
        match self.card_type:
            case 'OneTimeExpense':
                return ''.join([str_text,
                                f'\nOne Time Payment: {str(self.one_time_payment)}'])
            case 'ChildCost':
                return ''.join([str_text,
                    f'\nAny Child Cost:   {str(self.any_child_payment)}'
                    f'\nEach Child Cost:  {str(self.each_child_payment)}'])
            case 'NewLoan':
                return ''.join([str_text,
                    f'\nLoan Title  :     {self.loan_title}'
                    f'\nLoan Amount :     {str(self.loan_amount)}'
                    f'\nLoan Payment:     {str(self.loan_payment)}'])
            case _:
                print("Card Type: ", self.card_type, " not found in string conversion")
                return ''


@dataclass(slots=True, kw_only=True)
class MarketCard(Card):
    """Object to represent Market Card in Game Simulation."""

    price: int = 0
    added_price: int = 0
    increased_cash_flow: int = 0
    must_sell: bool = False
    self_only: bool = False

    def __post_init__(self):
        """Create Market Card object."""
        assert ((self.price > 0 and self.title in [
            'Condo Buyer - 2Br/1Ba', 'Shopping Mall Wanted',
            'Buyer for 20 Acres', 'Price of Gold Soars', 'Car Wash Buyer',
            'Software Company Buyer', 'Apartment House Buyer',
            'House Buyer - 3Br/2Ba', 'Plex Buyer', 'Limited Partnership Sold',
            'Interest Rates Drop!', 'Inflation Hits!']) or
            (self.title == "Small Business Improves" and self.increased_cash_flow > 0))

        assert (self.title in ['Small Business Improves',
            'Condo Buyer - 2Br/1Ba', 'Shopping Mall Wanted',
            'Buyer for 20 Acres', 'Price of Gold Soars',
            'Car Wash Buyer', 'Software Company Buyer',
            'Apartment House Buyer', 'House Buyer - 3Br/2Ba',
            'Plex Buyer', 'Limited Partnership Sold',
            'Interest Rates Drop!', 'Inflation Hits!'])

    def __str__(self):
        """Create string to be returned when str method is called."""
        match self.title:
            case 'Small Business Improves':
                return (
                    f'\nTitle:                   {self.title}'
                    f'\nIncreased Cash Flow:     {str(self.increased_cash_flow)}'
                    f'\nMust Sell:               {str(self.must_sell)}'
                )
            case ('Condo Buyer - 2Br/1Ba' | 'Shopping Mall Wanted' |
                  'Buyer for 20 Acres' | 'Price of Gold Soars' |
                  'Car Wash Buyer' | 'Software Company Buyer' |
                  'Apartment House Buyer' | 'House Buyer - 3Br/2Ba' |
                  'Plex Buyer'):
                return (f'\nTitle:     {self.title}'
                        f'\nPrice:     {str(self.price)}'
                        f'\nMust Sell: {str(self.must_sell)}'
                )
            case 'Limited Partnership Sold':
                return (f'\nTitle:          {self.title}'
                        f'\nPrice Multiple: {str(self.price)}'
                        f'\nMust Sell:      {str(self.must_sell)}'
                )
            case 'Interest Rates Drop!':
                return (f'\nTitle:       {self.title}'
                        f'\nAdded Price: {str(self.added_price)}'
                        f'\nMust Sell:   {str(self.must_sell)}'
                        f'\nSelf Only:   {str(self.self_only)}'
                )
            case 'Inflation Hits!':
                return (f'\nTitle:          {self.title}'
                        f'\nMust Sell:      {str(self.must_sell)}'
                )
            case _:
                return f'Card Type: {self.title} not found in card string conversion'


@dataclass(slots=True, kw_only=True)
class DealCard(Card):
    """Object to represent Deal Cards in Game Simulations."""

    card_type: str = ''
    house_or_condo: str = ''
    price: int = 0
    down_payment: int = 0
    cash_flow: int = 0
    price_range_low: int = 0
    price_range_high: int = 0
    all_may_buy: bool = False
    acres: int = 0

    def __post_init__(self):
        """Create Deal Card Object."""
        assert self.card_type != "HouseForSale" or self.price > 0


@dataclass(slots=True, kw_only=True)
class SmallDealCard(DealCard):
    """Object to manage Small Deal Cards in Game Simulation."""

    symbol: str = ''
    dividend: int = 0
    split_ratio: float = 1.0

    def __post_init__(self):
        """Create Small Deal Card to be added to Small Deal Deck."""
        available_stocks = ["OK4U", "ON2U", "GRO4US", "2BIG", "MYT4U", "CD"]
        assert (
            (self.card_type == "Stock" and self.symbol in available_stocks and self.price > 0)
            or (
                self.card_type == "StockSplit"
                and self.symbol in available_stocks
                and self.split_ratio > 0
            )
            or (self.price >0 and (self.card_type in ['HouseForSale', 'Asset', 'Land', 'LoanNotToBeRepaid',
            'CostIfRentalProperty', 'StartCompany']))
        )

    def __str__(self):
        """Create string to be returned when str method is called."""
        str_text: str = (
            f'\nSmall Deal Card:'
            f'\nTitle:            {self.title}'
            f'\nType:             {self.card_type}'
        )
        match self.card_type:
            case 'Stock':
                return ''.join([str_text,
                                f'\nSymbol:           {str(self.symbol)}',
                                f'\nPrice:            {str(self.price)}',
                                f'\nDividends:        {str(self.dividend)}',
                                f'\nPrice Range:      {str(self.price_range_low)} - ',
                                f'{str(self.price_range_high)}'])
            case 'StockSplit':
                return ''.join([str_text,
                                f'\nSymbol:           {str(self.symbol)}',
                                f'\nSplit Ratio:      {str(self.split_ratio)}'])
            case 'HouseForSale':
                return ''.join([str_text,
                                f'\nHouse or Condo:   {self.house_or_condo}'
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}',
                                f'\nPrice Range:      {str(self.price_range_low)} - ',
                                f'{str(self.price_range_high)}'])
            case 'Asset':
                return ''.join([str_text,
                                f'\nPrice:            {str(self.price)}',
                                f'\nCash Flow:        {str(self.cash_flow)}',
                                f'\nPrice Range:      {str(self.price_range_low)} - ',
                                f'{str(self.price_range_high)}'])
            case 'Land':
                return ''.join([str_text,
                                f'\nPrice:            {str(self.price)}',
                                f'\nAcres:            {str(self.acres)}'])
            case 'LoanNotToBeRepaid' | 'CostIfRentalProperty':
                return ''.join([str_text,
                                f'\nPrice:            {str(self.price)}'])
            case 'StartCompany':
                return ''.join([str_text,
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}'])
            case _:
                print('Small Deal Card Type: ', self.card_type, ' not found in string conversion')
                return ''


@dataclass(slots=True, kw_only=True)
class BigDealCard(DealCard):
    """Object to manage Big Deal Cards in Game Simulation."""

    units: int = 0
    cost_if_have_real_estate: int = 0
    cost_if_have_8plex: int = 0

    def __post_init__(self):
        assert (
            (
                self.card_type in ["ApartmentHouseForSale", "XPlex"]
                and self.units > 0
                and self.price > 0
            )
            or (self.card_type in ["HouseForSale", "Business"] and self.price > 0)
            or (self.card_type == "Land" and self.acres > 0 and self.price > 0)
            or (
                self.card_type == "Expense"
                and (self.cost_if_have_real_estate > 0 or self.cost_if_have_8plex > 0)
            )
        )

    def __str__(self):
        """Create string to be returned when str method is called."""
        str_text: str = (
            f'\nBig Deal Card:'
            f'\nTitle:            {self.title}'
            f'\nType:             {self.card_type}'
        )
        match self.card_type:
            case 'ApartmentHouseForSale' | 'XPlex':
                return ''.join([str_text,
                                f'\nUnits:            {str(self.units)}',
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}',
                                f'\nPrice Range:      {str(self.price_range_low)} - ',
                                f'{str(self.price_range_high)}'])
            case 'HouseForSale':
                return ''.join([str_text,
                                f'\nHouse or Condo:   {str(self.house_or_condo)}',
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}',
                                f'\nPrice Range:      {str(self.price_range_low)} - ',
                                f'{str(self.price_range_high)}'])
            case 'Partnership' | 'Business':
                return ''.join([str_text,
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}',
                                f'\nPrice Range:      {str(self.price_range_low)} - ',
                                f'{str(self.price_range_high)}'])
            case 'Land':
                return ''.join([str_text,
                                f'\nAcres:            {str(self.acres)}',
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}'])
            case 'Expense':
                return ''.join([str_text,
                                f'\nCost if Have Real Estate: {str(self.cost_if_have_real_estate)}',
                                f'\nCost if Have 8-Plex: {str(self.cost_if_have_8plex)}',
                                f'\nPrice:            {str(self.price)}',
                                f'\nDown Payment:     {str(self.down_payment)}',
                                f'\nCash Flow:        {str(self.cash_flow)}'])
            case _:
                print('Big Deal Card Type: ', self.card_type, ' not found in string conversion')
                return ''


@dataclass(slots=True, kw_only=True)
class Deck(object):
    """Object to hod a Deck of Cards in Game Simulation."""

    deck_type: str
    cards: List[Card] = field(default_factory=list)

    def __post_init__(self):
        pass

    @property
    def no_cards(self) -> int:
        """Find the number of cards."""
        return len(self.cards)

    def add_card(self, card: Card) -> None:
        """Add a card to the deck. This is how you create a deck."""
        self.cards.append(card)
        # return self.no_cards

    def take_random_card(self) -> Card | None:
        """Take a random card from the deck. Wh? We don't know either."""
        try:
            return self.cards.pop(int(random.random() * self.no_cards))
        except IndexError:
            return None

    def take_top_card(self) -> Card | None:
        """Take the top card of a deck. This is what to use."""
        try:
            return self.cards.pop()
        except IndexError:
            return None

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def __copy__(self) -> 'Deck':
        """Copy a deck. So a deck can be created once, and copied for each Monte Carlo run"""
        newDeck = Deck(deck_type=self.deck_type)
        for card in self.cards:
            newDeck.add_card(card)
        return newDeck

    def __str__(self):
        """Create string to be returned when str method is called."""
        return '\n'.join([str(card) for card in self.cards])

def load_all_doodad_cards(doodad_cards_filename: str) -> Deck:
    """Load all Doodad Cards."""
    try:
        doodad_cards_dict = load_json(doodad_cards_filename)
    except OSError:
        print('No good Doodad Cards json file found, file not found, please fix')
        raise OSError
    except ValueError:
        print('No good Doodad Cards json file found, ValueError, please fix')
        raise ValueError

    doodad_card_deck = Deck(deck_type='Doodad Cards')
    for card in doodad_cards_dict:
        if doodad_cards_dict[card]['Type'] == 'OneTimeExpense':
            doodad_card_deck.add_card(
                DoodadCard(
                    title=str(doodad_cards_dict[card]['Title']),
                    card_type=str(doodad_cards_dict[card]['Type']),
                    one_time_payment=int(doodad_cards_dict[card]['Cost']),
                )
            )
        elif doodad_cards_dict[card]['Type'] == 'ChildCost':
            doodad_card_deck.add_card(
                DoodadCard(
                    title=str(doodad_cards_dict[card]['Title']),
                    card_type=str(doodad_cards_dict[card]['Type']),
                    any_child_payment = int(doodad_cards_dict[card]['Cost if any Child']),
                    each_child_payment = int(doodad_cards_dict[card]['Cost per Child']),
                )
            )
        elif doodad_cards_dict[card]['Type'] == 'NewLoan':
            doodad_card_deck.add_card(
                DoodadCard(
                    title=str(doodad_cards_dict[card]['Title']),
                    card_type=str(doodad_cards_dict[card]['Type']),
                    one_time_payment=int(doodad_cards_dict[card]['Down Payment']),
                    loan_title=str(doodad_cards_dict[card]['Loan Name']),
                    loan_amount=int(doodad_cards_dict[card]['Loan Amount']),
                    loan_payment=int(doodad_cards_dict[card]['Payment']),
                )
            )
        else:
            print('Known Doodad card not found in row: ', doodad_cards_dict[card])
    return doodad_card_deck


def load_all_market_cards(market_cards_filename: str) -> Deck:
    """Load all Market Cards from JSON File."""
    try:
        market_cards_dict = load_json(market_cards_filename)
    except OSError:
        print('No good Market Cards json file found, file not found, please fix')
        raise OSError
    except ValueError:
        print('No good Market Cards json file found, ValueError, please fix')
        raise ValueError

    market_card_deck = Deck(deck_type='Market Cards')
    for card in market_cards_dict:
        match market_cards_dict[card]['Title']:
            case 'Small Business Improves':
                market_card_deck.add_card(
                    MarketCard(
                        title=str(market_cards_dict[card]['Title']),
                        increased_cash_flow=int(market_cards_dict[card]['Increased Cash Flow']),
                        must_sell=False,
                        self_only=False,
                    )
                )
            case ('Condo Buyer - 2Br/1Ba' | 'Shopping Mall Wanted' |
                  'Buyer for 20 Acres' | 'Price of Gold Soars' |
                  'Car Wash Buyer' | 'Software Company Buyer' |
                  'Apartment House Buyer' | 'House Buyer - 3Br/2Ba' |
                  'Limited Partnership Sold' | 'Plex Buyer'):
                market_card_deck.add_card(
                    MarketCard(
                        title = str(market_cards_dict[card]['Title']),
                        price=int(market_cards_dict[card]['Cost']),
                        must_sell=True if (
                            str(market_cards_dict[card]['Must Sell']) == 'True') else False
                    )
                )
            case 'Interest Rates Drop!':
                market_card_deck.add_card(
                    MarketCard(
                        title=str(market_cards_dict[card]['Title']),
                        price=int(market_cards_dict[card]['Cost']),
                        must_sell=True if (
                            str(market_cards_dict[card]['Must Sell'])) == 'True' else False,
                        self_only=True if (
                            str(market_cards_dict[card]['Self Only'])) == 'True' else False
                    )
                )
            case 'Inflation Hits!':
                market_card_deck.add_card(
                    MarketCard(
                        title=str(market_cards_dict[card]['Title']),
                        must_sell=True,
                        self_only=True,
                    )
                )
            case _:
                print('Known Market card not found in row: ', market_cards_dict[card])
    return market_card_deck


def load_all_small_deal_cards(small_deal_cards_filename: str) -> Deck:
    """Load all small deal cards for game simulation."""
    try:
        small_deal_cards_dict = load_json(small_deal_cards_filename)
    except OSError:
        print(
            'No good Small Deal Cards json file found, file not found, please fix'
        )
        raise OSError
    except ValueError:
        print('No good Small Deal Cards json file found, ValueError, please fix')
        raise ValueError
    #    else:
    #        noSmallDealCards = len(small_deal_cards_dict)
    #        print(noSmallDealCards, 'Small Deal Cards loaded')

    small_deal_card_deck = Deck(deck_type='Small Deal Cards')
    for card in small_deal_cards_dict:
        match small_deal_cards_dict[card]['Type']:
            case 'Stock':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        symbol=str(small_deal_cards_dict[card]['Symbol']),
                        price=int(small_deal_cards_dict[card]['Cost']),
                        dividend=int(small_deal_cards_dict[card]['Dividend']),
                        price_range_low=int(small_deal_cards_dict[card]['Price Range Low']),
                        price_range_high=int(small_deal_cards_dict[card]['Price Range High']),
                        all_may_buy=True,
                    )
                )
            case 'StockSplit':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        symbol= str(small_deal_cards_dict[card]['Symbol']),
                        split_ratio=float(small_deal_cards_dict[card]['Split Ratio']),
                        all_may_buy=True,
                    )
                )
            case 'HouseForSale':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        house_or_condo=str(small_deal_cards_dict[card]['HouseOrCondo']),
                        price=int(small_deal_cards_dict[card]['Cost']),
                        down_payment=int(small_deal_cards_dict[card]['Down Payment']),
                        cash_flow=int(small_deal_cards_dict[card]['Cash Flow']),
                        price_range_low=int(small_deal_cards_dict[card]['Price Range Low']),
                        price_range_high=int(small_deal_cards_dict[card]['Price Range High']),
                    )
                )
            case 'StartCompany':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        price=int(small_deal_cards_dict[card]['Cost']),
                        down_payment=int(small_deal_cards_dict[card]['Down Payment']),
                        cash_flow=int(small_deal_cards_dict[card]['Cash Flow']),
                    )
                )
            case 'Asset':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        price=int(small_deal_cards_dict[card]['Cost']),
                        cash_flow=int(small_deal_cards_dict[card]['Cash Flow']),
                        price_range_low=int(small_deal_cards_dict[card]['Price Range Low']),
                        price_range_high=int(small_deal_cards_dict[card]['Price Range High']),
                    )
                )
            case 'Land':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        price=int(small_deal_cards_dict[card]['Cost']),
                        down_payment=int(small_deal_cards_dict[card]['Down Payment']),
                        acres=int(small_deal_cards_dict[card]['Acres']),
                    )
                )
            case 'LoanNotToBeRepaid':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        price=int(small_deal_cards_dict[card]['Cost'])
                    )
                )
            case 'CostIfRentalProperty':
                small_deal_card_deck.add_card(
                    SmallDealCard(
                        title=str(small_deal_cards_dict[card]['Title']),
                        card_type=str(small_deal_cards_dict[card]['Type']),
                        price=int(small_deal_cards_dict[card]['Cost'])
                    )
                )
            case _:
                print(
                    'Small Deal Card known card not found in record: ',
                    small_deal_cards_dict[card],
                )
    return small_deal_card_deck


def load_all_big_deal_cards(big_deal_cards_filename: str) -> Deck:
    """Load all Big Deal Cards for Game Simulations."""
    try:
        big_deal_cards_dict = load_json(big_deal_cards_filename)
    except OSError:
        print('No good Big Deal Cards json file found, file not found, please fix')
        raise OSError
    except ValueError:
        print('No good Big Deal Cards json file found, ValueError, please fix')
        raise ValueError
    #    else:
    #        noBigDealCards = len(big_deal_cards_dict)
    #        print(noBigDealCards, 'Big Deal Cards loaded')

    big_deal_card_deck = Deck(deck_type='Big Deal Cards')
    for card in big_deal_cards_dict:
        match big_deal_cards_dict[card]['Type']:
            case 'ApartmentHouseForSale' | 'XPlex':
                big_deal_card_deck.add_card(
                    BigDealCard(
                        title=str(big_deal_cards_dict[card]['Title']),
                        card_type=str(big_deal_cards_dict[card]['Type']),
                        price=int(big_deal_cards_dict[card]['Cost']),
                        down_payment=int(big_deal_cards_dict[card]['Down Payment']),
                        cash_flow=int(big_deal_cards_dict[card]['Cash Flow']),
                        units=int(big_deal_cards_dict[card]['Units']),
                        price_range_low=int(big_deal_cards_dict[card]['Price Range Low']),
                        price_range_high=int(big_deal_cards_dict[card]['Price Range High'])
                    )
                )
            case 'HouseForSale' | 'Business':
                big_deal_card_deck.add_card(
                    BigDealCard(
                        title=str(big_deal_cards_dict[card]['Title']),
                        card_type=str(big_deal_cards_dict[card]['Type']),
                        price=int(big_deal_cards_dict[card]['Cost']),
                        down_payment=int(big_deal_cards_dict[card]['Down Payment']),
                        cash_flow=int(big_deal_cards_dict[card]['Cash Flow']),
                        price_range_low=int(big_deal_cards_dict[card]['Price Range Low']),
                        price_range_high=int(big_deal_cards_dict[card]['Price Range High']),
                    )
                )
            case 'Land':
                big_deal_card_deck.add_card(
                    BigDealCard(
                        title=str(big_deal_cards_dict[card]['Title']),
                        card_type=str(big_deal_cards_dict[card]['Type']),
                        price=int(big_deal_cards_dict[card]['Cost']),
                        down_payment=int(big_deal_cards_dict[card]['Down Payment']),
                        cash_flow=int(big_deal_cards_dict[card]['Cash Flow']),
                        acres=int(big_deal_cards_dict[card]['Acres']),
                    )
                )  # 11-unused-Cost if Have 8-Plex
            case 'Expense':
                big_deal_card_deck.add_card(
                    BigDealCard(
                        title=str(big_deal_cards_dict[card]['Title']),
                        card_type=str(big_deal_cards_dict[card]['Type']),
                        cost_if_have_real_estate=int(
                            big_deal_cards_dict[card]['Cost If Have Real Estate']),
                        cost_if_have_8plex=int(
                            big_deal_cards_dict[card]['Cost If Have 8-Plex']),
                    )
                )
            case _:
                print(
                    'Big Deal Card known card not found in record: ',
                    big_deal_cards_dict[card],
                )
    return big_deal_card_deck

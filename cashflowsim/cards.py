"""Manage cards for Game simulation."""
# from __future__ import annotations  # requried to create a Deck from Deck method
import logging
from cashflowsim.json_read_write_file import load_json
from dataclasses import dataclass, field
from typing import List
import random

log: logging.Logger = logging.getLogger(__name__)


class EmptyDeckError(Exception):
    pass


@dataclass(kw_only=True)
class Card:
    """Create card object."""

    title: str
    category: str
    card_type: str = ""
    acres: int = 0
    added_price: int = 0
    all_may_buy: bool = False
    any_child_payment: int = 0
    cash_flow: int = 0
    cost_if_have_8plex: int = 0
    cost_if_have_real_estate: int = 0
    dividend: int = 0
    down_payment: int = 0
    each_child_payment: int = 0
    house_or_condo: str = ""
    increased_cash_flow: int = 0
    loan_amount: int = 0
    loan_payment: int = 0
    loan_title: str = ""
    must_sell: bool = False
    one_time_payment: int = 0
    price: int = 0
    price_range_high: int = 0
    price_range_low: int = 0
    self_only: bool = False
    split_ratio: float = 1.0
    symbol: str = ""
    units: int = 0

    def __str__(self):
        """Create string to be returned when str method is called."""
        # Create General part first
        str_text = (
            f"\nTitle:            {self.title}"
            f"\nCategory:         {self.category}"
            f"\nType:             {self.card_type}"
        )
        match self.category:
            case "Doodad":
                match self.card_type:
                    case "OneTimeExpense":
                        return "\n".join(
                            [
                                str_text,
                                f"One Time Payment: {self.one_time_payment}",
                            ]
                        )
                    case "ChildCost":
                        return "\n".join(
                            [
                                str_text,
                                f"Any Child Cost:   {self.any_child_payment}",
                                f"Each Child Cost:  {self.each_child_payment}",
                            ]
                        )
                    case "NewLoan":
                        return "\n".join(
                            [
                                str_text,
                                f"Loan Title  :     {self.loan_title}",
                                f"Loan Amount :     {self.loan_amount}",
                                f"Loan Payment:     {self.loan_payment}",
                            ]
                        )
                    case _:
                        err_msg = f"Card Type: {self.card_type} not found in doodad card string conversion"
                        log.error(err_msg)
                        raise ValueError(err_msg)
            case "Market":
                match self.title:
                    case "Small Business Improves":
                        return "\n".join(
                            [
                                str_text,
                                f"Increased Cash Flow:     {self.increased_cash_flow}",
                                f"Must Sell:               {self.must_sell}",
                            ]
                        )

                    case (
                        "Condo Buyer - 2Br/1Ba"
                        | "Shopping Mall Wanted"
                        | "Buyer for 20 Acres"
                        | "Price of Gold Soars"
                        | "Car Wash Buyer"
                        | "Software Company Buyer"
                        | "Apartment House Buyer"
                        | "House Buyer - 3Br/2Ba"
                        | "Plex Buyer"
                    ):
                        return "\n".join(
                            [
                                str_text,
                                f"Price:     {self.price}",
                                f"Must Sell: {self.must_sell}",
                            ]
                        )
                    case "Limited Partnership Sold":
                        return "\n".join(
                            [
                                str_text,
                                f"Price Multiple: {self.price}",
                                f"Must Sell:      {self.must_sell}",
                            ]
                        )
                    case "Interest Rates Drop!":
                        return "\n".join(
                            [
                                str_text,
                                f"Added Price: {self.added_price}",
                                f"Must Sell:   {self.must_sell}",
                                f"Self Only:   {self.self_only}",
                            ]
                        )
                    case "Inflation Hits!":
                        return "\n".join(
                            [
                                str_text,
                                f"Title:          {self.title}",
                                f"Must Sell:      {self.must_sell}",
                            ]
                        )
                    case _:
                        err_msg = f"Card Type: {self.title} not found in market card string conversion"
                        log.error(err_msg)
                        raise ValueError(err_msg)
            case "Small Deal":
                match self.card_type:
                    case "Stock":
                        return "\n".join(
                            [
                                str_text,
                                f"Symbol:           {self.symbol}",
                                f"Price:            {self.price}",
                                f"Dividends:        {self.dividend}",
                                f"Price Range:      {self.price_range_low} - {self.price_range_high}",
                            ]
                        )
                    case "StockSplit":
                        return "\n".join(
                            [
                                str_text,
                                f"Symbol:           {self.symbol}",
                                f"Split Ratio:      {self.split_ratio}",
                            ]
                        )
                    case "HouseForSale":
                        return "\n".join(
                            [
                                str_text,
                                f"House or Condo:   {self.house_or_condo}",
                                f"Price:            {self.price}",
                                f"Down Payment:     {self.down_payment}",
                                f"Cash Flow:        {self.cash_flow}",
                                f"Price Range:      {self.price_range_low} - {self.price_range_high}",
                            ]
                        )
                    case "Asset":
                        return "\n".join(
                            [
                                str_text,
                                f"Price:            {self.price}",
                                f"Cash Flow:        {self.cash_flow}",
                                f"Price Range:      {self.price_range_low} - {self.price_range_high}",
                            ]
                        )
                    case "Land":
                        return "\n".join(
                            [
                                str_text,
                                f"Price:            {self.price}",
                                f"Acres:            {self.acres}",
                            ]
                        )
                    case "LoanNotToBeRepaid" | "CostIfRentalProperty":
                        return "\n".join([str_text, f"Price:            {self.price}"])
                    case "StartCompany":
                        return "\n".join(
                            [
                                str_text,
                                f"Price:            {self.price}",
                                f"Down Payment:     {self.down_payment}",
                                f"Cash Flow:        {self.cash_flow}",
                            ]
                        )
                    case _:
                        err_msg = f"Card Type: {self.card_type} not found in small deal card string conversion"
                        log.error(err_msg)
                        raise ValueError(err_msg)
            case "Big Deal":
                match self.card_type:
                    case "ApartmentHouseForSale" | "XPlex":
                        return "\n".join(
                            [
                                str_text,
                                f"Units:            {self.units}",
                                f"Price:            {self.price}",
                                f"Down Payment:     {self.down_payment}",
                                f"Cash Flow:        {self.cash_flow}",
                                f"Price Range:      {self.price_range_low} - {self.price_range_high}",
                            ]
                        )
                    case "HouseForSale":
                        return "\n".join(
                            [
                                str_text,
                                f"House or Condo:   {self.house_or_condo}",
                                f"Price:            {self.price}",
                                f"Down Payment:     {self.down_payment}",
                                f"Cash Flow:        {self.cash_flow}",
                                f"Price Range:      {self.price_range_low} - {self.price_range_high}",
                            ]
                        )
                    case "Partnership" | "Business":
                        return "".join(
                            [
                                str_text,
                                f"Price:            {self.price}",
                                f"Down Payment:     {self.down_payment}",
                                f"Cash Flow:        {self.cash_flow}",
                                f"Price Range:      {self.price_range_low} - {self.price_range_high}",
                            ]
                        )
                    case "Land":
                        return "".join(
                            [
                                str_text,
                                f"Acres:            {self.acres}",
                                f"Price:            {self.price}",
                                f"Down Payment:     {self.down_payment}",
                                f"Cash Flow:        {self.cash_flow}",
                            ]
                        )
                    case "Expense":
                        return "\n".join(
                            [
                                str_text,
                                f"Cost if Have Real Estate: {self.cost_if_have_real_estate}",
                                f"Cost if Have 8-Plex:      {self.cost_if_have_8plex}",
                                f"Price:                    {self.price}",
                                f"Down Payment:             {self.down_payment}",
                                f"Cash Flow:                {self.cash_flow}",
                            ]
                        )
                    case _:
                        err_msg = f"Card Type: {self.card_type} not found in big deal card string conversion"
                        log.warning(err_msg)
                        raise ValueError(err_msg)
            case _:
                err_msg = f"Card Category: {self.category} not one of standard types"
                log.error(err_msg)
                raise ValueError(err_msg)


@dataclass(kw_only=True)
class CardDeck:
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

    def take_top_card(self) -> Card:
        """Take the top card of a deck. This is what to use."""
        try:
            log.info(f"Card taken:\n{self.cards[0]}. len(self.cards) remaining.")
            return self.cards.pop(0)
        except IndexError:
            log.error(f"No card taken. Deck is empty")
            raise EmptyDeckError(f"Deck is empty!")

    def shuffle(self) -> None:
        """Shuffle the deck."""
        log.info(f"Shuffling the deck: {self.deck_type}")
        random.shuffle(self.cards)

    def __str__(self):
        """Create string to be returned when str method is called."""
        return "\n".join([f"{card}" for card in self.cards])


def load_all_doodad_cards(*, doodad_cards_filename: str) -> CardDeck:
    """Load all Doodad Cards."""
    try:
        cards_dict: dict[str, dict[str, str]] = load_json(
            file_name=doodad_cards_filename
        )
    except OSError:
        err_msg = f"No good Doodad Cards json file found, file not found, please fix"
        log.error(f"{err_msg}\nFile name: {doodad_cards_filename}")
        raise OSError(err_msg)
    except ValueError:
        err_msg = f"No good Doodad Cards json file found, ValueError, please fix"
        log.error(f"{err_msg}\nFile name: {doodad_cards_filename}")
        raise ValueError(err_msg)

    card_deck: CardDeck = CardDeck(deck_type="Doodad")
    for card in cards_dict:
        match cards_dict[card]["Type"]:
            case "OneTimeExpense":
                new_card: Card = Card(
                    category="Doodad",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    one_time_payment=int(cards_dict[card]["Cost"]),
                )

            case "ChildCost":
                new_card: Card = Card(
                    category="Doodad",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    any_child_payment=int(cards_dict[card]["Cost if any Child"]),
                    each_child_payment=int(cards_dict[card]["Cost per Child"]),
                )
            case "NewLoan":
                new_card: Card = Card(
                    category="Doodad",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    one_time_payment=int(cards_dict[card]["Down Payment"]),
                    loan_title=str(cards_dict[card]["Loan Name"]),
                    loan_amount=int(cards_dict[card]["Loan Amount"]),
                    loan_payment=int(cards_dict[card]["Payment"]),
                )
            case _:
                raise ValueError(
                    f"Known Doodad card not found in row: {cards_dict[card]}"
                )

        assert (
            (new_card.card_type == "OneTimeExpense" and new_card.one_time_payment > 0)
            or (
                new_card.card_type == "ChildCost"
                and (
                    (new_card.any_child_payment > 0)
                    or (new_card.each_child_payment > 0)
                )
            )
            or (
                new_card.card_type == "NewLoan"
                and new_card.loan_title != ""
                and new_card.loan_amount > 0
                and new_card.loan_payment > 0
            )
        )
        card_deck.add_card(new_card)

    return card_deck


def load_all_market_cards(*, market_cards_filename: str) -> CardDeck:
    """Load all Market Cards from JSON File."""
    try:
        cards_dict: dict[str, dict[str, str]] = load_json(
            file_name=market_cards_filename
        )
    except OSError:
        err_msg = f"No good Market Cards json file found, file not found, please fix"
        log.error(f"{err_msg}\nFile name: {market_cards_filename}")
        raise OSError(err_msg)
    except ValueError:
        err_msg = f"No good Market Cards json file found, ValueError, please fix"
        log.error(f"{err_msg}\nFile name: {market_cards_filename}")
        raise ValueError(err_msg)

    card_deck: CardDeck = CardDeck(deck_type="Market")
    for card in cards_dict:
        match cards_dict[card]["Title"]:
            case "Small Business Improves":
                new_card: Card = Card(
                    category="Market",
                    title=str(cards_dict[card]["Title"]),
                    increased_cash_flow=int(cards_dict[card]["Increased Cash Flow"]),
                    must_sell=False,
                    self_only=False,
                )
                assert new_card.increased_cash_flow > 0
            case (
                "Condo Buyer - 2Br/1Ba"
                | "Shopping Mall Wanted"
                | "Buyer for 20 Acres"
                | "Price of Gold Soars"
                | "Car Wash Buyer"
                | "Software Company Buyer"
                | "Apartment House Buyer"
                | "House Buyer - 3Br/2Ba"
                | "Limited Partnership Sold"
                | "Plex Buyer"
            ):
                new_card: Card = Card(
                    category="Market",
                    title=str(cards_dict[card]["Title"]),
                    price=int(cards_dict[card]["Cost"]),
                    must_sell=str(cards_dict[card]["Must Sell"]) == "True",
                )
                assert new_card.price >= 0
            case "Interest Rates Drop!":
                new_card: Card = Card(
                    category="Market",
                    title=str(cards_dict[card]["Title"]),
                    price=int(cards_dict[card]["Cost"]),
                    must_sell=str(cards_dict[card]["Must Sell"]) == "True",
                    self_only=str(cards_dict[card]["Self Only"]) == "True",
                )
                assert new_card.price >= 0
            case "Inflation Hits!":
                new_card: Card = Card(
                    category="Market",
                    title=str(cards_dict[card]["Title"]),
                    must_sell=True,
                    self_only=True,
                )
            case _:
                raise ValueError(
                    f"Known Market card not found in row: {cards_dict[card]}"
                )

        card_deck.add_card(new_card)

    return card_deck


def load_all_small_deal_cards(*, small_deal_cards_filename: str) -> CardDeck:
    """Load all small deal cards for game simulation."""
    try:
        cards_dict: dict[str, dict[str, str]] = load_json(
            file_name=small_deal_cards_filename
        )
    except OSError:
        err_msg = (
            f"No good Small Deal Cards json file found, file not found, please fix"
        )
        log.error(f"{err_msg}\nFile name: {small_deal_cards_filename}")
        raise OSError(err_msg)
    except ValueError:
        err_msg = f"No good Small Deal Cards json file found, ValueError, please fix"
        log.error(f"{err_msg}\nFile name: {small_deal_cards_filename}")
        raise ValueError(err_msg)

    card_deck: CardDeck = CardDeck(deck_type="Small Deal")
    for card in cards_dict:
        match cards_dict[card]["Type"]:
            case "Stock":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    symbol=str(cards_dict[card]["Symbol"]),
                    price=int(cards_dict[card]["Cost"]),
                    dividend=int(cards_dict[card]["Dividend"]),
                    price_range_low=int(cards_dict[card]["Price Range Low"]),
                    price_range_high=int(cards_dict[card]["Price Range High"]),
                    all_may_buy=True,
                )
            case "StockSplit":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    symbol=str(cards_dict[card]["Symbol"]),
                    split_ratio=float(cards_dict[card]["Split Ratio"]),
                    all_may_buy=True,
                )
            case "HouseForSale":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    house_or_condo=str(cards_dict[card]["HouseOrCondo"]),
                    price=int(cards_dict[card]["Cost"]),
                    down_payment=int(cards_dict[card]["Down Payment"]),
                    cash_flow=int(cards_dict[card]["Cash Flow"]),
                    price_range_low=int(cards_dict[card]["Price Range Low"]),
                    price_range_high=int(cards_dict[card]["Price Range High"]),
                )
            case "StartCompany":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                    down_payment=int(cards_dict[card]["Down Payment"]),
                    cash_flow=int(cards_dict[card]["Cash Flow"]),
                )
            case "Asset":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                    cash_flow=int(cards_dict[card]["Cash Flow"]),
                    price_range_low=int(cards_dict[card]["Price Range Low"]),
                    price_range_high=int(cards_dict[card]["Price Range High"]),
                )
            case "Land":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                    down_payment=int(cards_dict[card]["Down Payment"]),
                    acres=int(cards_dict[card]["Acres"]),
                )
            case "LoanNotToBeRepaid":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                )
            case "CostIfRentalProperty":
                new_card: Card = Card(
                    category="Small Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                )
            case _:
                raise ValueError(
                    f"Known Small Deal card not found in row: {cards_dict[card]}"
                )

        assert new_card.card_type != "HouseForSale" or new_card.price > 0

        AVAILABLE_STOCKS: list[str] = ["OK4U", "ON2U", "GRO4US", "2BIG", "MYT4U", "CD"]
        assert (
            (
                new_card.card_type == "Stock"
                and new_card.symbol in AVAILABLE_STOCKS
                and new_card.price > 0
            )
            or (
                new_card.card_type == "StockSplit"
                and new_card.symbol in AVAILABLE_STOCKS
                and new_card.split_ratio > 0
            )
            or (
                new_card.price > 0
                and (
                    new_card.card_type
                    in [
                        "HouseForSale",
                        "Asset",
                        "Land",
                        "LoanNotToBeRepaid",
                        "CostIfRentalProperty",
                        "StartCompany",
                    ]
                )
            )
        )

        card_deck.add_card(new_card)

    return card_deck


def load_all_big_deal_cards(*, big_deal_cards_filename: str) -> CardDeck:
    """Load all Big Deal Cards for Game Simulations."""
    try:
        cards_dict: dict[str, dict[str, str]] = load_json(
            file_name=big_deal_cards_filename
        )
    except OSError:
        err_msg = f"No good Big Deal Cards json file found, file not found, please fix"
        log.error(f"{err_msg}\nFile name: {big_deal_cards_filename}")
        raise OSError(err_msg)
    except ValueError:
        err_msg = f"No good Big Deal Cards json file found, ValueError, please fix"
        log.error(f"{err_msg}\nFile name: {big_deal_cards_filename}")
        raise ValueError(err_msg)

    card_deck: CardDeck = CardDeck(deck_type="Big Deal")
    for card in cards_dict:
        match cards_dict[card]["Type"]:
            case "ApartmentHouseForSale" | "XPlex":
                new_card: Card = Card(
                    category="Big Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                    down_payment=int(cards_dict[card]["Down Payment"]),
                    cash_flow=int(cards_dict[card]["Cash Flow"]),
                    units=int(cards_dict[card]["Units"]),
                    price_range_low=int(cards_dict[card]["Price Range Low"]),
                    price_range_high=int(cards_dict[card]["Price Range High"]),
                )
            case "HouseForSale" | "Business":
                new_card: Card = Card(
                    category="Big Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                    down_payment=int(cards_dict[card]["Down Payment"]),
                    cash_flow=int(cards_dict[card]["Cash Flow"]),
                    price_range_low=int(cards_dict[card]["Price Range Low"]),
                    price_range_high=int(cards_dict[card]["Price Range High"]),
                )
            case "Land":
                new_card: Card = Card(
                    category="Big Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    price=int(cards_dict[card]["Cost"]),
                    down_payment=int(cards_dict[card]["Down Payment"]),
                    cash_flow=int(cards_dict[card]["Cash Flow"]),
                    acres=int(cards_dict[card]["Acres"]),
                )
            case "Expense":
                new_card: Card = Card(
                    category="Big Deal",
                    title=str(cards_dict[card]["Title"]),
                    card_type=str(cards_dict[card]["Type"]),
                    cost_if_have_real_estate=int(
                        cards_dict[card]["Cost If Have Real Estate"]
                    ),
                    cost_if_have_8plex=int(cards_dict[card]["Cost If Have 8-Plex"]),
                )
            case _:
                raise ValueError(
                    f"Known Big Deal card not found in row: {cards_dict[card]}"
                )

        assert (
            (
                new_card.card_type in ["ApartmentHouseForSale", "XPlex"]
                and new_card.units > 0
                and new_card.price > 0
            )
            or (
                new_card.card_type in ["HouseForSale", "Business"]
                and new_card.price > 0
            )
            or (
                new_card.card_type == "Land"
                and new_card.acres > 0
                and new_card.price > 0
            )
            or (
                new_card.card_type == "Expense"
                and (
                    new_card.cost_if_have_real_estate > 0
                    or new_card.cost_if_have_8plex > 0
                )
            )
        )

        card_deck.add_card(new_card)

    return card_deck

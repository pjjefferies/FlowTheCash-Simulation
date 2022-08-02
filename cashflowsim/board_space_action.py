# -*- coding: utf-8 -*-
"""Simulate Game: This is where all the action is for simulating game."""

# from cmath import pi
import logging

# from cv2 import error

logger = logging.getLogger(__name__)

from cashflowsim.player_choice import (
    choose_small_or_big_deal_card,
    choose_to_donate_to_charity,
    choose_to_sell_asset,
    choose_to_buy_asset,
    choose_to_buy_stock_asset,
)

from cashflowsim.loans import Loan
from cashflowsim.assets import RealEstate, Business, Stock  # , Asset
from cashflowsim.player import Player
from cashflowsim.cards import (
    Card,
    CardDeck,
)
from cashflowsim.board import Board, BoardSpace

log = logging.getLogger(__name__)


def board_space_action(
    *,
    player: Player,
    new_board_space: BoardSpace,
    small_deal_card_deck: CardDeck,
    big_deal_card_deck: CardDeck,
    doodad_card_deck: CardDeck,
    market_card_deck: CardDeck,
    board: Board,
) -> None:
    """Determine what action is needed for board space and make it so."""
    log.info(f"Board Space: {new_board_space}")
    space_type = new_board_space.board_space_type
    log.info(f"Board Space Type: {space_type}")
    match space_type:
        case "Opportunity":
            small_or_big_card = choose_small_or_big_deal_card(a_player=player)
            if small_or_big_card == "small":
                picked_small_card: Card = small_deal_card_deck.take_top_card()
                # Assuming there are cards in deck because it has been verified elsewhere

                logging.info(
                    f"Small Deal Picked Card: {picked_small_card}\n"
                    f"No. Cards left: {small_deal_card_deck.no_cards}"
                )
                do_small_deal_action(
                    a_player=player, picked_card=picked_small_card, board=board
                )
            else:  # Assume small_or_big_card=="big":
                picked_big_card: Card = big_deal_card_deck.take_top_card()
                log.info(
                    f"Big Deal Picked Card: {picked_big_card}\n"
                    f"No. Cards left: {big_deal_card_deck.no_cards}"
                )
                do_big_deal_action(a_player=player, picked_card=picked_big_card)
        case "Doodads":
            picked_doodad_card: Card = doodad_card_deck.take_top_card()
            log.info(
                f"Doodad Picked Card: {picked_doodad_card}\n"
                f"No. Cards left: {doodad_card_deck.no_cards}"
            )
            do_doodad_action(player=player, picked_card=picked_doodad_card)
        case "Charity":
            donate_to_charity_choice = choose_to_donate_to_charity(
                a_strategy=player.strategy
            )
            if donate_to_charity_choice:
                if player.savings > 0.1 * player.salary:
                    player.make_payment(payment=int(0.1 * player.salary))
                    player.start_charity_turns()
                    log.info("Charity started")
                else:
                    log.info("Sorry, you don't have enough money for charity")
        case "Pay Check":
            return  # Paycheck handled if passed or landed-on in main routine
        case "The Market":
            picked_market_card: Card = market_card_deck.take_top_card()
            log.info(
                f"Market Picked Card: {picked_market_card} \n"
                f"No. Cards left: {market_card_deck.no_cards}"
            )
            do_market_action(
                a_player=player, board=board, picked_card=picked_market_card
            )
        case "Baby":
            children = player.no_children
            player.have_child()
            log.info(
                f"Children-Before: {children} Children-After: {player.no_children}"
            )
            return
        case "Downsized":
            log.info(f"Player {player.name} downsized")
            player.refresh()
            total_expenses = player.total_expenses
            if total_expenses > player.savings:
                new_loan_amount = (
                    int(
                        ((float(total_expenses) - float(player.savings)) / 1000.0) + 1.0
                    )
                    * 1000
                )
                log.info(f"Not enough money, getting loan for {new_loan_amount}.")
                new_loan = Loan(
                    name="Bank Loan",
                    balance=new_loan_amount,
                    monthly_payment=int(new_loan_amount / 10),
                    partial_payment_allowed=True,
                )
                player.make_loan(loan=new_loan)
            log.info(
                f"Player making payment of {total_expenses} with savings of {player.savings}."
            )
            player.make_payment(payment=total_expenses)
            log.info(f"Player starting layoff")
            player.start_layoff()
        case _:
            raise ValueError(f"Board Space Type unknown: {space_type}")


def do_market_action(*, a_player: Player, board: Board, picked_card: Card) -> None:
    """Do action indicated on Market Card."""
    picked_card_type = picked_card.title
    log.info(f"In do_market_action: Card: {picked_card_type}")
    match picked_card_type:
        case "Small Business Improves":
            for player in board.players:
                log.info(f"Looking at player: {player.name}")
                for asset in player.business_assets:
                    log.info(
                        f"Looking at asset: {asset.name}, asset_type: {asset.asset_type}"
                    )
                    if asset.asset_type == "StartCompany":
                        asset.increase_cash_flow(
                            increase_amount=picked_card.increased_cash_flow
                        )
                        log.info(
                            f"\nPlayer {player.name} increased cash flow on asset {asset.name}"
                            f" by {picked_card.increased_cash_flow} to {asset.cash_flow}."
                        )
        case "Condo Buyer - 2Br/1Ba":
            for player in board.players:
                log.info(f"Evaluate Condo Buyer for player {player.name}")
                for asset in player.real_estate_assets:
                    log.info(f"Evaluating Real Estate Asset: {asset.name}")
                    if asset.house_or_condo == "Condo":
                        log.info(f"Have a Condo, choosing whether to sell...")
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            log.info(f"Chose to sell Condo")
                            player.sell_real_estate(
                                asset=asset, price=picked_card.price
                            )
        case "Shopping Mall Wanted":
            log.info(f"Shopping Mall Wanted")
            for player in board.players:
                log.info(f"Evaluate Shopping Mall Wanted for player {player.name}")
                for asset in player.business_assets:
                    log.info(f"Evaluating Business Asset: {asset.name}")
                    if asset.name == "Small Shopping Mall for Sale":
                        log.info(f"Have a Shopping Mall, choosing whether to sell...")
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            log.info(f"Chose to sell Shopping Mall")
                            player.sell_business(asset=asset, price=picked_card.price)
        case "Buyer for 20 Acres":
            log.info(f"Buyer for 20 Acres")
            for player in board.players:
                log.info(f"Evaluate Buyer for 20 Acres for player {player.name}")
                for asset in player.real_estate_assets:
                    log.info(f"Evaluating Real Estate Asset: {asset.name}")
                    if asset.name == "20 Acres for Sale":
                        log.info(f"Have a 20 Acres, choosing whether to sell...")
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            log.info(f"Chose to sell land")
                            player.sell_real_estate(
                                asset=asset, price=picked_card.price
                            )
        case "Price of Gold Soars":
            log.info(f"Price of Gold Soars")
            for player in board.players:
                log.info(f"Evaluate Buyer for Gold for player {player.name}")
                for asset in player.business_assets:
                    log.info(f"Evaluating Business Asset: {asset.name}")
                    if asset.name == "Rare Gold Coin":
                        log.info(f"Have a Rare Gold Coin, choosing whether to sell...")
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            log.info(f"Chose to sell Gold Coin")
                            player.sell_business(asset=asset, price=picked_card.price)
        case "Car Wash Buyer":
            log.info(f"Car Wash Buyer")
            for player in board.players:
                log.info(f"Evaluate Buyer for Car Wash for player {player.name}")
                for asset in player.business_assets:
                    log.info(f"Evaluating Business Asset: '{asset.name}'")
                    if asset.name == "Car Wash for Sale":
                        log.info(f"Have a Car Wash, choosing whether to sell...")
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            log.info(f"Chose to sell Car Wash")
                            player.sell_business(asset=asset, price=picked_card.price)
        case "Software Company Buyer":
            for player in board.players:
                for asset in player.business_assets:
                    if asset.name == "Start a Company Part Time":
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            player.sell_business(asset=asset, price=picked_card.price)
        case "Apartment House Buyer":
            for player in board.players:
                for asset in player.real_estate_assets:
                    if asset.asset_type == "ApartmentHouseForSale":
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price * asset.units,
                            delta_price=0,
                        ):
                            player.sell_real_estate(
                                asset=asset, price=picked_card.price * asset.units
                            )
        case "House Buyer - 3Br/2Ba":
            for player in board.players:
                for asset in player.real_estate_assets:
                    if asset.name == "House for Sale - 3Br/2Ba":
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price,
                            delta_price=0,
                        ):
                            player.sell_real_estate(
                                asset=asset, price=picked_card.price
                            )
        case "Plex Buyer":
            for player in board.players:
                for asset in player.real_estate_assets:
                    if asset.asset_type == "XPlex":
                        if choose_to_sell_asset(
                            a_player=player,
                            asset=asset,
                            price=picked_card.price * asset.units,
                            delta_price=0,
                        ):
                            player.sell_real_estate(
                                asset=asset,
                                price=picked_card.price * asset.units,
                            )
        case "Limited Partnership Sold":
            for player in board.players:
                for asset in player.business_assets:
                    if asset.name == "Limited Partner Wanted":
                        log.info(
                            f"Player {player.name} has {asset.name} and it must be sold"
                        )
                        player.sell_business(
                            asset=asset, price=picked_card.price * asset.cost
                        )
        case "Interest Rates Drop!":
            for real_estate_asset in a_player.real_estate_assets:
                if real_estate_asset.house_or_condo == "House":
                    if choose_to_sell_asset(
                        a_player=a_player,
                        asset=real_estate_asset,
                        price=picked_card.price,
                        delta_price=0,
                    ):
                        a_player.sell_real_estate(
                            asset=real_estate_asset,
                            price=real_estate_asset.cost + 50000,
                        )
        case "Inflation Hits!":
            for real_estate_asset in a_player.real_estate_assets:
                if real_estate_asset.house_or_condo == "House":
                    a_player.sell_real_estate(
                        asset=real_estate_asset,
                        price=0,
                    )
        case _:
            err_msg = f"Market card type {picked_card_type} is not valid"
            log.error(err_msg)
            raise ValueError(err_msg)


def do_big_deal_action(*, a_player: Player, picked_card: Card) -> None:
    """Do a Big Deal Action indicated on Big Deal Cards."""
    picked_card_type = picked_card.card_type
    log.info(
        f"In do_big_deal_action, Savings: {a_player.savings},\nCard: {picked_card.title}"
    )

    match picked_card_type:
        case "ApartmentHouseForSale" | "XPlex":
            new_real_estate_asset = RealEstate(
                name=picked_card.title,
                asset_type=picked_card_type,
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=picked_card.cash_flow,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
                house_or_condo=picked_card.house_or_condo,
                units=picked_card.units,
                acres=0,
            )
            if choose_to_buy_asset(
                a_player=a_player,
                asset=new_real_estate_asset,
                price=new_real_estate_asset.cost,
            ):
                a_player.buy_real_estate(real_estate_asset=new_real_estate_asset)
            else:
                del new_real_estate_asset
        case "Business":
            new_business_asset = Business(
                name=picked_card.title,
                asset_type=picked_card_type,
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=picked_card.cash_flow,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
            )
            if choose_to_buy_asset(
                a_player=a_player,
                asset=new_business_asset,
                price=new_business_asset.cost,
            ):
                a_player.buy_business(business_asset=new_business_asset)
            else:
                del new_business_asset
        case "HouseForSale":
            new_house_asset = RealEstate(
                name=picked_card.title,
                asset_type=picked_card_type,
                house_or_condo="House",
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=picked_card.cash_flow,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
                units=0,
                acres=0,
            )
            if choose_to_buy_asset(
                a_player=a_player, asset=new_house_asset, price=new_house_asset.cost
            ):
                a_player.buy_real_estate(real_estate_asset=new_house_asset)
            else:
                del new_house_asset
        case "Land":
            new_land_asset = RealEstate(
                name=picked_card.title,
                asset_type=picked_card_type,
                house_or_condo="None",
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=0,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
                units=0,
                acres=picked_card.acres,
            )
            if choose_to_buy_asset(a_player=a_player, asset=new_land_asset):
                a_player.buy_real_estate(real_estate_asset=new_land_asset)
            else:
                del new_land_asset
        case "Expense":
            log.info(f"In Big Card:Expense")
            if picked_card.cost_if_have_real_estate > 0:
                log.info(
                    f"tbsa:408:Number of real estate assets: {len(a_player.real_estate_assets)}"
                )
                for real_estate_asset in a_player.real_estate_assets:
                    log.info(f"Evaluating real estate asset: {real_estate_asset.name}")
                    if real_estate_asset.asset_type in [
                        "HouseForSale",
                        "ApartmentHouseForSale",
                        "XPlex",
                    ]:
                        a_player.make_payment(
                            payment=picked_card.cost_if_have_real_estate
                        )
                        log.info(f"Asset Type: {real_estate_asset.asset_type}")
                        log.info(f"Payed for damage on asset: {real_estate_asset.name}")
            elif picked_card.cost_if_have_8plex > 0:
                log.info(
                    f"tbsa:424:Number of real estate assets: {len(a_player.real_estate_assets)}"
                )
                for real_estate_asset in a_player.real_estate_assets:
                    if real_estate_asset.name == "8-plex for Sale":
                        log.info(f"Have an 8-plex for Sale, making paymetn")
                        a_player.make_payment(payment=picked_card.cost_if_have_8plex)
            else:
                err_msg = f"Big Deal card with type: 'Expense' is not valid"
                log.error(err_msg)
                raise ValueError(err_msg)
        case _:
            raise ValueError("Big Deal Card Type Not Found")
    log.info(f"End of do_big_deal_action")


def do_small_deal_action(*, a_player: Player, picked_card: Card, board: Board):
    """Do action indicated on Small Deal Card."""
    picked_card_type: str = picked_card.card_type
    log.info(
        f"In do_small_deal_action, Savings: {a_player.savings}, Card: {picked_card.title}"
    )

    match picked_card_type:
        case "Stock":
            new_stock: Stock = Stock(
                name=picked_card.symbol,
                asset_type="Stock",
                cost_per_share=picked_card.price,
                cash_flow=picked_card.dividend,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
            )
            # print(f"new_stock:\n{new_stock}")
            if not choose_to_buy_stock_asset(a_player=a_player, new_stock=new_stock):
                del new_stock
                return
            log.info(f"Chose to buy {new_stock.shares} shares of {new_stock.name}")
            a_player.buy_stock(stock_asset=new_stock, cost_per_share=picked_card.price)

        case "StockSplit":
            for each_player in board.players:
                list_of_stocks: list[Stock] = each_player.stock_assets
                for each_stock in list_of_stocks:
                    if each_stock.name == picked_card.symbol:
                        each_stock.stock_split(picked_card.split_ratio)
        #
        case "HouseForSale":
            new_house_asset = RealEstate(
                name=picked_card.title,
                asset_type=picked_card_type,
                house_or_condo=picked_card.house_or_condo,
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=picked_card.cash_flow,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
                units=0,
                acres=0,
            )
            if choose_to_buy_asset(a_player=a_player, asset=new_house_asset):
                a_player.buy_real_estate(real_estate_asset=new_house_asset)
            else:
                del new_house_asset
        case "StartCompany" | "Asset":
            new_business_asset: Business = Business(
                name=picked_card.title,
                asset_type=picked_card_type,
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=picked_card.cash_flow,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
            )
            if choose_to_buy_asset(a_player=a_player, asset=new_business_asset):
                a_player.buy_business(business_asset=new_business_asset)
            else:
                del new_business_asset
        case "Land":
            new_land_asset: RealEstate = RealEstate(
                name=picked_card.title,
                asset_type=picked_card_type,
                house_or_condo="None",
                cost=picked_card.price,
                down_payment=picked_card.down_payment,
                cash_flow=0,
                price_range_low=picked_card.price_range_low,
                price_range_high=picked_card.price_range_high,
                units=0,
                acres=picked_card.acres,
            )
            if choose_to_buy_asset(a_player=a_player, asset=new_land_asset):
                a_player.buy_real_estate(real_estate_asset=new_land_asset)
            else:
                del new_land_asset
        case "LoanNotToBeRepaid":
            loan_not_to_be_repaid_amount = picked_card.price
            if a_player.savings < loan_not_to_be_repaid_amount:
                new_loan_amount = (
                    int(
                        (
                            (
                                float(loan_not_to_be_repaid_amount)
                                - float(a_player.savings)
                            )
                            / 1000
                        )
                        + 1
                    )
                    * 1000
                )
                log.info(f"Not enough money, getting loan for {new_loan_amount}.")
                new_loan: Loan = Loan(
                    name="Bank Loan",
                    balance=new_loan_amount,
                    monthly_payment=int(new_loan_amount / 10),
                    partial_payment_allowed=True,
                )
                a_player.make_loan(loan=new_loan)
            a_player.make_payment(payment=loan_not_to_be_repaid_amount)
        case "CostIfRentalProperty":
            cost_if_rental_property_amount = picked_card.price
            the_players = board.players
            for each_player in the_players:
                if len(each_player.real_estate_assets) > 0:
                    if each_player.savings < cost_if_rental_property_amount:
                        new_loan_amount = (
                            int(
                                (
                                    (
                                        float(
                                            cost_if_rental_property_amount
                                            - each_player.savings
                                        )
                                    )
                                    / 1000
                                )
                                + 1
                            )
                            * 1000
                        )
                        log.info(
                            f"Not enough money, getting loan for {new_loan_amount}."
                        )
                        new_loan: Loan = Loan(
                            name="Bank Loan",
                            balance=new_loan_amount,
                            monthly_payment=int(new_loan_amount / 10),
                            partial_payment_allowed=True,
                        )
                        each_player.make_loan(loan=new_loan)
                    each_player.make_payment(payment=cost_if_rental_property_amount)
        case _:
            raise ValueError(
                f"Small Deal Option Card not in expected types: {picked_card_type}"
            )


def do_doodad_action(*, player: Player, picked_card: Card):
    """Do action on Doodad Card."""
    log.info(
        f"In do_doodad_action, Savings: {player.savings}, Card: {picked_card.title}"
    )

    match picked_card.card_type:
        case "OneTimeExpense":
            payment: int = picked_card.one_time_payment
            if player.savings < payment:
                new_loan_amount = (
                    int(((float(payment) - float(player.savings)) / 1000) + 1) * 1000
                )
                new_loan: Loan = Loan(
                    name="Bank Loan",
                    balance=new_loan_amount,
                    monthly_payment=int(new_loan_amount / 10),
                    partial_payment_allowed=True,
                )
                player.make_loan(loan=new_loan)
            savings_before: int = player.savings
            player.make_payment(payment=payment)
            log.info(
                f"Making payment of {payment}\nSavings before: {savings_before}\nSavings after: {player.savings}"
            )
        case "ChildCost":
            any_cost_per_child: int = picked_card.any_child_payment
            per_cost_per_child: int = picked_card.each_child_payment
            no_children: int = player.no_children
            if no_children > 0:
                log.info("You have kids, you must pay")
                payment = any_cost_per_child + no_children * per_cost_per_child
                if player.savings < payment:
                    new_loan_amount = (
                        int(((float(payment) - float(player.savings)) / 1000) + 1)
                        * 1000
                    )
                    new_loan = Loan(
                        name="Bank Loan",
                        balance=new_loan_amount,
                        monthly_payment=int(new_loan_amount / 10),
                        partial_payment_allowed=True,
                    )
                    player.make_loan(loan=new_loan)
                player.make_payment(payment=payment)
            else:
                log.info("No kids, no payment required")
        case "NewLoan":
            new_loan_amount: int = picked_card.loan_amount
            new_loan: Loan = Loan(
                name=picked_card.loan_title,
                balance=new_loan_amount,
                monthly_payment=picked_card.loan_payment,
                partial_payment_allowed=False,
            )
            player.make_loan(loan=new_loan)
            player.make_payment(payment=new_loan_amount + picked_card.one_time_payment)
        case _:
            raise ValueError(
                f"Doodad Card type not recognized: {picked_card.card_type}"
            )

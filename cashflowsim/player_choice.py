"""Module for making player choices for game simulations."""
from __future__ import annotations
import logging

import cashflowsim.player as cfs_player
import cashflowsim.strategy as cfs_strategy
import cashflowsim.assets as cfs_assets
import cashflowsim.loans as cfs_loans

log: logging.Logger = logging.getLogger(__name__)


def choose_small_or_big_deal_card(*, a_player: cfs_player.Player) -> str:
    """Choose between Small or Big Deal Card."""
    if a_player.strategy.manual:
        while True:
            small_or_big_card = input("Pick '(s)mall' or '(b)ig' Deal Card? ")
            if small_or_big_card.lower() in ["small", "s"]:
                log.info(f"Small Deal Card chosen with input: {small_or_big_card}")
                return "small"
            if small_or_big_card.lower() in ["big", "b"]:
                log.info(f"Big Deal Card chosen with input: {small_or_big_card}")
                return "big"
            print(f"Entry not understood, please try again\n")
            log.info(
                f"Entry not understood, please try again with input: {small_or_big_card}"
            )

    else:
        if a_player.savings > a_player.strategy.big_deal_small_deal_threshold:
            return "big"
        return "small"


def choose_to_donate_to_charity(*, a_strategy: cfs_strategy.Strategy) -> bool:
    """Decide whether to donate to charity manually or by strategy."""
    if a_strategy.manual:
        while True:
            charity_choice: str = input(
                f"Do you want to donate 10% of your income"
                f" to have the option of rolling 1 or 2"
                f" dice for the next 3 turns?"
            ).lower()[0]
            log.info(f"charity_choice: {charity_choice}")
            match charity_choice:
                case "n":
                    print(f"OK, no charity chosen")
                    return False
                case "y":
                    return True
                case _:
                    print(f"Entry not understood, please try again\n")
    else:
        if a_strategy.charitable:
            log.info(f"Choosing to be charitible in non-manual mode")
            return True
        log.info(f"Choosing not to be charitible in non-manual mode")
        return False


def choose_no_die(
    *,
    no_die_choice_list: list[int],
    a_strategy: cfs_strategy.Strategy,
) -> int:
    """Choose number of dice to roll."""
    if a_strategy.manual:
        while True:
            print(f"Please choose number of die to use.")
            try:
                no_die_choice: int = int(input(f"Choices: {str(no_die_choice_list)}"))
            except ValueError:
                err_msg = f"No numeric input. please choose number of die"
                log.info(err_msg)
                print(err_msg)
                continue
            if no_die_choice in no_die_choice_list:
                if no_die_choice == 1:
                    print(f"1 die chosen")
                else:
                    print(f"{no_die_choice} dice chosen")
                break
            print(f"Entry not in list, please try again\n")
            log.info(f"Entry not in list, please try again\n")
    else:
        no_die_choice = max(no_die_choice_list)
        log.info(f"Choosing {no_die_choice} as max in options in non-manual mode")
    return no_die_choice


def choose_to_buy_stock_asset(
    *, a_player: cfs_player.Player, new_stock: cfs_assets.Stock
) -> bool:
    """Choose whether and how much stock to buy."""
    if a_player.strategy.manual:
        while True:
            try:
                print(f"Stock for sale: {new_stock}")
                number_of_shares = int(
                    input(f"How many shares would you like to buy (or 0 to decline)?")
                )
                if number_of_shares >= 0:
                    break
            except ValueError:
                pass
            print(f"Valid number not entered, please try again")
        if number_of_shares >= 1:
            log.info(f"Buying {number_of_shares} shares")
            new_stock.shares = number_of_shares
            return True
        log.info(f"Small Deal Action to buy Stock declined")
        return False

    # Non Manual
    log.info(
        f"new_stock.roi: {new_stock.roi}, player roi_threshold: {a_player.strategy.roi_threshold}"
    )
    if new_stock.roi > a_player.strategy.roi_threshold or (
        (
            new_stock.cost_per_share
            < (
                (new_stock.price_range_high - new_stock.price_range_low)
                * a_player.strategy.price_ratio_threshold
                + new_stock.price_range_low
            )
        )
        and new_stock.name not in ["CD"]
    ):
        log.info(f"Meets ROI (income) or Cost Ratio (Value) criteria")
        if new_stock.cost_per_share < a_player.savings:
            # Buy maximum your can with cash
            # print(f"new_stock: {new_stock}")
            number_of_shares = int(
                float(a_player.savings) / float(new_stock.cost_per_share)
            )
            new_stock.shares = number_of_shares
        else:
            log.info(f"Not enough savings to buy even one share, please drive through")
            return False
        log.info(f"Choosing to buy {new_stock.shares} shares of {new_stock.name}")
        return True
    log.info(f"Choosing not to buy asset due to low roi: {new_stock.name}")
    return False


def choose_to_buy_asset(
    *,
    a_player: cfs_player.Player,
    asset: cfs_assets.Asset,
    price: int = 0,
) -> bool:
    """Decide whether to buy an asset."""
    if price == 0:
        price = asset.cost
    if a_player.strategy.manual:
        while True:
            print(f"Asset for sale: {asset}")
            to_buy = input(f"Do you want to buy for {asset.cost}?").lower()[0]
            if to_buy == "n":
                print("OK, no sale")
                return False
            if to_buy == "y":
                return True
            print(f"Entry not understood, please try again\n")
    else:
        log.info(
            f"In choosing to buy asset not-manual: {asset.name}.\nasset.roi: {asset.roi}. "
            f"a_player.strategy.roi_threshold: {a_player.strategy.roi_threshold}, "
            f"asset.cost: {asset.cost}, asset.price_range_low: "
            f"{asset.price_range_low}, asset.price_range_high: {asset.price_range_high}"
        )
        if asset.roi >= a_player.strategy.roi_threshold or (
            asset.cost
            <= (
                asset.price_range_low
                + (asset.price_range_high - asset.price_range_low)
                * a_player.strategy.price_ratio_threshold
            )
        ):
            log.info(f"Choosing to buy asset: {asset.name}")
            # Buy if high ROI or price below midpoint of range if not gold
            return True
        log.info(f"Choosing not to buy asset: {asset.name}")
        return False


def choose_to_sell_asset(
    *,
    a_player: cfs_player.Player,
    asset: cfs_assets.Asset,
    price: int = 0,
    delta_price: int = 0,
) -> bool:
    """Decide whether to sell assets."""
    log.info(f"In choose_to_sell_asset: {asset.name}")
    if asset.asset_type == "Stock":
        orig_price: int = asset.total_cost  # type: ignore
    else:
        orig_price = asset.cost
    if delta_price > 0:
        price = orig_price + delta_price
    if a_player.strategy.manual:
        while True:
            print(f"Asset: {asset} has an offer of {price}")
            to_sell = input("Do you want to sell?").lower()[0]
            if to_sell == "n":
                print("OK, no sale")
                return False
            if to_sell == "y":
                return True
            print(f"Entry not understood, please try again\n")
    else:
        log.info(f"price: {price}")
        log.info(f"orig_price: {orig_price}")
        if price > asset.loan_amount:
            roi_of_sale = (
                float(asset.cash_flow) * 12 / (float(price) - asset.loan_amount)
            )
        else:
            roi_of_sale = 0
        log.info(f"roi_of_sale: {roi_of_sale}")
        log.info(f"a_player.strategy.roi_threshold: {a_player.strategy.roi_threshold}")
        # Default is to Sell if price is higher than basis & less than ROI
        # threshold on sale price
        if price > orig_price and roi_of_sale < a_player.strategy.roi_threshold:
            log.info(f"Choosing to sell asset: {asset.name}")
            return True
        log.info(f"Choosing not to sell asset: {asset.name}")
        return False


def choose_to_get_loan_to_buy_asset(
    *,
    a_player: cfs_player.Player,
    asset: cfs_assets.Asset,
    loan_amount: int,
) -> bool:
    """Decice whether to take loan to buy asset."""
    expected_loan_payment = int(loan_amount / 10)
    log.info(
        f"Loan to buy asset attempt amount: {loan_amount}"
        f" with payment of {expected_loan_payment}."
    )
    if a_player.strategy.manual:
        while True:
            print(
                f"Asset for sale: {asset} for {asset.cost}"
                f"\nYou only have {a_player.savings}"
            )
            to_buy_entry: str = input(
                f"Do you want to take a loan for {loan_amount} ?"
            ).lower()[0]
            if to_buy_entry == "n":
                print("OK, no sale")
                return False
            if to_buy_entry == "y":
                print("OK, let's get it")
                return True
            print("Entry not understood, please try again\n")
    else:
        log.info(f"Player Strategy:\n{a_player.strategy}")
        if a_player.strategy.take_downpayment_loans:
            if expected_loan_payment <= a_player.monthly_cash_flow:
                log.info("Still enough cash flow for loan, let's buy!")
                return True
            log.info("Can't buy, not enough cash flow to get loan")
            return False
        log.info("Not taking downpayment loan due to strategy")
        return False


def choose_to_pay_off_loan(*, a_player: cfs_player.Player) -> bool:
    """Decide wheter to payoff loan and make payment or pay it off"""
    if len(a_player.loan_list) == 0 or a_player.strategy.loan_payback == "Never":
        return False
    loan_payoff_strategy_to_use = a_player.strategy.loan_payback
    log.info(f"loan_payoff_strategy_to_use: {loan_payoff_strategy_to_use}")
    loan_to_payoff: cfs_loans.Loan = cfs_loans.Loan(
        name="Dummy Loan",
        balance=1000,
        monthly_payment=100,
        partial_payment_allowed=True,
    )
    match loan_payoff_strategy_to_use:
        case "Manual":
            while True:
                for loan_no, loan in enumerate(a_player.loan_list):
                    print(f"{loan_no + 1}: {loan}")
                    log.info(f"{loan_no + 1}: {loan}")
                try:
                    loan_no_to_payoff: int = int(
                        input(
                            f"Which Loan Do you want to payoff (enter number or 0 for none):"
                        )
                    )
                except ValueError:
                    print(f"Invalid loan number (non number). Please try again")
                    log.info(f"Invalid loan number (non number). Please try again")
                    continue
                if loan_no_to_payoff == 0:
                    print(f"OK, not paying off any loans")
                    log.info(f"OK, not paying off any loans")
                    return False
                loan_no_to_payoff -= 1  # Change to 0 based
                if loan_no_to_payoff not in range(len(a_player.loan_list)):
                    print(f"Invalid loan number (bad number). Please try again")
                    log.info(f"Invalid loan number (bad number). Please try again")
                    continue
                log.info(f"Chose to payoff loan number {loan_no_to_payoff+1}")
                break
            while True:
                try:
                    payment = int(input("How Much to payoff? (increments of 1,000):"))
                except ValueError:
                    err_msg = "Invalid payoff amount (non number). Please try again"
                    log.info(err_msg)
                    print(err_msg)
                    continue
                if (
                    payment < 1000
                    or payment > a_player.loan_list[loan_no_to_payoff].balance
                    or payment % 1_000 != 0
                ):
                    err_msg = "Invalid payoff amount (bad number). Please try again"
                    log.info(err_msg)
                    print(err_msg)
                    continue
                break
            if (
                a_player.loan_list[loan_no_to_payoff].partial_payment_allowed
                and payment < a_player.loan_list[loan_no_to_payoff].balance
            ):
                log.info(f"Evaluating partial payment")
                log.info(f"Choose to make partial payment of {payment}")
                a_player.loan_list[loan_no_to_payoff].make_payment(payment=payment)
                a_player.make_payment(payment=payment)
                info_msg = f"Loan paydown made"
                log.info(info_msg)
                print(info_msg)
                return True
            else:
                log.info(f"Evaluating full payoff")
                if payment != a_player.loan_list[loan_no_to_payoff].balance:
                    info_msg = f"Partial payment not allowed and payment chosen was not for full loan amount. Loan paydown not made"
                    log.info(info_msg)
                    print(info_msg)
                    return False
                if payment > a_player.savings:
                    info_msg = (
                        f"Not enough savings to make requested payment to pay-off loan."
                    )
                    log.info(info_msg)
                    print(info_msg)
                    return False
                log.info(f"Player has enough savings to pay-off loan")
                a_player.payoff_loan(loan_number=loan_no_to_payoff)
                info_msg = f"Loan paid-off"
                log.info(info_msg)
                print(info_msg)
                return True
        case "Smallest":
            log.info("Evaluating whether to pay-off loan using 'Smallest' method")
            # loan_paid = False
            while True:
                loan_to_payoff_value: int = 1000000
                loan_to_payoff_no: int = 1
                loan_to_pay: bool = False
                for loan_no, a_loan in enumerate(a_player.loan_list):
                    if (
                        a_loan.partial_payment_allowed
                        and a_player.savings >= 1000
                        and loan_to_payoff_value > 1000
                    ):  # Is it the first loan found that a payment can be made against?
                        loan_to_payoff_value: int = 1000
                        loan_to_payoff: cfs_loans.Loan = a_loan
                        loan_to_payoff_no: int = loan_no
                        loan_to_pay: bool = True
                    if (
                        a_player.savings >= a_loan.balance
                        and a_loan.balance < loan_to_payoff_value
                    ):  # Is it the smallest loan that a payment can be made against?
                        loan_to_payoff_value: int = a_loan.balance
                        loan_to_payoff: cfs_loans.Loan = a_loan
                        loan_to_payoff_no: int = loan_no
                        loan_to_pay: bool = True
                if loan_to_pay:
                    if loan_to_payoff_value == loan_to_payoff.balance:
                        a_player.payoff_loan(loan_number=loan_to_payoff_no)
                        log.info(f"Loan {loan_to_payoff_no} has been paid-off")
                    else:
                        loan_to_payoff.make_payment(payment=1000)
                        log.info(f"Loan {loan_to_payoff_no} has been paid down")
                    return True  # loan_paid = True
                log.info(f"No loans have been paid-off")
                return False
        case "Largest":
            log.info(f"Evaluating whether to pay-off loan using 'Largest' method")
            # loan_paid = False
            while True:
                loan_to_payoff_value = 1
                loan_to_payoff_no = 1
                loan_to_pay = False
                for loan_no, a_loan in enumerate(a_player.loan_list):
                    log.info(
                        f"Partial Payment allowed: {a_loan.partial_payment_allowed}"
                    )
                    log.info(
                        f"a_player.savings: {a_player.savings}, loan_to_payoff_value: {loan_to_payoff_value}"
                    )
                    if (
                        a_loan.partial_payment_allowed
                        and a_player.savings >= 1_000
                        and loan_to_payoff_value < 1_000
                        # should only be true for fist loan if partial_payments_allowed
                    ):
                        log.info(f"Patial payment allowed and first loan")
                        loan_to_payoff_value = 1000
                        # largestLoan = aLoan
                        loan_to_payoff_no = loan_no
                        loan_to_payoff = a_loan
                        loan_to_pay = True
                    else:
                        log.info(f"No partial payment allowed or not first loan?")
                    if (
                        a_loan.balance > loan_to_payoff_value
                        and a_player.savings >= a_loan.balance
                    ):
                        loan_to_payoff_value = a_loan.balance
                        # largestLoan = aLoan
                        loan_to_payoff_no = loan_no
                        loan_to_payoff = a_loan
                        loan_to_pay = True
                if loan_to_pay:
                    if loan_to_payoff_value == loan_to_payoff.balance:
                        a_player.payoff_loan(loan_number=loan_to_payoff_no)
                        log.info(f"Loan {loan_to_payoff_no} has been paid-off")
                    else:
                        loan_to_payoff.make_payment(payment=1000)
                        log.info(f"Loan {loan_to_payoff_no} has been paid down")
                    return True  # Loan Paid
                log.info(f"No loans have been paid-off")
                return False
        case "Highest Interest":
            log.info(
                f"Evaluating whether to pay-off loan using 'Highest Interest' method"
            )
            # loan_paid = False
            while True:
                log.info("Searching through the list of loans")
                largest_interest_rate: float = 0.0
                loan_to_payoff_value: int = 1
                loan_to_payoff_no: int = 1
                loan_to_pay: bool = False
                for loan_no, a_loan in enumerate(a_player.loan_list):
                    this_loan_interest_rate = float(a_loan.monthly_payment) / float(
                        a_loan.balance
                    )
                    if (
                        a_loan.partial_payment_allowed
                        and a_player.savings >= 1000
                        and this_loan_interest_rate > largest_interest_rate
                    ):
                        loan_to_payoff_value = 1000
                        loan_to_payoff_no = loan_no
                        loan_to_payoff = a_loan
                        loan_to_pay = True
                        log.info(
                            f"Found a loan to be paritally repaid {loan_to_payoff_no}\n{a_loan}"
                        )
                    if (
                        a_player.savings >= a_loan.balance
                        and this_loan_interest_rate > largest_interest_rate
                    ):
                        log.info("Found a loan to be fully repaid")
                        loan_to_payoff_value = a_loan.balance
                        loan_to_payoff_no = loan_no
                        loan_to_payoff = a_loan
                        loan_to_pay = True
                if loan_to_pay:
                    if loan_to_payoff_value == loan_to_payoff.balance:
                        a_player.payoff_loan(loan_number=loan_to_payoff_no)
                        log.info(f"Loan {loan_to_payoff_no} has been paid-off")
                    else:
                        log.info(
                            f"Partially paying loan. Balance before: "
                            f"{a_player.loan_list[loan_to_payoff_no].balance}"
                        )
                        # new_balance, new_payment = (
                        loan_payment_result = loan_to_payoff.make_payment(payment=1000)
                        log.info(
                            f"Balance after: {loan_to_payoff.balance}"
                            # new_balance, new_payment)
                            f"\n{loan_payment_result}"
                        )
                    return True  # loan paid
                log.info(f"No loans have been paid-off")
                return False
        case _:
            err_msg = (
                f"Incorrect loan_payoff_strategy_to_use: {loan_payoff_strategy_to_use}"
            )
            log.error(err_msg)
            raise ValueError(err_msg)

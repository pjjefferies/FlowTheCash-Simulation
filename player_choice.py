"""Module for making player choices for game simulations."""

# from importlib import reload
import player
# reload(player)


def choose_small_or_big_deal_card(a_player, verbose=False):
    """Choose between Small or Big Deal Card."""
    if a_player.strategy.manual:
        while True:
            small_or_big_card = input("Pick '(s)mall' or '(b)ig' Deal Card? ")
            if small_or_big_card.lower() in ["small", "s"]:
                return "small"
            elif small_or_big_card.lower() in ["big", "b"]:
                return "big"
            print("Entry not understood, please try again\n")
    else:
        if (a_player.savings >
                a_player.strategy.big_deal_small_deal_threshold):
            return "big"
        else:
            return "small"


def choose_to_donate_to_charity(strategy, verbose=False):
    """Decide whether to donate to charity manually or by strategy."""
    if strategy.manual:
        while True:
            charity_choice = input("Do you want to donate 10% of your income" +
                                   " to have the option of rolling 1 or 2" +
                                   " dice for the next 3 turns? ")
            if charity_choice.lower()[0] == "n":
                print("OK, no charity chosen")
                return "no"
            elif charity_choice.lower()[0] == "y":
                return True
            print("Entry not understood, please try again\n")
    else:
        if strategy.charitable:
            if verbose:
                print("Choosing to be charitible in non-manual mode")
            return True
        else:
            if verbose:
                print("Choosing not to be charitible in non-manual mode")
            return False


def choose_no_die(no_die_choice_list, strategy, verbose):
    """Choose number of dice to roll."""
    if strategy.manual:
        while True:
            print("Please choose number of die to use.")
            no_die_choice = int(input("Choices: " + str(no_die_choice_list)))
            if no_die_choice in no_die_choice_list:
                if no_die_choice == 1:
                    print("1 die chosen")
                else:
                    print(str(no_die_choice) + " dice chosen")
                break
            print("Entry not in list, please try again\n")
    else:
        no_die_choice = max(no_die_choice_list)
        if verbose:
            print("Choosing " + str(no_die_choice)
                  + " as max in options in non-manual mode")
    return no_die_choice


def choose_to_buy_stock_asset(player, new_stock, verbose):
    """Choose whether and how much stock to buy."""
    if player.strategy.manual:
        while True:
            try:
                print("Stock for sale:", new_stock)
                number_of_shares = int(input("How many shares would you like" +
                                             " to buy (or 0 to decline)?"))
                if number_of_shares >= 0:
                    new_stock.set_no_shares(number_of_shares)
                    return True
            except ValueError:
                print("Number not entered, please try again")
        if number_of_shares < 1:
            if verbose:
                print("Small Deal Action to buy Stock declined")
            return False
    else:
        if verbose:
            print("In player choice to buy stock:", new_stock)
        if (new_stock.roi > player.strategy.roi_threshold or
            ((new_stock.cost_per_share <
              ((new_stock.price_range_high + new_stock.price_range_low) *
               player.strategy.price_ratio_threshold))
             and not new_stock.name in ("CD"))):
            if new_stock.cost_per_share < player.savings:
                # Buy maximum your can with cash
                number_of_shares = int(float(player.savings) /
                                       float(new_stock.cost_per_share))
                new_stock.no_shares = number_of_shares
            else:
                if verbose:
                    print("Not enough savings to buy even one share, " +
                          "please drive through")
                return False
            if verbose:
                print("Choosing to buy " + str(new_stock.no_shares) +
                      " shares of " + new_stock.name)
            return True
        else:
            if verbose:
                print("Choosing not to buy asset:", new_stock.name)
            return False


def choose_to_buy_asset(player, asset, verbose, price=0):
    """Decide whether to buy an asset."""
    if price == 0:
        price = asset.cost
    if player.strategy.manual:
        while True:
            print("Asset for sale:", asset)
            to_buy = input("Do you want to buy for " + str(asset.cost) +
                           "?").lower()[0]
            if to_buy == "n":
                print("OK, no sale")
                return False
            elif to_buy == "y":
                return True
            print("Entry not understood, please try again\n")
    else:
        if verbose:
            print("In choosing to buy asset:", asset)
        if ((asset.roi >= player.strategy.roi_threshold or
            (asset.cost <= (
                asset.price_range_low
                + (asset.price_range_high -
                   asset.price_range_low) *
                player.strategy.price_ratio_threshold)))
                and not (asset.name in ("Rare Gold Coin"))):
            if verbose:
                print("Choosing to buy asset:", asset.name)
            # Buy if high ROI or price below midpoint of range if not gold
            return True
        else:
            if verbose:
                print("Choosing not to buy asset:", asset.name)
            return False


def choose_to_sell_asset(player, asset, price, delta_price, verbose):
    """Decide whether to sell assets."""
    if asset.asset_type == "Stock":
        orig_price = asset.total_cost
    else:
        orig_price = asset.cost
    if delta_price > 0:
        price = orig_price + delta_price
    if player.strategy.manual:
        while True:
            print("Asset:", asset, "has an offer of", price)
            to_sell = input("Do you want to sell?").lower()[0]
            if to_sell == "n":
                print("OK, no sale")
                return False
            elif to_sell == "y":
                return True
            print("Entry not understood, please try again\n")
    else:
        roi_of_sale = float(asset.cash_flow) / float(price)
        # Default is to Sell if price is higher than basis & less than ROI
        # threshold on sale price
        if (price > orig_price and
                roi_of_sale < player.strategy.roi_threshold):
            if verbose:
                print("Choosing to sell asset:", asset)
            return True
        else:
            if verbose:
                print("Choosing not to sell asset:", asset)
            return False


def choose_to_get_loan_to_buy_asset(player, asset, loan_amount, verbose):
    """Decice whether to take loan to buy asset."""
    expected_loan_payment = int(loan_amount / 10)
    if verbose:
        print("Loan to buy asset attempt amount: " + str(loan_amount) +
              " with payment of " + str(expected_loan_payment))
    if player.strategy.manual:
        while True:
            print("Asset for sale:", asset, " for " + asset.cost +
                  "\nYou only have " + player.savings)
            to_buy_entry = (input("Do you want to take a loan for " +
                                  loan_amount + "?").lower()[0])
            if to_buy_entry == "n":
                print("OK, no sale")
                return False
            elif to_buy_entry == "y":
                print("OK, let's get it")
                return True
            print("Entry not understood, please try again\n")
    else:
        if player.strategy.take_downpayment_loans:
            if expected_loan_payment <= player.monthly_cash_flow:
                if verbose:
                    print("Still enough cash flow for loan, let's buy!")
                return True
            else:
                if verbose:
                    print("Can't buy, not enough cash flow to get loan")
                return False
        else:
            if verbose:
                print("Not taking downpayment loan due to strategy")
            return False


def choose_to_pay_off_loan(a_player, verbose=False):
    """Decide wheter to payoff loan."""
    if (len(a_player.loan_list) == 0 or
            a_player.strategy.loan_payback == "Never"):
        return False
    loan_payoff_strategy_to_use = a_player.strategy.loan_payback
    if verbose:
        print("loan_payoff_strategy_to_use:", loan_payoff_strategy_to_use)
    if loan_payoff_strategy_to_use == "Manual":
        if len(a_player.loan_list) == 0:
            return False
        loan_no = 0
        for loan in a_player.loan_list:
            loan_no += 1
            print(loan_no, ": ", loan)
        loan_to_payoff = int(input("Whick Loan Do you want to payoff (enter" +
                                   " number or 0 for none):"))
        if loan_to_payoff <= 0 or loan_to_payoff > len(a_player.loan_list):
            print("No Loan payment made")
            return False
        if a_player.loan_list[loan_to_payoff - 1].partial_payment_allowed:
            amount_to_partially_pay = int(input("How Much to payoff? (" +
                                                "increments of 1,000):"))
            if (amount_to_partially_pay % 1000 != 0 and
                amount_to_partially_pay <= a_player.savings and
                (amount_to_partially_pay <
                 a_player.loan_list[loan_to_payoff - 1].balance)):
                if (a_player.loan_list[loan_to_payoff - 1].make_payment(
                        amount_to_partially_pay)[0] is not None):
                    a_player.make_payment(amount_to_partially_pay)
                    print("Loan paydown made")
                    return True
                else:
                    print("Load paydown not made")
                    return False
        else:
            amount_to_pay = a_player.loan_list[loan_to_payoff - 1].balance
            if amount_to_pay <= a_player.savings:
                if a_player.payoff_loan(loan_to_payoff - 1):
                    print("Loan paid-off")
                    return True
                else:
                    print("Loan not paid-off")
                    return False
    else:
        if loan_payoff_strategy_to_use == "Smallest":
            if verbose:
                print("Evaluating whether to pay-off loan using 'Smallest'" +
                      " method")
            loan_paid = False
            while True:
                smallest_loan_value = 1e6
                loan_no = 0
                loan_to_pay = False
                for a_loan in a_player.loan_list:
                    if (a_loan.partial_payment_allowed and
                        a_player.savings >= 1000 and
                            1000 < smallest_loan_value):
                        smallest_loan_value = 1000
                        smallest_loan = a_loan
                        smallest_loan_no = loan_no
                        loan_to_pay = True
                    if (a_player.savings >= a_loan.balance and
                            a_loan.balance < smallest_loan_value):
                        smallest_loan_value = a_loan.balance
                        smallest_loan = a_loan
                        smallest_loan_no = loan_no
                        loan_to_pay = True
                    loan_no += 1
                if loan_to_pay:
                    if smallest_loan_value == smallest_loan.balance:
                        a_player.payoff_loan(smallest_loan_no)
                        loan_paid = True
                    else:
                        smallest_loan.make_payment(1000)
                        loan_paid = True
                else:
                    if loan_paid:
                        return True
                    else:
                        return False
        elif loan_payoff_strategy_to_use == "Largest":
            if verbose:
                print("Evaluating whether to pay-off loan using 'Largest'" +
                      " method")
            loan_paid = False
            while True:
                largest_loan_value = 1
                loan_no = 0
                loan_to_pay = False
                for a_loan in a_player.loan_list:
                    if (a_loan.partial_payment_allowed and
                        a_player.savings >= 1000 and
                            1000 > largest_loan_value):
                        largest_loan_value = 1000
                        # largestLoan = aLoan
                        largest_loan_no = loan_no
                        loan_to_pay = True
                    if (a_loan.balance > largest_loan_value and
                            a_player.savings >= a_loan.balance):
                        largest_loan_value = a_loan.balance
                        # largestLoan = aLoan
                        largest_loan_no = loan_no
                        loan_to_pay = True
                    loan_no += 1
                if loan_to_pay:
                    if (largest_loan_value ==
                            a_player.loan_list[largest_loan_no].balance):
                        a_player.payoff_loan(largest_loan_no)
                        loan_paid = True
                    else:
                        a_loan.make_payment(1000)
                        loan_paid = True
                else:
                    if loan_paid:
                        return True
                    else:
                        return False
        elif loan_payoff_strategy_to_use == "Highest Interest":
            if verbose:
                print("Evaluating whether to pay-off loan using 'Highest" +
                      " Interest' method")
            loan_paid = False
            while True:
                if verbose:
                    print("Searching through the list of loans")
                largest_interest_rate = 0.0
                loan_no = 0
                loan_to_pay = False
                for a_loan in a_player.loan_list:
                    this_loan_interest_rate = (
                        float(a_loan.monthly_payment) /
                        float(a_loan.balance))
                    if (a_loan.partial_payment_allowed and
                        a_player.savings >= 1000 and
                            this_loan_interest_rate > largest_interest_rate):
                        largest_loan_value = 1000
                        largest_loan_no = loan_no
                        loan_to_pay = True
                        if verbose:
                            print("Found a loan to be paritally repaid",
                                  largest_loan_no, loan_to_pay, a_loan)
                    if (a_player.savings >= a_loan.balance and
                            this_loan_interest_rate > largest_interest_rate):
                        if verbose:
                            print("Found a loan to be fully repaid")
                        largest_loan_value = a_loan.balance
                        largest_loan_no = loan_no
                        loan_to_pay = True
                    loan_no += 1
                if loan_to_pay:
                    if (largest_loan_value ==
                            a_player.loan_list[largest_loan_no].balance):
                        if verbose:
                            print("Paying loan in full")
                        a_player.payoff_loan(largest_loan_no)
                        loan_paid = True
                    else:
                        if verbose:
                            print(
                                "Partially paying loan. Balance before:",
                                a_player.loan_list[largest_loan_no].balance)
                        # new_balance, new_payment = (
                        loan_payment_result = (
                            a_player.loan_list[largest_loan_no].make_payment(1000))
                        if verbose:
                            print("Balance after:",
                                  a_player.loan_list[largest_loan_no].balance,
                                  # new_balance, new_payment)
                                  loan_payment_result)
                        loan_paid = True
                else:
                    if loan_paid:
                        return True
                    else:
                        return False
        else:
            return False


if __name__ == '__main__':      # test
    import profession
    import strategy

    PROFESSION_DICT = profession.get_profession_defs("ProfessionsList.json")
    # Make Available Strategies to Test

    STRATEGY_DICT = strategy.get_strategy_defs("Strategies.json")

    ME = player.Player("PaulCool", PROFESSION_DICT["Engineer"],
                       STRATEGY_DICT["Standard Auto"])
    SHE = player.Player("LynnHot", PROFESSION_DICT["Doctor"],
                        STRATEGY_DICT["Standard Auto"])
    HER = player.Player("KatieCute", PROFESSION_DICT["Business Manager"],
                        STRATEGY_DICT["Dave Ramsey"])
    print(ME.strategy)
    print(SHE.strategy)
    print(choose_small_or_big_deal_card(SHE, True))
    SHE.earn_salary()
    SHE.earn_salary()
    print(SHE.savings)
    print(choose_small_or_big_deal_card(SHE, True))

    ME.make_payment(-50000)      # add some cash to test paying-off loans
    SHE.make_payment(-100000)
    HER.make_payment(-25000)
    print(ME.savings)
    print(SHE.savings)

    print("me loan payoff result:", choose_to_pay_off_loan(ME, True))
    print("me loans remaining:", ME.loan_list)
    print("she loan payoff result:", choose_to_pay_off_loan(SHE, True))
    print("she loans remaining:", SHE.loan_list)
    print("Kaie loan payoff result:", choose_to_pay_off_loan(HER, True))
    print("Katie loans remaining:", HER.loan_list)

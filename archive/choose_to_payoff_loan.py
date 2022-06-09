"""Contains function to decide whether to pay-off loan."""


def choose_to_pay_off_loan(player):
    """Decide whether to choose to payoff loan."""
    if player[0].stratey == "Manual":
        loan_no = 0
        for loan in player[0].loans:
            loan_no += 1
            print(loan_no, ": ", loan)
        loan_to_payoff = int(input("Whick Loan Do you want to payoff (enter " +
                                   "number or 0 for none:"))
        if loan_to_payoff <= 0 or loan_to_payoff > len(player[0].loans):
            print("No Loan payment made")
            return False
        if player[0].loans[loan_to_payoff-1].partial_payment_allowed:
            amount_to_partially_pay = int(input(
                "How Much to payoff? (increments of 1,000):"))
            if (amount_to_partially_pay % 1000 != 0 and
                amount_to_partially_pay <= player[0].savings and
                amount_to_partially_pay <
                    player[0].loans[loan_to_payoff - 1].balance):
                if player[0].loans[loan_to_payoff - 1].make_payment(
                        amount_to_partially_pay)[0] is not None:
                    player[0].make_payment(amount_to_partially_pay)
                    print("Loan paydown made")
                    return True
                else:
                    print("Load paydown not made")
                    return False
        else:
            amount_to_pay = player[0].loans[loan_to_payoff - 1].balance
            if amount_to_pay <= player.savings:
                if player[0].payoff_loan(loan_to_payoff - 1):
                    print("Loan paid-off")
                    return True
                else:
                    print("Loan not paid-off")
                    return False
    else:
        print("Automatic Strategy for Loan Payoff Choice not implemented " +
              "yet, no loans paid-off")
        return False

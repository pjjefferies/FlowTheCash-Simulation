"""Contains function to decide whether to pay-off loan."""


def chooseToPayOffLoan(player):
    """Decide whether to choose to payoff load."""
    if player[0].getStratey == "Manual":
        loanNo = 0
        for loan in player[0].getLoans:
            loanNo += 1
            print(loanNo, ": ", loan)
        loanToPayoff = int(input("Whick Loan Do you want to payoff (enter " +
                                 "number or 0 for none:"))
        if loanToPayoff <= 0 or loanToPayoff > len(player[0].getLoans()):
            print("No Loan payment made")
            return False
        if player[0].getLoans()[loanToPayoff-1].getPartialPaymentAllowed():
            amountToPartiallyPay = int(input(
                "How Much to payoff? (increments of 1,000):"))
            if (amountToPartiallyPay % 1000 != 0 and
                amountToPartiallyPay <= player[0].getSavings() and
                amountToPartiallyPay <
                    player[0].getLoans()[loanToPayoff - 1].getBalance()):
                if player[0].getLoans()[loanToPayoff - 1].makePayment(
                        amountToPartiallyPay)[0] is not None:
                    player[0].makePayment(amountToPartiallyPay)
                    print("Loan paydown made")
                    return True
                else:
                    print("Load paydown not made")
                    return False
        else:
            amountToPay = player[0].getLoans()[loanToPayoff - 1].getBalance()
            if amountToPay <= player.getSavings():
                if player[0].payoffLoan(loanToPayoff - 1):
                    print("Loan paid-off")
                    return True
                else:
                    print("Loan not paid-off")
                    return False
    else:
        print("Automatic Strategy for Loan Payoff Choice not implemented " +
              "yet, no loans paid-off")
        return False

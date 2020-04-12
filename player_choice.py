"""Module for making player choices for game simulations."""

from importlib import reload
import player
reload(player)


def chooseSmallOrBigDealCard(aPlayer, verbose=False):
    """Choose between Small or Big Deal Card."""
    if aPlayer.getStrategy().getManual():
        while True:
            smallOrBigCard = input("Pick '(s)mall' or '(b)ig' Deal Card? ")
            if smallOrBigCard.lower() in ["small", "s"]:
                return "small"
            elif smallOrBigCard.lower() in ["big", "b"]:
                return "big"
            print("Entry not understood, please try again\n")
    else:
        if (aPlayer.getSavings() >
                aPlayer.getStrategy().getBigDealSmallDealThreshold()):
            return "big"
        else:
            return "small"


def chooseToDonateToCharity(strategy, verbose=False):
    """Decide whether to donate to charity manually or by strategy."""
    if strategy.getManual():
        while True:
            charityChoice = input("Do you want to donate 10% of your income" +
                                  " to have the option of rolling 1 or 2" +
                                  " dice for the next 3 turns? ")
            if charityChoice.lower()[0] == "n":
                print("OK, no charity chosen")
                return "no"
            elif charityChoice.lower()[0] == "y":
                return True
            print("Entry not understood, please try again\n")
    else:
        if strategy.getCharitable():
            if verbose:
                print("Choosing to be charitible in non-manual mode")
            return True
        else:
            if verbose:
                print("Choosing not to be charitible in non-manual mode")
            return False


def chooseNoDie(noDieChoiceList, strategy, verbose):
    """Choose number of dice to roll."""
    if strategy.getManual():
        while True:
            print("Please choose number of die to use.")
            noDieChoice = int(input("Choices: " + str(noDieChoiceList)))
            if noDieChoice in noDieChoiceList:
                if noDieChoice == 1:
                    print("1 die chosen")
                else:
                    print(str(noDieChoice) + " dice chosen")
                break
            print("Entry not in list, please try again\n")
    else:
        noDieChoice = max(noDieChoiceList)
        if verbose:
            print("Choosing " + str(noDieChoice)
                  + " as max in options in non-manual mode")
    return noDieChoice


def chooseToBuyStockAsset(player, newStock, verbose):
    """Choose whether and how much stock to buy."""
    if player.getStrategy().getManual():
        while True:
            try:
                print("Stock for sale:", newStock)
                numberOfShares = int(input("How many shares would you like" +
                                           " to buy (or 0 to decline)?"))
                if numberOfShares >= 0:
                    newStock.setNoShares(numberOfShares)
                    return True
            except ValueError:
                print("Number not entered, please try again")
        if numberOfShares < 1:
            if verbose:
                print("Small Deal Action to buy Stock declined")
            return False
    else:
        if verbose:
            print("In player choice to buy stock:", newStock)
        if (newStock.getROI() > player.getStrategy().getROIThreshold() or
            ((newStock.getCostPerShare() <
              ((newStock.getPriceRangeHigh() + newStock.getPriceRangeLow()) *
               player.getStrategy().getPriceRatioThreshold()))
             and not newStock.getName() in ("CD"))):
            if newStock.getCostPerShare() < player.getSavings():
                # Buy maximum your can with cash
                numberOfShares = int(float(player.getSavings()) /
                                     float(newStock.getCostPerShare()))
                newStock.setNoShares(numberOfShares)
            else:
                if verbose:
                    print("Not enough savings to buy even one share, " +
                          "please drive through")
                return False
            if verbose:
                print("Choosing to buy " + str(newStock.getNoShares()) +
                      " shares of " + newStock.getName())
            return True
        else:
            if verbose:
                print("Choosing not to buy asset:", newStock.getName())
            return False


def chooseToBuyAsset(player, asset, verbose, price=0):
    """Decide whether to buy an asset."""
    if price == 0:
        price = asset.getCost()
    if player.getStrategy().getManual():
        while True:
            print("Asset for sale:", asset)
            toBuy = input("Do you want to buy for " + str(asset.getCost()) +
                          "?")
            if toBuy.lower()[0] == "n":
                print("OK, no sale")
                return False
            elif toBuy.lower()[0] == "y":
                return True
            print("Entry not understood, please try again\n")
    else:
        if verbose:
            print("In choosing to buy asset:", asset)
        if ((asset.getROI() >= player.getStrategy().getROIThreshold() or
            (asset.getCost() <= (
                asset.getPriceRangeLow()
                + (asset.getPriceRangeHigh() -
                   asset.getPriceRangeLow()) *
                player.getStrategy().getPriceRatioThreshold())))
                and not (asset.getName() in ("Rare Gold Coin"))):
            if verbose:
                print("Choosing to buy asset:", asset.getName())
            # Buy if high ROI or price below midpoint of range if not gold
            return True
        else:
            if verbose:
                print("Choosing not to buy asset:", asset.getName())
            return False


def chooseToSellAsset(player, asset, price, deltaPrice, verbose):
    """Decide whether to sell assets."""
    if asset.getType == "Stock":
        origPrice = asset.getTotalCost()
    else:
        origPrice = asset.getCost()
    if deltaPrice > 0:
        price = origPrice + deltaPrice
    if player.getStrategy().getManual():
        while True:
            print("Asset:", asset, "has an offer of", price)
            toSell = input("Do you want to sell?")
            if toSell.lower()[0] == "n":
                print("OK, no sale")
                return False
            elif toSell.lower()[0] == "y":
                return True
            print("Entry not understood, please try again\n")
    else:
        ROIofSale = float(asset.getCashFlow()) / float(price)
        # Default is to Sell if price is higher than basis & less than ROI
        # threshold on sale price
        if (price > origPrice and
                ROIofSale < player.getStrategy().getROIThreshold()):
            if verbose:
                print("Choosing to sell asset:", asset)
            return True
        else:
            if verbose:
                print("Choosing not to sell asset:", asset)
            return False


def chooseToGetLoanToBuyAsset(player, asset, loanAmount, verbose):
    """Decice whether to take loan to buy asset."""
    expectedLoanPayment = int(loanAmount / 10)
    if verbose:
        print("Loan to buy asset attempt amount: " + str(loanAmount) +
              " with payment of " + str(expectedLoanPayment))
    if player.getStrategy().getManual():
        while True:
            print("Asset for sale:", asset, " for " + asset.cost +
                  "\nYou only have " + player.getSavings())
            toBuyEntry = input("Do you want to take a loan for " + loanAmount +
                               "?")
            if toBuyEntry.lower()[0] == "n":
                print("OK, no sale")
                return False
            elif toBuyEntry.lower()[0] == "y":
                print("OK, let's get it")
                return True
            print("Entry not understood, please try again\n")
    else:
        if player.getStrategy().getTakeDownPaymentLoans():
            if expectedLoanPayment <= player.getMonthlyCashFlow():
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


def chooseToPayOffLoan(aPlayer, verbose=False):
    """Decide wheter to payoff loan."""
    if (len(aPlayer.getLoans()) == 0 or
            aPlayer.getStrategy().getLoanPayback() == "Never"):
        return False
    loanPayoffStrategyToUse = aPlayer.getStrategy().getLoanPayback()
    if verbose:
        print("loanPayoffStrategyToUse:", loanPayoffStrategyToUse)
    if loanPayoffStrategyToUse == "Manual":
        if len(aPlayer.getLoans()) == 0:
            return False
        loanNo = 0
        for loan in aPlayer.getLoans():
            loanNo += 1
            print(loanNo, ": ", loan)
        loanToPayoff = int(input("Whick Loan Do you want to payoff (enter" +
                                 " number or 0 for none:"))
        if loanToPayoff <= 0 or loanToPayoff > len(aPlayer.getLoans()):
            print("No Loan payment made")
            return False
        if aPlayer.getLoans()[loanToPayoff-1].getPartialPaymentAllowed():
            amountToPartiallyPay = int(input("How Much to payoff? (" +
                                             "increments of 1,000):"))
            if (amountToPartiallyPay % 1000 != 0 and
                amountToPartiallyPay <= aPlayer.getSavings() and
                (amountToPartiallyPay <
                 aPlayer.getLoans()[loanToPayoff - 1].getBalance())):
                if (aPlayer.getLoans()[loanToPayoff - 1].makePayment(
                        amountToPartiallyPay)[0] is not None):
                    aPlayer.makePayment(amountToPartiallyPay)
                    print("Loan paydown made")
                    return True
                else:
                    print("Load paydown not made")
                    return False
        else:
            amountToPay = aPlayer.getLoans()[loanToPayoff-1].getBalance()
            if amountToPay <= aPlayer.getSavings():
                if aPlayer.payoffLoan(loanToPayoff-1):
                    print("Loan paid-off")
                    return True
                else:
                    print("Loan not paid-off")
                    return False
    else:
        if loanPayoffStrategyToUse == "Smallest":
            if verbose:
                print("Evaluating whether to pay-off loan using 'Smallest'" +
                      " method")
            loanPaid = False
            while True:
                smallestLoanValue = 1e6
                loanNo = 0
                loanToPay = False
                for aLoan in aPlayer.getLoans():
                    if (aLoan.getPartialPaymentAllowed() and
                        aPlayer.getSavings() >= 1000 and
                            1000 < smallestLoanValue):
                        smallestLoanValue = 1000
                        smallestLoan = aLoan
                        smallestLoanNo = loanNo
                        loanToPay = True
                    if (aPlayer.getSavings() >= aLoan.getBalance() and
                            aLoan.getBalance() < smallestLoanValue):
                        smallestLoanValue = aLoan.getBalance()
                        smallestLoan = aLoan
                        smallestLoanNo = loanNo
                        loanToPay = True
                    loanNo += 1
                if loanToPay:
                    if smallestLoanValue == smallestLoan.getBalance():
                        aPlayer.payoffLoan(smallestLoanNo)
                        loanPaid = True
                    else:
                        smallestLoan.makePayment(1000)
                        loanPaid = True
                else:
                    if loanPaid:
                        return True
                    else:
                        return False
        elif loanPayoffStrategyToUse == "Largest":
            if verbose:
                print("Evaluating whether to pay-off loan using 'Largest'" +
                      " method")
            loanPaid = False
            while True:
                largestLoanValue = 1
                loanNo = 0
                loanToPay = False
                for aLoan in aPlayer.getLoans():
                    if (aLoan.getPartialPaymentAllowed() and
                        aPlayer.getSavings() >= 1000 and
                            1000 > largestLoanValue):
                        largestLoanValue = 1000
                        # largestLoan = aLoan
                        largestLoanNo = loanNo
                        loanToPay = True
                    if (aLoan.getBalance() > largestLoanValue and
                            aPlayer.getSavings() >= aLoan.getBalance()):
                        largestLoanValue = aLoan.getBalance()
                        # largestLoan = aLoan
                        largestLoanNo = loanNo
                        loanToPay = True
                    loanNo += 1
                if loanToPay:
                    if (largestLoanValue ==
                            aPlayer.getLoans()[largestLoanNo].getBalance()):
                        aPlayer.payoffLoan(largestLoanNo)
                        loanPaid = True
                    else:
                        aLoan.makePayment(1000)
                        loanPaid = True
                else:
                    if loanPaid:
                        return True
                    else:
                        return False
        elif loanPayoffStrategyToUse == "Highest Interest":
            if verbose:
                print("Evaluating whether to pay-off loan using 'Highest" +
                      " Interest' method")
            loanPaid = False
            while True:
                if verbose:
                    print("Searching through the list of loans")
                largestInterestRate = 0.0
                loanNo = 0
                loanToPay = False
                for aLoan in aPlayer.getLoans():
                    thisLoanInterestRate = (float(aLoan.getMonthlyPayment()) /
                                            float(aLoan.getBalance()))
                    if (aLoan.getPartialPaymentAllowed() and
                        aPlayer.getSavings() >= 1000 and
                            thisLoanInterestRate > largestInterestRate):
                        largestLoanValue = 1000
                        largestLoanNo = loanNo
                        loanToPay = True
                        if verbose:
                            print("Found a loan to be paritally repaid",
                                  largestLoanNo, loanToPay, aLoan)
                    if (aPlayer.getSavings() >= aLoan.getBalance() and
                            thisLoanInterestRate > largestInterestRate):
                        if verbose:
                            print("Found a loan to be fully repaid")
                        largestLoanValue = aLoan.getBalance()
                        largestLoanNo = loanNo
                        loanToPay = True
                    loanNo += 1
                if loanToPay:
                    if (largestLoanValue ==
                            aPlayer.getLoans()[largestLoanNo].getBalance()):
                        if verbose:
                            print("Paying loan in full")
                        aPlayer.payoffLoan(largestLoanNo)
                        loanPaid = True
                    else:
                        if verbose:
                            print(
                                "Partially paying loan. Balance before:",
                                aPlayer.getLoans()[largestLoanNo].getBalance())
                        newBalance, newPayment = (
                            aPlayer.getLoans()[largestLoanNo].makePayment(1000)
                            )
                        if verbose:
                            print("Balance after:",
                                  aPlayer.getLoans()[largestLoanNo].getBalance(
                                      ), newBalance, newPayment)
                        loanPaid = True
                else:
                    if loanPaid:
                        return True
                    else:
                        return False
        else:
            return False


if __name__ == '__main__':      # test
    professionDict = player.getProfessionDict("ProfessionsList.json")
    # Make Available Strategies to Test

    strategyDict = player.getStrategyDict("Strategies.json")

    me = player.Player("PaulCool", professionDict["Engineer"],
                       strategyDict["Standard Auto"])
    she = player.Player("LynnHot", professionDict["Doctor"],
                        strategyDict["Standard Auto"])
    katie = player.Player("KatieCute", professionDict["Business Manager"],
                          strategyDict["Dave Ramsey"])
    print(me.getStrategy())
    print(she.getStrategy())
    print(chooseSmallOrBigDealCard(she, True))
    she.earnSalary()
    she.earnSalary()
    print(she.getSavings())
    print(chooseSmallOrBigDealCard(she, True))

    me.makePayment(-50000)      # add some cash to test paying-off loans
    she.makePayment(-100000)
    katie.makePayment(-25000)
    print(me.getSavings())
    print(she.getSavings())

    print("me loan payoff result:", chooseToPayOffLoan(me, True))
    print("me loans remaining:", me.getLoans())
    print("she loan payoff result:", chooseToPayOffLoan(she, True))
    print("she loans remaining:", she.getLoans())
    print("Kaie loan payoff result:", chooseToPayOffLoan(katie, True))
    print("Katie loans remaining:", katie.getLoans())

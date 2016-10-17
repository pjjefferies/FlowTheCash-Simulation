import board
import player_choice
import loans
import assets

def boardSpaceAction(playerOnBoard, newBoardSpace, verbose,
                     smallDealCardDeck, bigDealCardDeck, doodadCardDeck, marketCardDeck,
                     board):
    aPlayer = playerOnBoard[0]
    if aPlayer.getStrategy().getManual():
        verbose = True
    #
    if verbose:
        print("Board Space:", newBoardSpace)
    spaceType = newBoardSpace.getBoardSpaceType()
    if spaceType == "Opportunity":
        smallOrBigCard = player_choice.chooseSmallOrBigDealCard(aPlayer, verbose)
        if smallOrBigCard == "small":
            pickedCard = smallDealCardDeck.takeTopCard()
            if verbose:
                print("Small Deal Picked Card:", pickedCard, "\nNo. Cards left:", smallDealCardDeck.getNoCards())
            doSmallDealAction(aPlayer, pickedCard, board, verbose)
        elif smallOrBigCard == "big":
            pickedCard = bigDealCardDeck.takeTopCard()
            if verbose:
                print("Big Deal Picked Card:", pickedCard, "\nNo. Cards left:", bigDealCardDeck.getNoCards())
            doBigDealAction(aPlayer, pickedCard, board, verbose)
    elif spaceType == "Doodads":
        pickedCard = doodadCardDeck.takeTopCard()
        if verbose:
            print("Doodad Picked Card:", pickedCard, "\nNo. Cards left:", doodadCardDeck.getNoCards())
        doDoodadAction(aPlayer, pickedCard, verbose)
  ###      print("Out of doDoodadAction function")
    elif spaceType == "Charity":
        donateToCharityChoice = player_choice.chooseToDonateToCharity(aPlayer.getStrategy(), verbose)
        if donateToCharityChoice == True:
            if aPlayer.getSavings() > 0.1 * aPlayer.getSalary():
                aPlayer.makePayment(int(0.1 * aPlayer.getSalary()))
                aPlayer.startCharityTurns()
                if verbose:
                    print("Charity started")
            else:
                if verbose:
                    print("Sorry, you don't have enough money for charity")
    elif spaceType == "Pay Check":
        return  #paycheck handled if passed or landed-on in main routine
    elif spaceType == "The Market":
        pickedCard = marketCardDeck.takeTopCard()
        if verbose:
            print("Market Picked Card:", pickedCard, "\nNo. Cards left:", marketCardDeck.getNoCards())
        doMarketAction(aPlayer, board, pickedCard, verbose)
    elif spaceType == "Baby":
        children = aPlayer.getNoChildren()
        aPlayer.haveChild()
        if verbose:
            print("Children-Before: " + str(children) +
                  "\nChildren-After : " + str(aPlayer.getNoChildren()))
        return
    elif spaceType == "Downsized":
        aPlayer.refresh()
        totalExpenses = aPlayer.getTotalExpenses()
        if totalExpenses > aPlayer.getSavings():
            newLoanAmount = int(((float(totalExpenses) - float(aPlayer.getSavings()))/1000.0)+1.0)*1000
            if verbose:
                print("Not enough money, getting loan for", str(newLoanAmount) + ".")
                newLoan = loans.Loan("Bank Loan", newLoanAmount, int(newLoanAmount/10), True)
                aPlayer.makeLoan(newLoan)
        aPlayer.makePayment(totalExpenses)
        aPlayer.startLayoff()
    else:
        print("Board Space Type unknown: " + spaceType)
        assert ValueError
 ###   print("End of board space action function")

def doMarketAction(thisPlayer, board, pickedCard, verbose):
    pickedCardType = pickedCard.getCardType()
    if verbose:
        print("In doMarketAction: Card:", pickedCard)
    assert pickedCardType in ["Small Business Improves", "Condo Buyer - 2Br/1Ba", "Shopping Mall Wanted",
                             "Buyer for 20 Acres", "Price of Gold Soars", "Car Wash Buyer",
                             "Software Company Buyer", "Apartment House Buyer", "House Buyer - 3Br/2Ba",
                             "Plex Buyer", "Limited Partnership Sold", "Interest Rates Drop!",
                             "Inflation Hits!"]
    if pickedCardType == "Small Business Improves":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getBusinessAssets():
                if asset.getType() == "StartCompany":
                    asset.increaseCashFlow(pickedCard.getIncreasedCashFlow())
                    if verbose:
                        print("\nPlayer " + aPlayer.getName() + " increased cash flow on asset " +
                              asset.getName() + " by " + pickedCard.getIncreasedCashFlow() + " to " +
                              asset.getCashFlow() + ".")
    elif pickedCardType == "Condo Buyer - 2Br/1Ba":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getRealEstateAssets():
                if asset.getHouseOrCondo() == "Condo":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellRealEstate(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Shopping Mall Wanted":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getBusinessAssets():
                if asset.getName() == "Small Shopping Mall for Sale":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellBusiness(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Buyer for 20 Acres":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getRealEstateAssets():
                if asset.getName() == "Land":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellRealEstate(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Price of Gold Soars":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getBusinessAssets():
                if asset.getName() == "Rare Gold Coin":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellBusiness(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Car Wash Buyer":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getBusinessAssets():
                if asset.getName() == "Car Wash for Sale":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellBusiness(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Software Company Buyer":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getBusinessAssets():
                if asset.getName() == "Start a Company Part Time-Software":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellBusiness(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Apartment House Buyer":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getRealEstateAssets():
                if asset.getType() == "ApartmentHouseForSale":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice()*asset.getUnits(), 0, verbose):
                        aPlayer.sellRealEstate(asset, pickedCard.getPrice()*asset.getUnits(), verbose)
    elif pickedCardType == "House Buyer - 3Br/2Ba":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getRealEstateAssets():
                if asset.getName() == "House for Sale - 3Br/2Ba":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellRealEstate(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Plex Buyer":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getRealEstateAssets():
                if asset.getType() == "XPlex":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice()*asset.getUnits(), 0, verbose):
                        aPlayer.sellRealEstate(asset, pickedCard.getPrice()*asset.getUnits(), verbose)
    elif pickedCardType == "Limited Partnership Sold":
        for aPlayer in board.getPlayerList():
            for asset in aPlayer.getBusinessAssets():
                if asset.getName() == "Limited Partner Wanted":
                    if player_choice.chooseToSellAsset(aPlayer, asset, pickedCard.getPrice(), 0, verbose):
                        aPlayer.sellBusiness(asset, pickedCard.getPrice(), verbose)
    elif pickedCardType == "Interest Rates Drop!":
        for realEstateAsset in thisPlayer.getRealEstateAssets():
            if realEstateAsset.getHouseOrCondo() == "House":
                if player_choice.chooseToSellAsset(thisPlayer, realEstateAsset, 0, 50000, verbose):
                   thisPlayer.sellRealEstate(realEstateAsset, realEstateAsset.getCost()+50000, verbose)
    elif pickedCardType == "Inflation Hits!":
        for realEstateAsset in thisPlayer.getRealEstateAssets():
            if realEstateAsset.getHouseOrCondo() == "House":
                thisPlayer.sellRealEstate(realEstateAsset, 0, verbose)
    else:
        assert ValueError


def doBigDealAction(thisPlayer, pickedCard, board, verbose):
    pickedCardType = pickedCard.getCardType()
    if verbose:
        print("In doBigDealAction, Savings:", thisPlayer.getSavings(), "\nCard:", pickedCard)
    assert pickedCardType in ["ApartmentHouseForSale", "XPlex", "Business", "HouseForSale",
                              "Land", "Expense"]
    #
    if pickedCardType in ["ApartmentHouseForSale", "XPlex"]:
        newRealEstateAsset = assets.RealEstate(pickedCard.getTitle(),
                                               pickedCardType,
                                               None,
                                               pickedCard.getPrice(),
                                               pickedCard.getDownPayment(),
                                               pickedCard.getCashFlow(),
                                               pickedCard.getPriceRangeLow(),
                                               pickedCard.getPriceRangeHigh(),
                                               pickedCard.getUnits(),
                                               0)   #no acres
        if player_choice.chooseToBuyAsset(thisPlayer, newRealEstateAsset, verbose):
            thisPlayer.buyRealEstate(newRealEstateAsset, verbose)
        else:
            del newRealEstateAsset
    elif pickedCardType == "Business":
        newBusinessAsset = assets.Business(pickedCard.getTitle(),
                                           pickedCardType,
                                           pickedCard.getPrice(),
                                           pickedCard.getDownPayment(),
                                           pickedCard.getCashFlow(),
                                           pickedCard.getPriceRangeLow(),
                                           pickedCard.getPriceRangeHigh())
        if player_choice.chooseToBuyAsset(thisPlayer, newBusinessAsset, verbose):
            thisPlayer.buyBusiness(newBusinessAsset, verbose)
        else:
            del newBusinessAsset
    elif pickedCardType == "HouseForSale":
        newHouseAsset = assets.RealEstate(pickedCard.getTitle(),
                                          pickedCardType,
                                          "House",
                                          pickedCard.getPrice(),
                                          pickedCard.getDownPayment(),
                                          pickedCard.getCashFlow(),
                                          pickedCard.getPriceRangeLow(),
                                          pickedCard.getPriceRangeHigh(),
                                          0,   #no units
                                          0)   #no acres
        if player_choice.chooseToBuyAsset(thisPlayer, newHouseAsset, verbose):
            thisPlayer.buyRealEstate(newHouseAsset, verbose)
        else:
            del newHouseAsset
    elif pickedCardType == "Land":
        newLandAsset = assets.RealEstate(pickedCard.getTitle(),
                                        pickedCardType,
                                        "None",
                                        pickedCard.getPrice(),
                                        pickedCard.getDownPayment(),
                                        0,    #no Cash Flow :-(
                                        pickedCard.getPriceRangeLow(),
                                        pickedCard.getPriceRangeHigh(),
                                        0,   #no units
                                        pickedCard.getAcres())
        if player_choice.chooseToBuyAsset(thisPlayer, newLandAsset, verbose):
            thisPlayer.buyRealEstate(newLandAsset, verbose)
        else:
            del newLandAsset
    elif pickedCardType == "Expense":
        if pickedCard.getCostIfHaveRealEstate() > 0:
            for realEstateAsset in thisPlayer.getRealEstateAssets():
                if realEstateAsset.getType() in ["HouseForSale", "ApartmentHouseForSale", "XPlex"]:
                    havePropertyCost = pickedCard.getCostIfHaveRealEstate()
                    break
        elif pickedCard.getCostIfHave8Plex() > 0:
            for realEstateAsset in thisPlayer.getRealEstateAssets():
                if realEstateAsset.getType() == "XPlex":
                    if realEstateAsset.getUnits == 8:
                        havePropertyCost = pickedCard.getCostIfHave8Plex()
                        break


def doSmallDealAction(thisPlayer, pickedCard, board, verbose):
    pickedCardType = pickedCard.getCardType()
    if verbose:
        print("In doSmallDealAction, Savings:", thisPlayer.getSavings(), "Card:", pickedCard)
    assert pickedCardType in ["Stock", "StockSplit", "HouseForSale", "StartCompany", "Asset", "Land",
                               "LoanNotToBeRepaid", "CostIfRentalProperty"]
    #
    if pickedCardType == "Stock":
        newStock = assets.Stock(pickedCard.getSymbol(),
                                0,
                                pickedCard.getPrice(),
                                pickedCard.getDividend(),
                                pickedCard.getPriceRangeLow(),
                                pickedCard.getPriceRangeHigh())
        if not player_choice.chooseToBuyStockAsset(thisPlayer, newStock, verbose):
            del newStock
            return
        thisPlayer.buyStock(newStock, pickedCard.getPrice(), verbose)
    #
    elif pickedCardType == "StockSplit":
        stockSymbol = pickedCard.getSymbol()
        stockSplitRatio = pickedCard.getSplitRatio()
        playerList = board.getPlayerList()
        for eachPlayer in playerList:       #check each player
            listOfStocks = eachPlayer.getStockAssets()
            for eachStock in listOfStocks:
                if eachStock.getName() == stockSymbol:
                    eachStock.stockSplit(stockSplitRatio)
    #
    elif pickedCardType == "HouseForSale":
        newHouseAsset = assets.RealEstate(pickedCard.getTitle(),
                                          pickedCardType,
                                          "House",
                                          pickedCard.getPrice(),
                                          pickedCard.getDownPayment(),
                                          pickedCard.getCashFlow(),
                                          pickedCard.getPriceRangeLow(),
                                          pickedCard.getPriceRangeHigh(),
                                          0,   #no units
                                          0)   #no acres
        if player_choice.chooseToBuyAsset(thisPlayer, newHouseAsset, verbose):
            thisPlayer.buyRealEstate(newHouseAsset, verbose)
        else:
            del newHouseAsset
    elif pickedCardType in ["StartCompany", "Asset"]:
        newBusinessAsset = assets.Business(pickedCard.getTitle(),
                                           pickedCardType,
                                           pickedCard.getPrice(),
                                           pickedCard.getDownPayment(),
                                           pickedCard.getCashFlow(),
                                           pickedCard.getPriceRangeLow(),
                                           pickedCard.getPriceRangeHigh())
        if player_choice.chooseToBuyAsset(thisPlayer, newBusinessAsset, verbose):
            thisPlayer.buyBusiness(newBusinessAsset, verbose)
        else:
            del newBusinessAsset
    elif pickedCardType == "Land":
        newLandAsset = assets.RealEstate(pickedCard.getTitle(),
                                         pickedCardType,
                                         "None",
                                         pickedCard.getPrice(),
                                         pickedCard.getDownPayment(),
                                         0,
                                         pickedCard.getPriceRangeLow(),
                                         pickedCard.getPriceRangeHigh(),
                                         0,   #no units
                                         pickedCard.getAcres())
        if player_choice.chooseToBuyAsset(thisPlayer, newLandAsset, verbose):
            thisPlayer.buyRealEstate(newLandAsset, verbose)
        else:
            del newLandAsset
    elif pickedCardType == "LoanNotToBeRepaid":
        loanNotToBeRepaidAmount = pickedCard.getPrice()
        if thisPlayer.getSavings() < loanNotToBeRepaidAmount:
            newLoanAmount = int(((float(loanNotToBeRepaidAmount) - float(thisPlayer.getSavings()))/1000.0)+1.0)*1000
            if verbose:
                print("Not enough money, getting loan for", str(newLoanAmount) + ".")
            newLoan = loans.Loan("Bank Loan", newLoanAmount, int(newLoanAmount/10), True)
            thisPlayer.makeLoan(newLoan)
        thisPlayer.makePayment(loanNotToBeRepaidAmount)
    elif pickedCardType == "CostIfRentalProperty":
        costIfRentalPropertyAmount = pickedCard.getPrice()
        playerList = board.getPlayerList()
        for eachPlayer in playerList:       #check each player
            if len(eachPlayer.getRealEstateAssets()) > 0:
                if eachPlayer.getSavings() < costIfRentalPropertyAmount:
                    newLoanAmount = int(((float(costIfRentalPropertyAmount) - float(eachPlayer.getSavings()))/1000.0)+1.0)*1000
                    if verbose:
                        print("Not enough money, getting loan for", str(newLoanAmount) + ".")
                    newLoan = loans.Loan("Bank Loan", newLoanAmount, int(newLoanAmount/10), True)
                    eachPlayer.makeLoan(newLoan)
                eachPlayer.makePayment(costIfRentalPropertyAmount)
    else:
        assert ValueError


def doDoodadAction(aPlayer, pickedCard, verbose):
    pickedCardType = pickedCard.getCardType()
    if verbose:
        print("In doDoodadAction, Savings:", aPlayer.getSavings(), "Card:", pickedCard)
    assert pickedCardType in ["OneTimeExpense", "ChildCost", "NewLoan"]
    if pickedCardType == "OneTimeExpense":
        payment = pickedCard.getOneTimePayment()
        if aPlayer.getSavings() < payment:
            newLoanAmount = int(((float(payment) - float(aPlayer.getSavings()))/1000.0)+1.0)*1000
            newLoan = loans.Loan("Bank Loan", newLoanAmount, int(newLoanAmount/10), True)
            aPlayer.makeLoan(newLoan)
        if verbose:
            print("Making payment of", payment)
            print("Savings before:", aPlayer.getSavings())
        aPlayer.makePayment(payment)
        if verbose:
            print("Savings  after:", aPlayer.getSavings())
    elif pickedCardType == "ChildCost":
        anyChildCost = pickedCard.getAnyChildPayment()
        perChildCost = pickedCard.getEachChildPayment()
        noChildren = aPlayer.getNoChildren()
        if noChildren > 0:
            if verbose:
                print("You have kids, you must pay")
            payment = anyChildCost + noChildren * perChildCost
            if aPlayer.getSavings() < payment:
                newLoanAmount = int(((float(payment) - float(aPlayer.getSavings()))/1000.0)+1.0)*1000
                newLoan = loans.Loan("Bank Loan", newLoanAmount, int(newLoanAmount/10), True)
                aPlayer.makeLoan(newLoan)
            aPlayer.makePayment(payment)
        else:
            if verbose:
                print("No kids, no payment required")
    elif pickedCardType == "NewLoan":
        newLoanAmount = pickedCard.getLoanAmount()
  ###      print("newLoanAmount:", newLoanAmount)
        newLoan = loans.Loan(pickedCard.getLoanTitle(), newLoanAmount, pickedCard.getLoanPayment(), False)
  ###      print("newLoan:", str(newLoan))
        aPlayer.makeLoan(newLoan)
  ###      print("aPlayer.getLoans()[-1]:", aPlayer.getLoans()[-1])
        aPlayer.makePayment(newLoanAmount + pickedCard.getOneTimePayment())
  ###      print("Done with 'NewLoan'")
    else:
        assert ValueError


if __name__ == '__main__':      #test
    import board
    import cards
    import player
    import dieRoll
    import copy
    import sys
    import random
    random.seed(2)
    ratRaceBoard = board.getBoardSpaces("RatRaceBoardSpaces.json")

    smallDealCardDeckMaster = cards.loadAllSmallDealCards("SmallDealCards.json")
    bigDealCardDeckMaster = cards.loadAllBigDealCards("BigDealCards.json")
    doodadCardDeckMaster = cards.loadAllDoodadCards("DoodadCards.json")
    marketCardDeckMaster = cards.loadAllMarketCards("MarketCards.json")
    smallDealCardDeck = copy.copy(smallDealCardDeckMaster)
    bigDealCardDeck = copy.copy(bigDealCardDeckMaster)
    doodadCardDeck = copy.copy(doodadCardDeckMaster)
    marketCardDeck = copy.copy(marketCardDeckMaster)

    turnHistory = []

    smallDealCardDeck.shuffle()
    bigDealCardDeck.shuffle()
    doodadCardDeck.shuffle()
    marketCardDeck.shuffle()

    #Make Available Strategies to Test
    #manualStrategy = Strategy(strategyName="Manual",
    #                          manual = True)
    manualStrategy = player.Strategy(strategyName="Manual", manual = True)
    standardAutoStrategy = player.Strategy(strategyName="Standard Auto", manual = False)
    daveRamseyAutoStrategy = player.Strategy(strategyName="Dave Ramsey",
                                             manual = True,
                                             roiThreshold = 0.20,
                                             priceRatioThreshold = 0.5,
                                             takeDownpaymentLoans = False,
                                             takeAnyLoans = False)
    noDownPaymentLoanAutoStrategy = player.Strategy(strategyName="No Down Payment Loans",
                                                    manual = True,
                                                    roiThreshold = 0.20,
                                                    priceRatioThreshold = 0.5,
                                                    takeDownpaymentLoans = False,
                                                    takeAnyLoans = True)
    professionDict = player.getProfessionDict("ProfessionsList.json")
    #me = Player("Paulcool", professionDict["Engineer"], manualStrategy)
    me = player.Player("Paulcool", professionDict["Engineer"], standardAutoStrategy)
    #me = Player("Paulcool", professionDict["Engineer"], daveRamseyAutoStrategy)
    #me = Player("Paulcool", professionDict["Engineer"], noDownPaymentLoadAutoStrategy)
    ratRaceBoard.addPlayer(me, 0)
    meOnBoard = ratRaceBoard.getNextPlayer()
    verbose = True
    verboseLoc = ""
    verboseLoc = "test_logfile.txt"
    if verboseLoc != "":
        saveout = sys.stdout
        outputFile = open(verboseLoc, 'w')
        sys.stdout = outputFile    
    turn = 0
    while True:
        turn += 1
        singleTurnDetail = [turn]
        singleTurnDetail.append(meOnBoard[0].getName())
        singleTurnDetail.append(meOnBoard[0].getProfession())
        singleTurnDetail.append(meOnBoard[0].getStrategy().getName())
        singleTurnDetail.append(meOnBoard[0].getSalary())
        singleTurnDetail.append(meOnBoard[0].getPassiveIncome())
        singleTurnDetail.append(meOnBoard[0].getTaxes())
        singleTurnDetail.append(meOnBoard[0].getOtherExpenses())
        singleTurnDetail.append(meOnBoard[0].getTotalExpenses())
        singleTurnDetail.append(meOnBoard[0].getChildCost())
        singleTurnDetail.append(meOnBoard[0].getSavings())
        singleTurnDetail.append(len(meOnBoard[0].getLoans()))
        singleTurnDetail.append(len(meOnBoard[0].getSoldAssets()))
        singleTurnDetail.append(meOnBoard[0].getNoChildren())
        singleTurnDetail.append(meOnBoard[0].getMonthlyCashFlow())
        singleTurnDetail.append(len(meOnBoard[0].getStockAssets()))
        singleTurnDetail.append(len(meOnBoard[0].getRealEstateAssets()))
        singleTurnDetail.append(len(meOnBoard[0].getBusinessAssets()))
        if verbose:
            print("\nSample Turn:", turn, str(meOnBoard[0]))
        if meOnBoard[0].getCharityTurns() > 0:
            meOnBoard[0].useCharityTurn()
            noOfDice = player_choice.chooseNoDie([1, 2], meOnBoard[0].getStrategy(), verbose)
        else:
            noOfDice = 1
        singleTurnDetail.append(noOfDice)
        if meOnBoard[0].getSkippedTurnsRemaining() > 0:
            if verbose:
                print("Using a layoff day, " + str(meOnBoard[0].getSkippedTurnsRemaining()) + " turns remaining")
            meOnBoard[0].useLayoff()
            singleTurnDetail.append("Use Layoff")
            turnHistory.append(singleTurnDetail)
            continue
        aDieRoll = dieRoll.rollDie(meOnBoard[0].getStrategy(), noOfDice, verbose)
        singleTurnDetail.append(aDieRoll)
        singleTurnDetail.append(meOnBoard[1])
        meOnBoard[1], passedPaycheck, newBoardSpace = ratRaceBoard.movePlayerBoardSpaces(meOnBoard, aDieRoll)
        singleTurnDetail.append(meOnBoard[1])
        singleTurnDetail.append(passedPaycheck)
        singleTurnDetail.append(newBoardSpace.getBoardSpaceType())
        if passedPaycheck:
            if verbose:
                print("Passed payday")
            meOnBoard[0].earnSalary()
        boardSpaceAction(meOnBoard, newBoardSpace, verbose,
                         smallDealCardDeck, bigDealCardDeck, doodadCardDeck, marketCardDeck,
                         ratRaceBoard)
        amIRich, amIBroke = me.refresh()
        if amIRich:
            print("After", turn, "turns, Player", me.getName(), "is rich and wins")
            print(me)
            print("Sold Assets\n\n", me.getSoldAssets())
            break
        elif amIBroke:
            print("After", turn, "turns, Player", me.getName(), "is broke and looses")
            print(me)
            print("Sold Assets\n\n", me.getSoldAssets())
            break
        #
        if doodadCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Doodad Deck, shuffling...")
            doodadCardDeck = copy.copy(doodadCardDeckMaster)
            doodadCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Doodad Deck:", doodadCardDeck.getNoCards())
        elif smallDealCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Small Deal Deck, shuffling...")
            smallDealCardDeck = copy.copy(smallDealCardDeckMaster)
            smallDealCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Small Deal Deck:", smallDealCardDeck.getNoCards())
        elif bigDealCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Big Deal Deck, shuffling...")
            bigDealCardDeck = copy.copy(bigDealCardDeckMaster)
            bigDealCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Big Deal Deck:", bigDealCardDeck.getNoCards())
        elif marketCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Market Deck, shuffling...")
            marketCardDeck = copy.copy(marketCardDeckMaster)
            marketCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Market Deck:", marketCardDeck.getNoCards())
        turnHistory.append(singleTurnDetail)
    singleTurnDetail = [turn]
    singleTurnDetail.append(meOnBoard[0].getName())
    singleTurnDetail.append(meOnBoard[0].getProfession())
    singleTurnDetail.append(meOnBoard[0].getStrategy().getName())
    singleTurnDetail.append(meOnBoard[0].getSalary())
    singleTurnDetail.append(meOnBoard[0].getPassiveIncome())
    singleTurnDetail.append(meOnBoard[0].getTaxes())
    singleTurnDetail.append(meOnBoard[0].getOtherExpenses())
    singleTurnDetail.append(meOnBoard[0].getTotalExpenses())
    singleTurnDetail.append(meOnBoard[0].getChildCost())
    singleTurnDetail.append(meOnBoard[0].getSavings())
    singleTurnDetail.append(len(meOnBoard[0].getLoans()))
    singleTurnDetail.append(len(meOnBoard[0].getSoldAssets()))
    singleTurnDetail.append(meOnBoard[0].getNoChildren())
    singleTurnDetail.append(meOnBoard[0].getMonthlyCashFlow())
    singleTurnDetail.append(len(meOnBoard[0].getStockAssets()))
    singleTurnDetail.append(len(meOnBoard[0].getRealEstateAssets()))
    singleTurnDetail.append(len(meOnBoard[0].getBusinessAssets()))
    singleTurnDetail.append(noOfDice)
    singleTurnDetail.append(dieRoll)
    singleTurnDetail.append(meOnBoard[1])
    singleTurnDetail.append(meOnBoard[1])
    singleTurnDetail.append(passedPaycheck)
    singleTurnDetail.append(newBoardSpace.getBoardSpaceType())
    turnHistory.append(singleTurnDetail)
    turnHistory.append("End of simulation")
    #singleTurnDetail.append(singleTurnDetail)
    print("Entries in Turn Detail List", len(turnHistory), "\n", turnHistory[:5], "\n", turnHistory[-5:])
    if verboseLoc != "":
        sys.stdout = saveout
        outputFile.close()

    import csv
    import datetime
    oneGameFileLogFilename = "GameLog-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
    with open(oneGameFileLogFilename, "w") as OutputFile:
        writer = csv.writer(OutputFile, delimiter=",")
        writer.writerow(["Turn", "Player Name", "Profession", "Strategy", "Salary", "Passive Income",
                         "Taxes", "Other Expenses", "Total Expenses",
                         "Child Cost", "Savings", "Loans", "Sold Assets", "No. Children", "Cashflow",
                         "Stock Assets", "Real Estate Assets", "Business Assets", "No. Dice",
                         "Die Roll", "Board Space No. Before", "Board Space No. After",
                         "Passed Paycheck", "Board Space After"])
        for turn in turnHistory:
            writer.writerow(turn)
        OutputFile.close()

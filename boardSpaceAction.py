"""Simulate Game: This is where all the action is for simulating game."""
import board
import player_choice
import loans
import assets


def board_space_action(player_on_board,
                       new_board_space,
                       verbose,
                       small_deal_card_deck,
                       big_deal_card_deck,
                       doodad_card_deck,
                       market_card_deck,
                       board):
    """Determine what action is needed for board space and make it so."""
    a_player = player_on_board[0]
    if a_player.getStrategy().getManual():
        verbose = True
    #
    if verbose:
        print("Board Space:", new_board_space)
    space_type = new_board_space.getBoardSpaceType()
    if space_type == "Opportunity":
        small_or_big_card = player_choice.chooseSmallOrBigDealCard(
            a_player, verbose)
        if small_or_big_card == "small":
            picked_card = small_deal_card_deck.takeTopCard()
            if verbose:
                print("Small Deal Picked Card:", picked_card,
                      "\nNo. Cards left:", small_deal_card_deck.getNoCards())
            do_small_deal_action(a_player, picked_card, board, verbose)
        elif small_or_big_card == "big":
            picked_card = big_deal_card_deck.takeTopCard()
            if verbose:
                print("Big Deal Picked Card:", picked_card,
                      "\nNo. Cards left:", big_deal_card_deck.getNoCards())
            do_big_deal_action(a_player, picked_card, board, verbose)
    elif space_type == "Doodads":
        picked_card = doodadCardDeck.takeTopCard()
        if verbose:
            print("Doodad Picked Card:", picked_card, "\nNo. Cards left:",
                  doodadCardDeck.getNoCards())
        doDoodadAction(a_player, picked_card, verbose)
    elif space_type == "Charity":
        donateToCharityChoice = player_choice.chooseToDonateToCharity(
            a_player.getStrategy(), verbose)
        if donateToCharityChoice:
            if a_player.getSavings() > 0.1 * a_player.getSalary():
                a_player.makePayment(int(0.1 * a_player.getSalary()))
                a_player.startCharityTurns()
                if verbose:
                    print("Charity started")
            else:
                if verbose:
                    print("Sorry, you don't have enough money for charity")
    elif space_type == "Pay Check":
        return  # Paycheck handled if passed or landed-on in main routine
    elif space_type == "The Market":
        picked_card = marketCardDeck.takeTopCard()
        if verbose:
            print("Market Picked Card:", picked_card, "\nNo. Cards left:",
                  marketCardDeck.getNoCards())
        doMarketAction(a_player, board, picked_card, verbose)
    elif space_type == "Baby":
        children = a_player.getNoChildren()
        a_player.haveChild()
        if verbose:
            print("Children-Before: " + str(children) +
                  "\nChildren-After : " + str(a_player.getNoChildren()))
        return
    elif space_type == "Downsized":
        a_player.refresh()
        totalExpenses = a_player.getTotalExpenses()
        if totalExpenses > a_player.getSavings():
            newLoanAmount = int(((float(totalExpenses) -
                                  float(a_player.getSavings()))
                                 / 1000.0) + 1.0) * 1000
            if verbose:
                print("Not enough money, getting loan for",
                      str(newLoanAmount) + ".")
                newLoan = loans.Loan("Bank Loan", newLoanAmount,
                                     int(newLoanAmount/10), True)
                a_player.makeLoan(newLoan)
        a_player.makePayment(totalExpenses)
        a_player.startLayoff()
    else:
        print("Board Space Type unknown: " + space_type)
        assert ValueError


def doMarketAction(this_player, board, picked_card, verbose):
    """Do action indicated on Market Card."""
    picked_card_type = picked_card.getCardType()
    if verbose:
        print("In doMarketAction: Card:", picked_card)
    assert picked_card_type in [
        "Small Business Improves", "Condo Buyer - 2Br/1Ba",
        "Shopping Mall Wanted", "Buyer for 20 Acres", "Price of Gold Soars",
        "Car Wash Buyer", "Software Company Buyer", "Apartment House Buyer",
        "House Buyer - 3Br/2Ba", "Plex Buyer", "Limited Partnership Sold",
        "Interest Rates Drop!", "Inflation Hits!"]
    if picked_card_type == "Small Business Improves":
        for a_player in board.getPlayerList():
            for asset in a_player.getBusinessAssets():
                if asset.getType() == "StartCompany":
                    asset.increaseCashFlow(picked_card.getIncreasedCashFlow())
                    if verbose:
                        print("\nPlayer " + a_player.getName() +
                              " increased cash flow on asset " +
                              asset.getName() + " by " +
                              picked_card.getIncreasedCashFlow() + " to " +
                              asset.getCashFlow() + ".")
    elif picked_card_type == "Condo Buyer - 2Br/1Ba":
        for a_player in board.getPlayerList():
            for asset in a_player.getRealEstateAssets():
                if asset.getHouseOrCondo() == "Condo":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellRealEstate(asset, picked_card.getPrice(),
                                                verbose)
    elif picked_card_type == "Shopping Mall Wanted":
        for a_player in board.getPlayerList():
            for asset in a_player.getBusinessAssets():
                if asset.getName() == "Small Shopping Mall for Sale":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellBusiness(asset, picked_card.getPrice(),
                                              verbose)
    elif picked_card_type == "Buyer for 20 Acres":
        for a_player in board.getPlayerList():
            for asset in a_player.getRealEstateAssets():
                if asset.getName() == "Land":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellRealEstate(asset, picked_card.getPrice(),
                                                verbose)
    elif picked_card_type == "Price of Gold Soars":
        for a_player in board.getPlayerList():
            for asset in a_player.getBusinessAssets():
                if asset.getName() == "Rare Gold Coin":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellBusiness(asset, picked_card.getPrice(),
                                              verbose)
    elif picked_card_type == "Car Wash Buyer":
        for a_player in board.getPlayerList():
            for asset in a_player.getBusinessAssets():
                if asset.getName() == "Car Wash for Sale":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellBusiness(asset, picked_card.getPrice(),
                                              verbose)
    elif picked_card_type == "Software Company Buyer":
        for a_player in board.getPlayerList():
            for asset in a_player.getBusinessAssets():
                if asset.getName() == "Start a Company Part Time-Software":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellBusiness(asset, picked_card.getPrice(),
                                              verbose)
    elif picked_card_type == "Apartment House Buyer":
        for a_player in board.getPlayerList():
            for asset in a_player.getRealEstateAssets():
                if asset.getType() == "ApartmentHouseForSale":
                    if player_choice.chooseToSellAsset(
                            a_player, asset,
                            picked_card.getPrice()*asset.getUnits(), 0,
                            verbose):
                        a_player.sellRealEstate(
                            asset, picked_card.getPrice()*asset.getUnits(),
                            verbose)
    elif picked_card_type == "House Buyer - 3Br/2Ba":
        for a_player in board.getPlayerList():
            for asset in a_player.getRealEstateAssets():
                if asset.getName() == "House for Sale - 3Br/2Ba":
                    if player_choice.chooseToSellAsset(a_player, asset,
                                                       picked_card.getPrice(),
                                                       0, verbose):
                        a_player.sellRealEstate(asset, picked_card.getPrice(),
                                                verbose)
    elif picked_card_type == "Plex Buyer":
        for a_player in board.getPlayerList():
            for asset in a_player.getRealEstateAssets():
                if asset.getType() == "XPlex":
                    if player_choice.chooseToSellAsset(
                            a_player, asset,
                            picked_card.getPrice()*asset.getUnits(), 0,
                            verbose):
                        a_player.sellRealEstate(
                            asset,
                            picked_card.getPrice()*asset.getUnits(), verbose)
    elif picked_card_type == "Limited Partnership Sold":
        for a_player in board.getPlayerList():
            for asset in a_player.getBusinessAssets():
                if asset.getName() == "Limited Partner Wanted":
                    if player_choice.chooseToSellAsset(
                            a_player, asset, picked_card.getPrice(),
                            0, verbose):
                        a_player.sellBusiness(asset, picked_card.getPrice(),
                                              verbose)
    elif picked_card_type == "Interest Rates Drop!":
        for real_estate_asset in this_player.getRealEstateAssets():
            if real_estate_asset.getHouseOrCondo() == "House":
                if player_choice.chooseToSellAsset(
                        this_player, real_estate_asset, 0, 50000, verbose):
                    this_player.sellRealEstate(real_estate_asset,
                                               real_estate_asset.getCost() +
                                               50000,
                                               verbose)
    elif picked_card_type == "Inflation Hits!":
        for real_estate_asset in this_player.getRealEstateAssets():
            if real_estate_asset.getHouseOrCondo() == "House":
                this_player.sellRealEstate(real_estate_asset, 0, verbose)
    else:
        assert ValueError


def do_big_deal_action(this_player, picked_card, board, verbose):
    """Do a Big Deal Action indicated on Big Deal Cards."""
    picked_card_type = picked_card.getCardType()
    if verbose:
        print("In do_big_deal_action, Savings:", this_player.getSavings(),
              "\nCard:", picked_card)
    assert picked_card_type in ["ApartmentHouseForSale", "XPlex", "Business",
                                "HouseForSale", "Land", "Expense"]
    #
    if picked_card_type in ["ApartmentHouseForSale", "XPlex"]:
        new_real_estate_asset = assets.RealEstate(
            picked_card.getTitle(),
            picked_card_type,
            None,
            picked_card.getPrice(),
            picked_card.getDownPayment(),
            picked_card.getCashFlow(),
            picked_card.getPriceRangeLow(),
            picked_card.getPriceRangeHigh(),
            picked_card.getUnits(),
            acres=0)
        if player_choice.chooseToBuyAsset(this_player, new_real_estate_asset,
                                          verbose):
            this_player.buyRealEstate(new_real_estate_asset, verbose)
        else:
            del new_real_estate_asset
    elif picked_card_type == "Business":
        new_business_asset = assets.Business(picked_card.getTitle(),
                                             picked_card_type,
                                             picked_card.getPrice(),
                                             picked_card.getDownPayment(),
                                             picked_card.getCashFlow(),
                                             picked_card.getPriceRangeLow(),
                                             picked_card.getPriceRangeHigh())
        if player_choice.chooseToBuyAsset(this_player, new_business_asset,
                                          verbose):
            this_player.buyBusiness(new_business_asset, verbose)
        else:
            del new_business_asset
    elif picked_card_type == "HouseForSale":
        new_house_asset = assets.RealEstate(picked_card.getTitle(),
                                            picked_card_type,
                                            "House",
                                            picked_card.getPrice(),
                                            picked_card.getDownPayment(),
                                            picked_card.getCashFlow(),
                                            picked_card.getPriceRangeLow(),
                                            picked_card.getPriceRangeHigh(),
                                            units=0,
                                            acres=0)
        if player_choice.chooseToBuyAsset(this_player, new_house_asset,
                                          verbose):
            this_player.buyRealEstate(new_house_asset, verbose)
        else:
            del new_house_asset
    elif picked_card_type == "Land":
        new_land_asset = assets.RealEstate(picked_card.getTitle(),
                                           picked_card_type,
                                           "None",
                                           picked_card.getPrice(),
                                           picked_card.getDownPayment(),
                                           0,  # cashFlow
                                           picked_card.getPriceRangeLow(),
                                           picked_card.getPriceRangeHigh(),
                                           0,  # units
                                           picked_card.getAcres())
        if player_choice.chooseToBuyAsset(this_player,
                                          new_land_asset, verbose):
            this_player.buyRealEstate(new_land_asset, verbose)
        else:
            del new_land_asset
    elif picked_card_type == "Expense":
        if picked_card.getCostIfHaveRealEstate() > 0:
            for real_estate_asset in this_player.getRealEstateAssets():
                if real_estate_asset.getType() in ["HouseForSale",
                                                   "ApartmentHouseForSale",
                                                   "XPlex"]:
                    # havePropertyCost = picked_card.getCostIfHaveRealEstate()
                    break
        elif picked_card.getCostIfHave8Plex() > 0:
            for real_estate_asset in this_player.getRealEstateAssets():
                if real_estate_asset.getType() == "XPlex":
                    if real_estate_asset.getUnits == 8:
                        # havePropertyCost = picked_card.getCostIfHave8Plex()
                        break


def do_small_deal_action(this_player, picked_card, board, verbose):
    """Do action indicated on Small Deal Card."""
    picked_card_type = picked_card.getCardType()
    if verbose:
        print("In do_small_deal_action, Savings:", this_player.getSavings(),
              "Card:", picked_card)
    assert picked_card_type in ["Stock", "StockSplit", "HouseForSale",
                                "StartCompany", "Asset", "Land",
                                "LoanNotToBeRepaid", "CostIfRentalProperty"]

    if picked_card_type == "Stock":
        newStock = assets.Stock(picked_card.getSymbol(),
                                0,
                                picked_card.getPrice(),
                                picked_card.getDividend(),
                                picked_card.getPriceRangeLow(),
                                picked_card.getPriceRangeHigh())
        if not player_choice.chooseToBuyStockAsset(this_player, newStock,
                                                   verbose):
            del newStock
            return
        this_player.buyStock(newStock, picked_card.getPrice(), verbose)
    #
    elif picked_card_type == "StockSplit":
        stock_symbol = picked_card.getSymbol()
        stock_split_ratio = picked_card.getSplitRatio()
        player_list = board.getPlayerList()
        for eachPlayer in player_list:
            listOfStocks = eachPlayer.getStockAssets()
            for eachStock in listOfStocks:
                if eachStock.getName() == stock_symbol:
                    eachStock.stockSplit(stock_split_ratio)
    #
    elif picked_card_type == "HouseForSale":
        new_house_asset = assets.RealEstate(picked_card.getTitle(),
                                            picked_card_type,
                                            "House",
                                            picked_card.getPrice(),
                                            picked_card.getDownPayment(),
                                            picked_card.getCashFlow(),
                                            picked_card.getPriceRangeLow(),
                                            picked_card.getPriceRangeHigh(),
                                            units=0,
                                            acres=0)
        if player_choice.chooseToBuyAsset(this_player, new_house_asset,
                                          verbose):
            this_player.buyRealEstate(new_house_asset, verbose)
        else:
            del new_house_asset
    elif picked_card_type in ["StartCompany", "Asset"]:
        new_business_asset = assets.Business(picked_card.getTitle(),
                                             picked_card_type,
                                             picked_card.getPrice(),
                                             picked_card.getDownPayment(),
                                             picked_card.getCashFlow(),
                                             picked_card.getPriceRangeLow(),
                                             picked_card.getPriceRangeHigh())
        if player_choice.chooseToBuyAsset(this_player, new_business_asset,
                                          verbose):
            this_player.buyBusiness(new_business_asset, verbose)
        else:
            del new_business_asset
    elif picked_card_type == "Land":
        new_land_asset = assets.RealEstate(picked_card.getTitle(),
                                           picked_card_type,
                                           "None",
                                           picked_card.getPrice(),
                                           picked_card.getDownPayment(),
                                           0,  # cashFlow
                                           picked_card.getPriceRangeLow(),
                                           picked_card.getPriceRangeHigh(),
                                           0,  # units
                                           picked_card.getAcres())
        if player_choice.chooseToBuyAsset(this_player, new_land_asset,
                                          verbose):
            this_player.buyRealEstate(new_land_asset, verbose)
        else:
            del new_land_asset
    elif picked_card_type == "LoanNotToBeRepaid":
        loanNotToBeRepaidAmount = picked_card.getPrice()
        if this_player.getSavings() < loanNotToBeRepaidAmount:
            newLoanAmount = (int(((float(loanNotToBeRepaidAmount) -
                                   float(this_player.getSavings())) /
                                  1000) + 1) * 1000)
            if verbose:
                print("Not enough money, getting loan for",
                      str(newLoanAmount) + ".")
            newLoan = loans.Loan("Bank Loan", newLoanAmount,
                                 int(newLoanAmount/10), True)
            this_player.makeLoan(newLoan)
        this_player.makePayment(loanNotToBeRepaidAmount)
    elif picked_card_type == "CostIfRentalProperty":
        costIfRentalPropertyAmount = picked_card.getPrice()
        player_list = board.getPlayerList()
        for eachPlayer in player_list:
            if len(eachPlayer.getRealEstateAssets()) > 0:
                if eachPlayer.getSavings() < costIfRentalPropertyAmount:
                    newLoanAmount = (int(((float(costIfRentalPropertyAmount) -
                                          float(eachPlayer.getSavings())) /
                                          1000) + 1) * 1000)
                    if verbose:
                        print("Not enough money, getting loan for",
                              str(newLoanAmount) + ".")
                    newLoan = loans.Loan("Bank Loan", newLoanAmount,
                                         int(newLoanAmount / 10), True)
                    eachPlayer.makeLoan(newLoan)
                eachPlayer.makePayment(costIfRentalPropertyAmount)
    else:
        assert ValueError


def doDoodadAction(a_player, picked_card, verbose):
    """Do action on Doodad Card."""
    picked_card_type = picked_card.getCardType()
    if verbose:
        print("In doDoodadAction, Savings:", a_player.getSavings(),
              "Card:", picked_card)
    assert picked_card_type in ["OneTimeExpense", "ChildCost", "NewLoan"]
    if picked_card_type == "OneTimeExpense":
        payment = picked_card.getOneTimePayment()
        if a_player.getSavings() < payment:
            newLoanAmount = (int(((float(payment) -
                                   float(a_player.getSavings())) /
                                  1000) + 1) * 1000)
            newLoan = loans.Loan("Bank Loan", newLoanAmount,
                                 int(newLoanAmount/10), True)
            a_player.makeLoan(newLoan)
        if verbose:
            print("Making payment of", payment)
            print("Savings before:", a_player.getSavings())
        a_player.makePayment(payment)
        if verbose:
            print("Savings  after:", a_player.getSavings())
    elif picked_card_type == "ChildCost":
        anyChildCost = picked_card.getAnyChildPayment()
        perChildCost = picked_card.getEachChildPayment()
        noChildren = a_player.getNoChildren()
        if noChildren > 0:
            if verbose:
                print("You have kids, you must pay")
            payment = anyChildCost + noChildren * perChildCost
            if a_player.getSavings() < payment:
                newLoanAmount = (int(((float(payment) -
                                       float(a_player.getSavings())) /
                                      1000) + 1) * 1000)
                newLoan = loans.Loan("Bank Loan", newLoanAmount,
                                     int(newLoanAmount / 10), True)
                a_player.makeLoan(newLoan)
            a_player.makePayment(payment)
        else:
            if verbose:
                print("No kids, no payment required")
    elif picked_card_type == "NewLoan":
        newLoanAmount = picked_card.getLoanAmount()
        newLoan = loans.Loan(picked_card.getLoanTitle(), newLoanAmount,
                             picked_card.getLoanPayment(), False)
        a_player.makeLoan(newLoan)
        a_player.makePayment(newLoanAmount + picked_card.getOneTimePayment())
    else:
        assert ValueError


if __name__ == '__main__':
    import cards
    import player
    import dieRoll
    import copy
    import sys
    import random
    random.seed(2)
    ratRaceBoard = board.getBoardSpaces("RatRaceBoardSpaces.json")

    small_deal_card_deck_master = cards.loadAllSmallDealCards(
        "SmallDealCards.json")
    big_deal_card_deck_master = cards.loadAllBigDealCards("BigDealCards.json")
    doodadCardDeckMaster = cards.loadAllDoodadCards("DoodadCards.json")
    market_card_deck_master = cards.loadAllMarketCards("MarketCards.json")
    small_deal_card_deck = copy.copy(small_deal_card_deck_master)
    big_deal_card_deck = copy.copy(big_deal_card_deck_master)
    doodadCardDeck = copy.copy(doodadCardDeckMaster)
    marketCardDeck = copy.copy(market_card_deck_master)

    turnHistory = []

    small_deal_card_deck.shuffle()
    big_deal_card_deck.shuffle()
    doodadCardDeck.shuffle()
    marketCardDeck.shuffle()

    # Make Available Strategies to Test
    manualStrategy = player.Strategy(strategyName="Manual", manual=True)
    standardAutoStrategy = player.Strategy(strategyName="Standard Auto",
                                           manual=False)
    daveRamseyAutoStrategy = player.Strategy(strategyName="Dave Ramsey",
                                             manual=True,
                                             roiThreshold=0.20,
                                             priceRatioThreshold=0.5,
                                             takeDownpaymentLoans=False,
                                             takeAnyLoans=False)
    noDownPaymentLoanAutoStrategy = player.Strategy(
        strategyName="No Down Payment Loans",
        manual=True,
        roiThreshold=0.20,
        priceRatioThreshold=0.5,
        takeDownpaymentLoans=False,
        takeAnyLoans=True)
    professionDict = player.getProfessionDict("ProfessionsList.json")
    me = player.Player("Paulcool", professionDict["Engineer"],
                       standardAutoStrategy)
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
            noOfDice = player_choice.chooseNoDie([1, 2],
                                                 meOnBoard[0].getStrategy(),
                                                 verbose)
        else:
            noOfDice = 1
        singleTurnDetail.append(noOfDice)
        if meOnBoard[0].getSkippedTurnsRemaining() > 0:
            if verbose:
                print("Using a layoff day, " +
                      str(meOnBoard[0].getSkippedTurnsRemaining()) +
                      " turns remaining")
            meOnBoard[0].useLayoff()
            singleTurnDetail.append("Use Layoff")
            turnHistory.append(singleTurnDetail)
            continue
        aDieRoll = dieRoll.rollDie(meOnBoard[0].getStrategy(), noOfDice,
                                   verbose)
        singleTurnDetail.append(aDieRoll)
        singleTurnDetail.append(meOnBoard[1])
        meOnBoard[1], passedPaycheck, new_board_space = (
            ratRaceBoard.movePlayerBoardSpaces(meOnBoard, aDieRoll))
        singleTurnDetail.append(meOnBoard[1])
        singleTurnDetail.append(passedPaycheck)
        singleTurnDetail.append(new_board_space.getBoardSpaceType())
        if passedPaycheck:
            if verbose:
                print("Passed payday")
            meOnBoard[0].earnSalary()
        board_space_action(meOnBoard,
                           new_board_space,
                           verbose,
                           small_deal_card_deck,
                           big_deal_card_deck,
                           doodadCardDeck,
                           marketCardDeck,
                           ratRaceBoard)
        amIRich, amIBroke = me.refresh()
        if amIRich:
            print("After", turn, "turns, Player", me.getName(),
                  "is rich and wins")
            print(me)
            print("Sold Assets\n\n", me.getSoldAssets())
            break
        elif amIBroke:
            print("After", turn, "turns, Player", me.getName(),
                  "is broke and looses")
            print(me)
            print("Sold Assets\n\n", me.getSoldAssets())
            break

        if doodadCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Doodad Deck, shuffling...")
            doodadCardDeck = copy.copy(doodadCardDeckMaster)
            doodadCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Doodad Deck:",
                      doodadCardDeck.getNoCards())
        elif small_deal_card_deck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Small Deal Deck, shuffling...")
            small_deal_card_deck = copy.copy(small_deal_card_deck_master)
            small_deal_card_deck.shuffle()
            if verbose:
                print("After shuffling, cards now in Small Deal Deck:",
                      small_deal_card_deck.getNoCards())
        elif big_deal_card_deck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Big Deal Deck, shuffling...")
            big_deal_card_deck = copy.copy(big_deal_card_deck_master)
            big_deal_card_deck.shuffle()
            if verbose:
                print("After shuffling, cards now in Big Deal Deck:",
                      big_deal_card_deck.getNoCards())
        elif marketCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Market Deck, shuffling...")
            marketCardDeck = copy.copy(market_card_deck_master)
            marketCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Market Deck:",
                      marketCardDeck.getNoCards())
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
    singleTurnDetail.append(new_board_space.getBoardSpaceType())
    turnHistory.append(singleTurnDetail)
    turnHistory.append("End of simulation")

    print("Entries in Turn Detail List", len(turnHistory), "\n",
          turnHistory[:5], "\n", turnHistory[-5:])
    if verboseLoc != "":
        sys.stdout = saveout
        outputFile.close()

    import csv
    import datetime
    oneGameFileLogFilename = ("GameLog-" +
                              datetime.datetime.now().strftime(
                                  "%Y%m%d-%H%M%S") + ".csv")
    with open(oneGameFileLogFilename, "w") as OutputFile:
        writer = csv.writer(OutputFile, delimiter=",")
        writer.writerow(["Turn", "Player Name", "Profession", "Strategy",
                         "Salary", "Passive Income", "Taxes", "Other Expenses",
                         "Total Expenses", "Child Cost", "Savings", "Loans",
                         "Sold Assets", "No. Children", "Cashflow",
                         "Stock Assets", "Real Estate Assets",
                         "Business Assets", "No. Dice", "Die Roll",
                         "Board Space No. Before", "Board Space No. After",
                         "Passed Paycheck", "Board Space After"])
        for turn in turnHistory:
            writer.writerow(turn)
        OutputFile.close()

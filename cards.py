from jsonReadWriteFile import *

class Card(object):
    def __init__(self, title, cardType):
        self.title = title
        self.cardType = cardType
    def getTitle(self):
        return self.title
    def getCardType(self):
        return self.cardType

class DoodadCard(Card):
    def __init__(self, title, cardType, oneTimePayment=0, anyChildPayment=0, eachChildPayment=0,
                 loanTitle='', loanAmount=0, loanPayment=0):
        assert ((cardType == "OneTimeExpense" and oneTimePayment > 0) or
                (cardType == "ChildCost" and ((anyChildPayment > 0) or (eachChildPayment > 0))) or
                (cardType == "NewLoan" and loanTitle != "" and loanAmount > 0 and loanPayment > 0))
        Card.__init__(self, title, cardType)
        if self.cardType == "OneTimeExpense":
            self.oneTimePayment = oneTimePayment
        elif self.cardType == "ChildCost":
            self.anyChildPayment = anyChildPayment
            self.eachChildPayment = eachChildPayment
        elif self.cardType == "NewLoan":
            self.loanTitle = loanTitle
            self.loanAmount = loanAmount
            self.loanPayment = loanPayment
            self.oneTimePayment = oneTimePayment
        else:
            print("Card Type: ", self.cardType, "no found in Card creation")
    def getOneTimePayment(self):
        return self.oneTimePayment
    def getAnyChildPayment(self):
        return self.anyChildPayment
    def getEachChildPayment(self):
        return self.eachChildPayment
    def getLoanTitle(self):
        return self.loanTitle
    def getLoanAmount(self):
        return self.loanAmount
    def getLoanPayment(self):
        return self.loanPayment
    def __str__(self):
        if self.cardType == "OneTimeExpense":
            return ("\nTitle:           " + self.title +
                    "\nType:            " + self.cardType +
                    "\nOne Time Payment:" + str(self.oneTimePayment))
        elif self.cardType == "ChildCost":
            return ("\nTitle:           " + self.title +
                    "\nType:            " + self.cardType +
                    "\nAny Child Cost:  " + str(self.anyChildPayment) +
                    "\nEach Child Cost: " + str(self.eachChildPayment))
        elif self.cardType == "NewLoan":
            return ("\nTitle:           " + self.title +
                    "\nType:            " + self.cardType +
                    "\nLoan Title  :    " + self.loanTitle +
                    "\nLoan Amount :    " + str(self.loanAmount) +
                    "\nLoan Payment:    " + str(self.loanPayment))
        else:
            print("Card Type: ", self.cardType, " not found in string conversion")

        
class MarketCard(Card):
    def __init__(self, titleCardType, price=0, increasedCashFlow=0,
                 mustSell=False, selfOnly=False):
        assert ((titleCardType == "Small Business Improves" and increasedCashFlow > 0) or
                (titleCardType == "Condo Buyer - 2Br/1Ba" and price > 0) or
                (titleCardType == "Shopping Mall Wanted" and price > 0) or
                (titleCardType == "Buyer for 20 Acres" and price > 0) or
                (titleCardType == "Price of Gold Soars" and price > 0) or
                (titleCardType == "Car Wash Buyer" and price > 0) or
                (titleCardType == "Software Company Buyer" and price > 0) or
                (titleCardType == "Apartment House Buyer" and price > 0) or
                (titleCardType == "House Buyer - 3Br/2Ba" and price > 0) or
                (titleCardType == "Plex Buyer" and price > 0) or
                (titleCardType == "Limited Partnership Sold" and price > 0) or
                (titleCardType == "Interest Rates Drop!" and price > 0) or
                (titleCardType == "Inflation Hits!"))
        Card.__init__(self, titleCardType, titleCardType)
        if mustSell == "True":
            mustSell = True
        elif mustSell == "False":
            mustSell = False
        self.mustSell = mustSell
        self.price = price

        if selfOnly == "True":
            selfOnly = True
        elif selfOnly == "False":
            selfOnly = False
        self.selfOnly = selfOnly

        if self.title == "Small Business Improves":
            self.increasedCashFlow = increasedCashFlow
        elif self.title in ["Condo Buyer - 2Br/1Ba", "Shopping Mall Wanted", "Buyer for 20 Acres",
                            "Price of Gold Soars", "Car Wash Buyer", "Software Company Buyer",
                            "Apartment House Buyer", "House Buyer - 3Br/2Ba", "Plex Buyer"]:
            self.price = price
        elif self.title == "Limited Partnership Sold":
            self.priceMultiple = price
        elif self.title == "Interest Rates Drop!":
            self.addedPrice = price
        elif self.title == "Inflation Hits!":
            pass
        else:
            print("Unknown Market Card Type:", self.title, "in card creation")
    def getPrice(self):
        return self.price
    def getIncreasedCashFlow(self):
        return self.increasedCashFlow
    def getPriceMultiple(self):
        return self.priceMultiple
    def getAddedPrice(self):
        return self.addedPrice
    def getMustSell(self):
        return self.mustSell
    def getSelfOnly(self):
        return self.selfOnly
    def __str__(self):
        if self.cardType == "Small Business Improves":
            return ("\nTitle:                   " + self.title +
                    "\nIncreased Cash Flow:     " + str(self.increasedCashFlow) +
                    "\nMust Sell:               " + str(self.mustSell))
        elif self.cardType in ["Condo Buyer - 2Br/1Ba", "Shopping Mall Wanted", "Buyer for 20 Acres",
                               "Price of Gold Soars", "Car Wash Buyer", "Software Company Buyer",
                               "Apartment House Buyer", "House Buyer - 3Br/2Ba", "Plex Buyer"]:
            return ("\nTitle:     " + self.title +
                    "\nPrice:     " + str(self.price) +
                    "\nMust Sell: " + str(self.mustSell))
        elif self.cardType == "Limited Partnership Sold":
            return ("\nTitle:          " + self.title +
                    "\nPrice Multiple: " + str(self.priceMultiple) +
                    "\nMust Sell:      " + str(self.mustSell))
        elif self.cardType == "Interest Rates Drop!":
            return ("\nTitle:       " + self.title +
                    "\nAdded Price: " + str(self.addedPrice) +
                    "\nMust Sell:   " + str(self.mustSell) +
                    "\nSelf Only:   " + str(self.selfOnly))
        elif self.cardType == "Inflation Hits!":
            return ("\nTitle:          " + self.title +
                    "\nMust Sell:      " + str(self.mustSell))
        else:
            print("Card Type: ", self.cardType, " not found in card string conversion")

        
class DealCard(Card):
    def __init__(self, title, cardType, houseOrCondo, price, downPayment, cashFlow,
                 priceRangeLow, priceRangeHigh,
                 allMayBuy=False):
        assert (cardType != "HouseForSale" or price > 0)
        Card.__init__(self, title, cardType)
        if self.cardType == "HouseForSale":
            self.houseOrCondo = houseOrCondo
            self.price = price
            self.downPayment = downPayment
            self.cashFlow = cashFlow
        self.allMayBuy = allMayBuy
        self.priceRangeLow = priceRangeLow
        self.priceRangeHigh = priceRangeHigh

    def getPrice(self):
        return self.price
    def getDownPayment(self):
        return self.downPayment
    def getCashFlow(self):
        return self.cashFlow
    def getPriceRangeLow(self):
        return self.priceRangeLow
    def getPriceRangeHigh(self):
        return self.priceRangeHigh
    def getHouseOrCondo(self):
        return self.houseOrCondo
    def getAllMayBuy(self):
        return self.allMayBuy

class SmallDealCard(DealCard):
    def __init__(self, title, cardType, houseOrCondo, symbol, price, downPayment, cashFlow,
                 splitRatio, priceRangeLow, priceRangeHigh,
                 allMayBuy=False):
        AvailableStocks = ['OK4U', 'ON2U', 'GRO4US', '2BIG', 'MYT4U', 'CD']
        assert ((cardType == "Stock" and symbol in AvailableStocks and price > 0) or
                (cardType == "StockSplit" and symbol in AvailableStocks and splitRatio > 0) or
                (cardType == "HouseForSale" and price > 0) or
                (cardType == "Asset" and price > 0) or
                (cardType == "Land" and price > 0) or
                (cardType == "LoanNotToBeRepaid" and price > 0) or
                (cardType == "CostIfRentalProperty" and price > 0) or
                (cardType == "StartCompany" and price > 0))
        DealCard.__init__(self, title, cardType, houseOrCondo, price, downPayment, cashFlow,
                          priceRangeLow, priceRangeHigh, 
                          allMayBuy)
        if self.cardType == "Stock":
            self.symbol = symbol
            self.price = price
            self.dividend = cashFlow
        elif self.cardType == "StockSplit":
            self.symbol = symbol
            self.splitRatio = splitRatio
        elif self.cardType == "StockSplit":
            self.symbol = symbol
            self.splitRatio = splitRatio
        elif self.cardType == "Asset":
            self.price = price
            self.downPayment = price
            self.cashFlow = cashFlow
            self.priceRangeLow = priceRangeLow
            self.priceRangeHigh = priceRangeHigh
        elif self.cardType == "Land":
            self.price = price
            self.downPayment = downPayment
            self.acres = cashFlow
            self.houseOrCondo = "None"
        elif self.cardType in ["LoanNotToBeRepaid", "CostIfRentalProperty"]:
            self.price = price
        elif self.cardType == "StartCompany":
            self.price = price
            self.downPayment = downPayment
            self.cashFlow = cashFlow
    def getSymbol(self):
        return self.symbol
    def getDividend(self):
        return self.dividend
    def getSplitRatio(self):
        return self.splitRatio
    def getAcres(self):
        return self.acres
    def __str__(self):
        if self.cardType == "Stock":
            return ("\nSmall Deal Card:" +
                    "\nTitle:       " + self.title +
                    "\nType:        " + self.cardType +
                    "\nSymbol:      " + self.symbol +
                    "\nPrice:       " + str(self.price) +
                    "\nDividends:   " + str(self.dividend) +
                    "\nPrice Range: " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "StockSplit":
            return ("\nSmall Deal Card:" +
                    "\nTitle: " + self.title +
                    "\nType: " + self.cardType +
                    "\nSymbol: " + self.symbol +
                    "\nSplit Ratio: " + str(self.splitRatio))
        elif self.cardType == "HouseForSale":
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.cardType +
                    "\nHouse or Condo: " + self.houseOrCondo +
                    "\nPrice:          " + str(self.price) +
                    "\nDown Payment:   " + str(self.downPayment) +
                    "\nCash Flow:      " + str(self.cashFlow) +
                    "\nPrice Range:    " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "Asset":
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.cardType +
                    "\nPrice:          " + str(self.price) +
                    "\nCash Flow:      " + str(self.cashFlow) +
                    "\nPrice Range:    " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "Land":
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.cardType +
                    "\nAcres:          " + str(self.acres))
        elif self.cardType in ["LoanNotToBeRepaid", "CostIfRentalProperty"]:
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.cardType +
                    "\nCost:           " + str(self.price))
        elif self.cardType == "StartCompany":
            return ("\nSmall Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.cardType +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.downPayment) +
                    "\nCash Flow:    " + str(self.cashFlow))
        else:
            print("Small Deal Card Type: ", self.cardType, " not found")

class BigDealCard(DealCard):
    def __init__(self, title, cardType, price, downPayment, cashFlow,
                 units, acres,
                 priceRangeLow, priceRangeHigh,
                 costIfHaveRealEstate, costIfHave8Plex):
        assert ((cardType in ["ApartmentHouseForSale", "XPlex"] and units > 0 and price > 0) or
                (cardType in ["HouseForSale", "Business"] and price > 0) or
                (cardType == "Land" and acres > 0 and price > 0) or
                (cardType == "Expense" and (costIfHaveRealEstate > 0 or costIfHave8Plex > 0)))
        DealCard.__init__(self, title, cardType, "None", price, downPayment, cashFlow,
                          priceRangeLow, priceRangeHigh, False)
        if self.cardType in ["ApartmentHouseForSale", "XPlex"]:
            self.units = units
            self.price = price
            self.houseOrCondo = "None"
            self.downPayment = downPayment
            self.cashFlow = cashFlow
            self.priceRangeLow = priceRangeLow
            self.priceRangeHigh = priceRangeHigh
        elif self.cardType in ["Partnership", "Business"]:
            self.price = price
            self.downPayment = downPayment
            self.cashFlow = cashFlow
            self.priceRangeLow = priceRangeLow
            self.priceRangeHigh = priceRangeHigh
        elif self.cardType == "Land":
            self.acres = acres
            self.price = price
            self.downPayment = downPayment
            self.cashFlow = cashFlow
            self.priceRangeLow = priceRangeLow
            self.priceRangeHigh = priceRangeHigh
        elif self.cardType == "Expense":
            self.costIfHaveRealEstate = costIfHaveRealEstate
            self.costIfHave8Plex = costIfHave8Plex
    def getUnits(self):
        return self.units
    def getAcres(self):
        return self.acres
    def getCostIfHaveRealEstate(self):
        return self.costIfHaveRealEstate
    def getCostIfHave8Plex(self):
        return self.costIfHave8Plex
    def __str__(self):
        if self.cardType in ["ApartmentHouseForSale", "XPlex"]:
            return ("\nBig Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.cardType +
                    "\nUnits:          " + str(self.units) +
                    "\nPrice:          " + str(self.price) +
                    "\nDown Payment:   " + str(self.downPayment) +
                    "\nCash Flow:      " + str(self.cashFlow) +
                    "\nPrice Range:    " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "HouseForSale":
            return ("\nBig Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.cardType +
                    "\nHouse or Condo: " + self.houseOrCondo +
                    "\nDown Payment:   " + str(self.downPayment) +
                    "\nCash Flow:      " + str(self.cashFlow) +
                    "\nPrice Range:    " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "Partnership":
            return ("\nBig Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.cardType +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.downPayment) +
                    "\nCash Flow:    " + str(self.cashFlow) +
                    "\nPrice Range:    " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "Land":
            return ("\nBig Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.cardType +
                    "\nAcres:        " + str(self.acres) +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.downPayment) +
                    "\nCash Flow:    " + str(self.cashFlow))
        elif self.cardType == "Business":
            return ("\nBig Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.cardType +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.downPayment) +
                    "\nCash Flow:    " + str(self.cashFlow) +
                    "\nPrice Range:    " + str(self.priceRangeLow) + " - " + str(self.priceRangeHigh))
        elif self.cardType == "Expense":
            return ("\nBig Deal Card:" +
                    "\nTitle:                    " + self.title +
                    "\nType:                     " + self.cardType +
                    "\nCost if Have Real Estate: " + str(self.costIfHaveRealEstate) +
                    "\nCost if Have 8-Plex     : " + str(self.costIfHave8Plex))
        else:
            print("big Deal Card Type: ", self.cardType, " not found")


def loadAllDoodadCards(doodadCardsFilename):
    try:
        doodadCardsDict = load_json(doodadCardsFilename)
    except OSError:
        print("No good Doodad Cards json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good Doodad Cards json file found, ValueError, please fix")
        raise ValueError

    doodadCardDeck = Deck("Doodad Cards")
    for card in doodadCardsDict:
        if doodadCardsDict[card]["Type"] == "OneTimeExpense":
            doodadCardDeck.addCard(DoodadCard(doodadCardsDict[card]["Title"],
                                              doodadCardsDict[card]["Type"],
                                              int(doodadCardsDict[card]["Cost"])))
        elif doodadCardsDict[card]["Type"] == "ChildCost":
            doodadCardDeck.addCard(DoodadCard(doodadCardsDict[card]["Title"],
                                              doodadCardsDict[card]["Type"],
                                              0,   #3 - One Time Payment
                                              int(doodadCardsDict[card]["Cost if any Child"]),
                                              int(doodadCardsDict[card]["Cost per Child"])))
        elif doodadCardsDict[card]["Type"] == "NewLoan":
            doodadCardDeck.addCard(DoodadCard(doodadCardsDict[card]["Title"],
                                              doodadCardsDict[card]["Type"],
                                              int(doodadCardsDict[card]["Down Payment"]),
                                              0,    #4 - Any Child Payment
                                              0,    #5 - Each Child Payment
                                              doodadCardsDict[card]["Loan Name"],
                                              int(doodadCardsDict[card]["Loan Amount"]),
                                              int(doodadCardsDict[card]["Payment"])))
        else:
            print("Known Doodad card not found in row: ", doodadCardsDict[card])
    return doodadCardDeck


def loadAllMarketCards(marketCardsFilename):
    try:
        marketCardsDict = load_json(marketCardsFilename)
    except OSError:
        print("No good Market Cards json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good Market Cards json file found, ValueError, please fix")
        raise ValueError

    marketCardDeck = Deck("Market Cards")
    for card in marketCardsDict:
        if marketCardsDict[card]["Title"] == "Small Business Improves":
            marketCardDeck.addCard(MarketCard(marketCardsDict[card]["Title"],
                                              0,    # - 2 - Cost/Price not used
                                              marketCardsDict[card]["Increased Cash Flow"],
                                              False, # - 4 - mustSell not used
                                              False)) # - 5 - selfOnly not used.
        elif marketCardsDict[card]["Title"] in ["Condo Buyer - 2Br/1Ba",
                                                "Shopping Mall Wanted",
                                                "Buyer for 20 Acres",
                                                "Price of Gold Soars",
                                                "Car Wash Buyer",
                                                "Software Company Buyer",
                                                "Apartment House Buyer",
                                                "House Buyer - 3Br/2Ba",
                                                "Limited Partnership Sold",
                                                "Plex Buyer"]:
            marketCardDeck.addCard(MarketCard(marketCardsDict[card]["Title"],
                                              int(marketCardsDict[card]["Cost"]),
                                              0,  # - 3 - Increased Cash Flow not used
                                              marketCardsDict[card]["Must Sell"]))
        elif marketCardsDict[card]["Title"] == "Interest Rates Drop!":
            marketCardDeck.addCard(MarketCard(marketCardsDict[card]["Title"],
                                              int(marketCardsDict[card]["Cost"]),
                                              0,  # - 3 - Increased Cash Flow not used
                                              marketCardsDict[card]["Must Sell"],
                                              marketCardsDict[card]["Self Only"]))
        elif marketCardsDict[card]["Title"] == "Inflation Hits!":
            marketCardDeck.addCard(MarketCard(marketCardsDict[card]["Title"],
                                              0,  # - 4 - Cost not used),
                                              0,  # - 3 - Increased Cash Flow not used
                                              True,
                                              True))
        else:
            print("Known Market card not found in row: ", marketCardsDict[card])
    return marketCardDeck


def loadAllSmallDealCards(smallDealCardsFilename):
    try:
        smallDealCardsDict = load_json(smallDealCardsFilename)
    except OSError:
        print("No good Small Deal Cards json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good Small Deal Cards json file found, ValueError, please fix")
        raise ValueError
#    else:
#        noSmallDealCards = len(smallDealCardsDict)
#        print(noSmallDealCards, "Small Deal Cards loaded")

    smallDealCardDeck = Deck("Small Deal Cards")
    for card in smallDealCardsDict:
        if smallDealCardsDict[card]["Type"] == "Stock":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unused for stock
                                                    smallDealCardsDict[card]["Symbol"],
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    0,              #6-Unused
                                                    int(smallDealCardsDict[card]["Dividend"]),
                                                    0,              #8-Unused
                                                    int(smallDealCardsDict[card]["Price Range Low"]),
                                                    int(smallDealCardsDict[card]["Price Range High"]),
                                                    True))
        elif smallDealCardsDict[card]["Type"] == "StockSplit":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unsed for stock split
                                                    smallDealCardsDict[card]["Symbol"],
                                                    0,              #5-Unused
                                                    0,              #6-Unused
                                                    0,              #7-Unused
                                                    float(smallDealCardsDict[card]["Split Ratio"]),
                                                    0,              #9-Unused
                                                    0,              #10-Unused
                                                    True))
        elif smallDealCardsDict[card]["Type"] == "HouseForSale":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    smallDealCardsDict[card]["HouseOrCondo"],
                                                    "",             #4-Unused
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    int(smallDealCardsDict[card]["Down Payment"]),
                                                    int(smallDealCardsDict[card]["Cash Flow"]),
                                                    0,              #8-Unused
                                                    int(smallDealCardsDict[card]["Price Range Low"]),
                                                    int(smallDealCardsDict[card]["Price Range High"])))
        elif smallDealCardsDict[card]["Type"] == "StartCompany":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unused
                                                    "",             #Unsed
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    int(smallDealCardsDict[card]["Down Payment"]),
                                                    int(smallDealCardsDict[card]["Cash Flow"]),
                                                    0,              #8-Unused
                                                    0,              #9-Unused
                                                    0,              #10-Unused
                                                    0))             #11-Unused
        elif smallDealCardsDict[card]["Type"] == "Asset":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unused
                                                    "",             #Unsed
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    int(smallDealCardsDict[card]["Cost"]), # = Down Payment
                                                    int(smallDealCardsDict[card]["Cash Flow"]),
                                                    0,              #8-Unused
                                                    int(smallDealCardsDict[card]["Price Range Low"]),
                                                    int(smallDealCardsDict[card]["Price Range High"])))
        elif smallDealCardsDict[card]["Type"] == "Land":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unused
                                                    "",             #Unsed
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    int(smallDealCardsDict[card]["Down Payment"]),
                                                    int(smallDealCardsDict[card]["Acres"]),
                                                    0,              #8-Unused
                                                    0,              #9-Unused
                                                    0,              #10-Unused
                                                    0))             #11-Unused
        elif smallDealCardsDict[card]["Type"] == "LoanNotToBeRepaid":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unused
                                                    "",             #Unsed
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    0,              #6-Unused
                                                    0,              #7-Unused
                                                    0,              #8-Unused
                                                    0,              #9-Unused
                                                    0,              #10-Unused
                                                    0))             #11-Unused
        elif smallDealCardsDict[card]["Type"] == "CostIfRentalProperty":
            smallDealCardDeck.addCard(SmallDealCard(smallDealCardsDict[card]["Title"],
                                                    smallDealCardsDict[card]["Type"],
                                                    "",             #Unused
                                                    "",             #Unsed
                                                    int(smallDealCardsDict[card]["Cost"]),
                                                    0,              #6-Unused
                                                    0,              #7-Unused
                                                    0,              #8-Unused
                                                    0,              #9-Unused
                                                    0,              #10-Unused
                                                    0))             #11-Unused
        else:
            print("Small Deal Card known card not found in record: ", smallDealCardsDict[card])
    return smallDealCardDeck

def loadAllBigDealCards(bigDealCardsFilename):
    try:
        bigDealCardsDict = load_json(bigDealCardsFilename)
    except OSError:
        print("No good Big Deal Cards json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good Big Deal Cards json file found, ValueError, please fix")
        raise ValueError
#    else:
#        noBigDealCards = len(bigDealCardsDict)
#        print(noBigDealCards, "Big Deal Cards loaded")

    bigDealCardDeck = Deck("Big Deal Cards")
    for card in bigDealCardsDict:
        if bigDealCardsDict[card]["Type"] in ["ApartmentHouseForSale", "XPlex"]:
            bigDealCardDeck.addCard(BigDealCard(bigDealCardsDict[card]["Title"],
                                                bigDealCardsDict[card]["Type"],
                                                int(bigDealCardsDict[card]["Cost"]),
                                                int(bigDealCardsDict[card]["Down Payment"]),
                                                int(bigDealCardsDict[card]["Cash Flow"]),
                                                int(bigDealCardsDict[card]["Units"]),
                                                0,              #7-Acres-unused
                                                int(bigDealCardsDict[card]["Price Range Low"]),
                                                int(bigDealCardsDict[card]["Price Range High"]),
                                                0,              #10-unused-Cost if Have Real Estate
                                                0))             #11-unused-Cost if Have 8-Plex
        elif bigDealCardsDict[card]["Type"] in ["HouseForSale", "Business"]:
            bigDealCardDeck.addCard(BigDealCard(bigDealCardsDict[card]["Title"],
                                                bigDealCardsDict[card]["Type"],
                                                int(bigDealCardsDict[card]["Cost"]),
                                                int(bigDealCardsDict[card]["Down Payment"]),
                                                int(bigDealCardsDict[card]["Cash Flow"]),
                                                0,              #6-Units-unused
                                                0,              #7-Acres-unused
                                                int(bigDealCardsDict[card]["Price Range Low"]),
                                                int(bigDealCardsDict[card]["Price Range High"]),
                                                0,              #10-unused-Cost if Have Real Estate
                                                0))             #11-unused-Cost if Have 8-Plex
        elif bigDealCardsDict[card]["Type"] == "Land":
            bigDealCardDeck.addCard(BigDealCard(bigDealCardsDict[card]["Title"],
                                                bigDealCardsDict[card]["Type"],
                                                int(bigDealCardsDict[card]["Cost"]),
                                                int(bigDealCardsDict[card]["Down Payment"]),
                                                int(bigDealCardsDict[card]["Cash Flow"]),
                                                0,              #6-Units-unused
                                                int(bigDealCardsDict[card]["Acres"]),
                                                0,              #8-Price Range Low
                                                0,              #9-Price Range High
                                                0,              #10-unused-Cost if Have Real Estate
                                                0))             #11-unused-Cost if Have 8-Plex
        elif bigDealCardsDict[card]["Type"] == "Expense":
            bigDealCardDeck.addCard(BigDealCard(bigDealCardsDict[card]["Title"],
                                                bigDealCardsDict[card]["Type"],
                                                0,              #3-Cost
                                                0,              #4-Down Payment
                                                0,              #5-Cash Flow
                                                0,              #6-Units-unused
                                                0,              #7-Acres-unused
                                                0,              #8-Price Range Low
                                                0,              #9-Price Range High
                                                int(bigDealCardsDict[card]["Cost If Have Real Estate"]),
                                                int(bigDealCardsDict[card]["Cost If Have 8-Plex"])))
        else:
            print("Big Deal Card known card not found in record: ", bigDealCardsDict[card])
    return bigDealCardDeck


class Deck(object):
    def __init__(self, deckType):
        self.deckType = deckType
        self.cards = []
    def getDeckType(self):
        return self.deckType
    def getCards(self):
        return self.Cards
    def getNoCards(self):
        return len(self.cards)
    def addCard(self, card):
        self.cards.append(card)
        return self.getNoCards()
    def takeRandomCard(self):
        import random
        try:
            return self.cards.pop(int(random.random()*self.getNoCards()))
        except IndexError:
            return None
    def takeTopCard(self):
        try:
            return self.cards.pop()
        except IndexError:
            return None
    def shuffle(self):
        import random
        random.shuffle(self.cards)
    def __copy__(self):
        newDeck = Deck(self.deckType)
        for card in self.cards:
            newDeck.addCard(card)
        return newDeck
    def __str__(self):
        cardString = ""
        for card in self.cards:
            cardString = cardString + str(card) + "\n"
        return cardString[:-1]


if __name__ == '__main__':      #test Card Objects
    smallDealCardDeck = loadAllSmallDealCards("SmallDealCards.json")
    bigDealCardDeck = loadAllBigDealCards("BigDealCards.json")
    doodadCardDeck = loadAllDoodadCards("DoodadCards.json")
    marketCardDeck = loadAllMarketCards("MarketCards.json")
    
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards())
#    print(smallDealCardDeck)
    print("No. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())
#    print(bigDealCardDeck)
    print("No. of Doodad     Cards: ", doodadCardDeck.getNoCards())
#    print(doodadCardDeck)
    print("No. of Market     Cards: ", marketCardDeck.getNoCards())
#    print(marketCardDeck)

    bDCPR = []
    bDCPRError = []
    while True:
        bigDealCard = bigDealCardDeck.takeTopCard()
        try:
            bDCPR.append((bigDealCard.getPrice()-bigDealCard.getPriceRangeLow())/(bigDealCard.getPriceRangeHigh()-bigDealCard.getPriceRangeLow()))
            #print(bigDealCard.getTitle(), bDCPR[-1])
        except AttributeError:
            print("No Market Value, MAX or MIN on card:", bigDealCard.getTitle())
        except ZeroDivisionError:
            bDCPRError.append((bigDealCard.getDownPayment(),'No Price Range', "Card:"+bigDealCard.getTitle()))
        if bigDealCardDeck.getNoCards() == 0:
            break

    bDCPR.sort()

    for aPR in bDCPR:
        print("{:.3f}".format(aPR))
    print("\n\n")
    for aPR in bDCPRError:
        print(aPR)
        
    print("\n\n\n")
    
    bDCROI = []
    bigDealCardDeck = loadAllBigDealCards("BigDealCards.json")
    while True:
        bigDealCard = bigDealCardDeck.takeTopCard()
        try:
            bDCROI.append(bigDealCard.getCashFlow()*12/bigDealCard.getDownPayment())
        except AttributeError:
            print("No ROI on card:", bigDealCard.getTitle())
        if bigDealCardDeck.getNoCards() == 0:
            break

    bDCROI.sort()

    for anROI in bDCROI:
        print("{:.3f}".format(anROI))


#NEXT TO TRY - DECK METHODS - SHUFFLE, DEAL CARD, ETC. - COMPLETE
"""
    while True:
        card = smallDealCardDeck.takeTopCard()
        if card != None:
            print(card)
            print("Number of cards remaining:", smallDealCardDeck.getNoCards())
        else:
            break
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())
    smallDealCardDeck = loadAllSmallDealCards("SmallDealCards.txt")
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())    
    while True:
        card = smallDealCardDeck.takeRandomCard()
        if card != None:
            print(card)
            print("Number of cards remaining:", smallDealCardDeck.getNoCards())
        else:
            break
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())

    while True:
        card = bigDealCardDeck.takeTopCard()
        if card != None:
            print(card)
            print("Number of cards remaining:", bigDealCardDeck.getNoCards())
        else:
            break

    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())
    bigDealCardDeck = loadAllBigDealCards("BigDealCards.txt")
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())    
    while True:
        card = bigDealCardDeck.takeRandomCard()
        if card != None:
            print(card)
            print("Number of cards remaining:", bigDealCardDeck.getNoCards())
        else:
            break
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())

    
    smallDealCardDeck = loadAllSmallDealCards("SmallDealCards.txt")
    bigDealCardDeck = loadAllBigDealCards("BigDealCards.txt")
    smallDealCardDeck.shuffle()
    bigDealCardDeck.shuffle()
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())
    while True:
        card = smallDealCardDeck.takeTopCard()
        if card != None:
            print(card)
            print("Number of cards remaining:", smallDealCardDeck.getNoCards())
        else:
            break
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())
    while True:
        card = bigDealCardDeck.takeTopCard()
        if card != None:
            print(card)
            print("Number of cards remaining:", bigDealCardDeck.getNoCards())
        else:
            break
    print("No. of Small Deal Cards: ", smallDealCardDeck.getNoCards(), "\nNo. of Big   Deal Cards: ", bigDealCardDeck.getNoCards())
    print("Small Deck Type:", smallDealCardDeck.getDeckType(), "\nBig   Deck Type:", bigDealCardDeck.getDeckType())

"""

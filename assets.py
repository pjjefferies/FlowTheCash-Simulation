class Asset(object):
    def __init__(self, name, assetType, cost, downPayment,
                 cashFlow, priceRangeLow, priceRangeHigh):
        self.name = name
        self.type = assetType
        self.cost = cost
        self.downPayment = downPayment
        self.cashFlow = cashFlow
        self.priceRangeLow = priceRangeLow
        self.priceRangeHigh = priceRangeHigh
    def getName(self):
        return self.name
    def getType(self):
        return self.type
    def getCost(self):
        return self.cost
    def getLoanAmount(self):
        return self.cost - self.downPayment
    def getDownPayment(self):
        return self.downPayment
    def getCashFlow(self):
        return self.cashFlow
    def getPriceRangeLow(self):
        return self.priceRangeLow
    def getPriceRangeHigh(self):
        return self.priceRangeHigh
    def getROI(self):
        if self.downPayment > 0:
            return float(self.cashFlow)*12.0/float(self.downPayment)
        else:
            return 1.0
    def __str__(self):
        return ("\n  Type:         " + self.type +
                "\n   Name:        " + self.name +
                "\n   Cost:        " + str(self.cost) +
                "\n   Down Payment:" + str(self.downPayment) +
                "\n   Cash Flow:   " + str(self.cashFlow) +
                "\n   Price Range: " + str(self.priceRangeLow) + " - " +
                str(self.priceRangeHigh) +
                "\n   ROI:         " + str(self.getROI()))
    

class Stock(Asset):
    def __init__(self, stockName, shares, costPerShare, dividendInterest,
                 priceRangeLow, priceRangeHigh):
        Asset.__init__(self, stockName, "Stock", 0, 0, 0,
                       priceRangeLow, priceRangeHigh)
        self.shares = shares
        self.costPerShare = costPerShare
        self.dividendInterest = dividendInterest
    def getNoShares(self):
        return self.shares
    def getCostPerShare(self):
        return self.costPerShare
    def getTotalCost(self):
        return self.shares * self.costPerShare
    def setNoShares(self, shares):
        self.shares = shares
    def stockSplit(self, ratio):
        self.shares *= ratio
    def getDividendInterest(self):
        return self.dividendInterest
    def reduceNoShares(self, sharesToReduce):
        if sharesToReduce < self.shares:
            self.shares -= sharesToReduce
        return self.shares
    def getROI(self):
        if self.dividendInterest == 0:
            return 0.0
        elif self.costPerShare > 0:
            return float(self.dividendInterest)*12.0/float(self.costPerShare)
        else:
            return 1.0
    def __str__(self):
        return ("\n  Type:              " + "Stock" +
                "\n   Symbol:           " + self.name +
                "\n   Shares:           " + str(self.shares) +
                "\n   Cost per Share:   " + str(self.costPerShare) +
                "\n   Total Cost:       " + str(self.shares * self.costPerShare) +
                "\n   Dividends/share:  " + str(self.dividendInterest) +
                "\n   Price Range: " + str(self.priceRangeLow) + " - " +
                str(self.priceRangeHigh) +
                "\n   ROI:              " + str(self.getROI()))

class RealEstate(Asset):
    def __init__(self, name, realEstateType, houseOrCondo, cost, downPayment, cashFlow=0,
                 priceRangeLow=0, priceRangeHigh=0,
                 units=0,
                 acres = 0):
        Asset.__init__(self, name, realEstateType, cost, downPayment,
                       cashFlow, priceRangeLow, priceRangeHigh)
        self.houseOrCondo = houseOrCondo
        self.units = units
        self.acres = acres
    def getHouseOrCondo(self):
        return self.houseOrCondo
    def getUnits(self):
        return self.units
    def getAcres(self):
        return self.acres
    def getLoanAmount(self):
        return self.cost - self.downPayment
    def __str__(self):
        return ("\n  Type:        " + self.type +
                "\n   Name:        " + self.name +
                "\n   HouseOrCondo " + str(self.houseOrCondo) +
                "\n   Cost:        " + str(self.cost) +
                "\n   Down Payment:" + str(self.downPayment) +
                "\n   Cash Flow:   " + str(self.cashFlow) +
                "\n   Units:       " + str(self.units) +
                "\n   Acres:       " + str(self.acres) +
                "\n   Price Range: " + str(self.priceRangeLow) + " - " +
                                       str(self.priceRangeHigh) +
                "\n   ROI:         " + str(self.getROI()))

class Business(Asset):
    def __init__(self, name, cardType, cost, downPayment, cashFlow=0,
               priceRangeLow=0, priceRangeHigh=0):
        Asset.__init__(self, name, cardType, cost, downPayment,
                       cashFlow, priceRangeLow, priceRangeHigh)
    def increaseCashFlow(self, increaseAmount):
        self.cashFlow += increaseAmount
        return self.cashFlow
    def getLoanAmount(self):
        return self.cost - self.downPayment    


if __name__ == '__main__':      #asset sub-classes
    from cards import *
    import copy
    smallDealCardDeckMaster = loadAllSmallDealCards("SmallDealCards.json")
    bigDealCardDeckMaster = loadAllBigDealCards("BigDealCards.json")

    smallDealCardDeck = copy.copy(smallDealCardDeckMaster)
    bigDealCardDeck = copy.copy(bigDealCardDeckMaster)

#    smallDealCardDeck.shuffle()
#    bigDealCardDeck.shuffle()

    assetList = []

    while True:
        smallDealCard = smallDealCardDeck.takeTopCard()
        if smallDealCard == None:
            break
#        print("Small Deal Card Type: ", smallDealCard.getCardType())
        if smallDealCard.getCardType() in ["Stock", "CD"]:
            assetList.append(Stock(smallDealCard.getSymbol(),
                                   100,     #shares
                                   smallDealCard.getPrice(),
                                   smallDealCard.getDividend(),
                                   smallDealCard.getPriceRangeLow(),
                                   smallDealCard.getPriceRangeHigh()))
        elif smallDealCard.getCardType() == "HouseForSale":
            assetList.append(RealEstate(smallDealCard.getTitle(),
                                        smallDealCard.getCardType(),
                                        smallDealCard.getHouseOrCondo(),
                                        smallDealCard.getPrice(),
                                        smallDealCard.getDownPayment(),
                                        smallDealCard.getCashFlow(),
                                        smallDealCard.getPriceRangeLow(),
                                        smallDealCard.getPriceRangeHigh(),
                                        0,0))
        elif smallDealCard.getCardType() == "StartCompany":
            assetList.append(Business(smallDealCard.getTitle(),
                                      smallDealCard.getCardType(),
                                      smallDealCard.getPrice(),
                                      smallDealCard.getDownPayment(),
                                      smallDealCard.getCashFlow(),
                                      0,    #no Price Range for Small Deal Co.
                                      0))    #no Price Range for Small Deal Co.
        elif smallDealCard.getCardType() == "Land":
            assetList.append(RealEstate(smallDealCard.getTitle(),
                                        smallDealCard.getCardType(),
                                        smallDealCard.getHouseOrCondo(),
                                        smallDealCard.getPrice(),
                                        smallDealCard.getDownPayment(),
                                        0,  #no cash flow
                                        0,  #no Price Range Low
                                        0,  #no Price Range High,
                                        0,  #no units
                                        smallDealCard.getAcres()))
        elif smallDealCard.getCardType() =="Asset":
            assetList.append(Asset(smallDealCard.getTitle(),
                                   smallDealCard.getCardType(),
                                   smallDealCard.getPrice(),
                                   0,       #no Down Payment on Small Deal Assets
                                   smallDealCard.getCashFlow(),
                                   smallDealCard.getPriceRangeLow(),
                                   smallDealCard.getPriceRangeHigh()))
        else:
            print("Small Card type:", smallDealCard.getCardType(), "not found")


    while True:
        bigDealCard = bigDealCardDeck.takeTopCard()
        if bigDealCard == None:
            break
#        print("Big Deal Card Type: ", bigDealCard.getCardType())
        if bigDealCard.getCardType() in ["ApartmentHouseForSale", "XPlex"]:
            assetList.append(RealEstate(bigDealCard.getTitle(),
                                        bigDealCard.getCardType(),
                                        bigDealCard.getHouseOrCondo(),
                                        bigDealCard.getPrice(),
                                        bigDealCard.getDownPayment(),
                                        bigDealCard.getCashFlow(),
                                        bigDealCard.getPriceRangeLow(),
                                        bigDealCard.getPriceRangeHigh(),
                                        bigDealCard.getUnits(),
                                        0))    #no acres
        elif bigDealCard.getCardType() == "HouseForSale":
            #print("HouseForSale bigDealCard:", bigDealCard)
            #print(bigDealCard.getTitle() + ", " +
             #     bigDealCard.getCardType()  + ", " +
             #     str(bigDealCard.getPrice())  + ", " +
             #     str(bigDealCard.getHouseOrCondo()) + ", " +
             #     str(bigDealCard.getDownPayment())  + ", " +
             #     str(bigDealCard.getCashFlow())  + ", " +
             #     str(bigDealCard.getPriceRangeLow())  + ", " +
             #     str(bigDealCard.getPriceRangeHigh())  + ", " +
             #     str(0)  + ", " +
             #     str(0))
            assetList.append(RealEstate(bigDealCard.getTitle(),
                                        bigDealCard.getCardType(),
                                        bigDealCard.getHouseOrCondo(),
                                        bigDealCard.getPrice(),
                                        bigDealCard.getDownPayment(),
                                        bigDealCard.getCashFlow(),
                                        bigDealCard.getPriceRangeLow(),
                                        bigDealCard.getPriceRangeHigh(),
                                        0,      #no units
                                        0))    #no acres
        elif bigDealCard.getCardType() in ["Partnership", "Business"]:
            assetList.append(Business(bigDealCard.getTitle(),
                                      bigDealCard.getCardType(),
                                      bigDealCard.getPrice(),
                                      bigDealCard.getDownPayment(),
                                      bigDealCard.getCashFlow(),
                                      bigDealCard.getPriceRangeLow(),
                                      bigDealCard.getPriceRangeHigh()))
        elif bigDealCard.getCardType() == "Land":
            assetList.append(RealEstate(bigDealCard.getTitle(),
                                        bigDealCard.getCardType(),
                                        bigDealCard.getPrice(),
                                        bigDealCard.getDownPayment(),
                                        bigDealCard.getCashFlow(),
                                        bigDealCard.getPriceRangeLow(),
                                        bigDealCard.getPriceRangeHigh(),
                                        0,   #no units
                                        bigDealCard.getAcres()))
        else:
            print("Big Card type:", bigDealCard.getCardType(), "not found")

    for asset in assetList:
        print(asset)

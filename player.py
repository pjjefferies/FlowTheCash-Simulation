import loans
import assets
import player_choice
import jsonReadWriteFile


class Profession(object):
    def __init__(self, profession, salary, expenseTaxes, expenseOther, costPerChild, savings, loanList = None):
                                                    #loanList = list of Loan objects
        self.profession = profession
        self.salary = salary
        self.expenseTaxes = expenseTaxes
        self.expenseOther = expenseOther
        self.costPerChild = costPerChild
        self.savings = savings
        if loanList == None:
            self.loanList = []
        else:
            self.loanList = loanList
        #print("Creating Profession:\n   profession:", selfprofession,
        #      "\n   salary:", self.salary,
        #      "\n   expenseTaxes:", self.expenseTaxes,
        #      "\n   expenseOther:", self.expenseOther,
        #      "\n   costPerChild:", self.costPerChild,
        #      "\n   savings:", self.savings,
        #      "\n   loanList:", self.loanList, "\n\n")
        #input("Enter to continue")
    def getProfession(self):
        return self.profession
    def getSalary(self):
        return self.salary
    def getExpenseTaxes(self):
        return self.expenseTaxes
    def getExpenseOther(self):
        return self.expenseOther
    def getCostPerChild(self):
        return self.costPerChild
    def getSavings(self):
        return self.savings
    def getLoans(self):
        return self.loanList
    def __str__(self):
        loanStrList = ""
        for loan in self.loanList:
            loanStrList = loanStrList + str(loan) + "\n"
        loanStrList = loanStrList[:-1]
        return ("\nProfession:     " + self.profession +
                "\nSalary:         " + str(self.salary) +
                "\nTaxes:          " + str(self.expenseTaxes) +
                "\nOther Expenses: " + str(self.expenseOther) +
                "\nCost per Child: " + str(self.costPerChild) +
                "\nSavings:        " + str(self.savings) +
                "\nNo. Loans:      " + str(len(self.loanList)) +
                "\n" + loanStrList)


class Strategy(object):
    def __init__(self, strategyName, manual = True, roiThreshold = 0.20,
                 priceRatioThreshold = 0.5, takeDownpaymentLoans = False,
                 takeAnyLoans = True, charitable = True,
                 bigDealSmallDealThreshold = 5000, loanPayback="Highest Interest"):
        self.strategyName = strategyName
        if manual == True:
            self.manual = True
        else:
            self.manual = False
        self.roiThreshold = float(roiThreshold)
        self.priceRatioThreshold = float(priceRatioThreshold)
        self.takeDownpaymentLoans = bool(takeDownpaymentLoans and takeAnyLoans)
        self.takeAnyLoans = bool(takeAnyLoans)
        self.charitable = bool(charitable)
        self.bigDealSmallDealThreshold = int(bigDealSmallDealThreshold)
        if loanPayback in ["Smallest", "Largest", "Never", "Higest Interest"]:
            self.loanPayback = loanPayback
        else:
            self.loanPayback = "Highest Interest"
    def getName(self):
        return self.strategyName
    def getManual(self):
        return self.manual
    def getROIThreshold(self):
        return self.roiThreshold
    def getPriceRatioThreshold(self):
        return self.priceRatioThreshold
    def getTakeDownPaymentLoans(self):
        return self.takeDownpaymentLoans
    def getTakeAnyLoans(self):
        return self.takeAnyLoans
    def getCharitable(self):
        return self.charitable
    def getBigDealSmallDealThreshold(self):
        return self.bigDealSmallDealThreshold
    def getLoanPayback(self):
        return self.loanPayback
    def __str__(self):
        return ("\n Strategy Name:              " + str(self.strategyName) +
                "\n Manual:                     " + str(self.manual) +
                "\n ROI Threshold:              " + str(self.roiThreshold) +
                "\n Price Ratio Threshold:      " + str(self.priceRatioThreshold) +
                "\n Take Downpayment Loans:     " + str(self.takeDownpaymentLoans) +
                "\n Take Any Loans:             " + str(self.takeAnyLoans) +
                "\n Charitable:                 " + str(self.charitable) +
                "\n Big Deal Savings Threshold: " + str(self.bigDealSmallDealThreshold) +
                "\n Loan Payback Strategy:      " + str(self.loanPayback))



class Player(object):
    def __init__(self, name, profession, strategy): #profession as a Profession object
        self.name = name
        self.profession = profession.getProfession()
        self.salary = profession.getSalary()
        self.expenseTaxes = profession.getExpenseTaxes()
        self.expenseOther = profession.getExpenseOther()
        self.costPerChild = profession.getCostPerChild()
        self.savings = profession.getSavings()
        self.loanList = profession.getLoans().copy()
        self.strategy = strategy
        self.noChildren = 0
        self.stockAssets = []
        self.realEstateAssets = []
        self.businessAssets = []
        self.soldAssets = []    #list of sold assets: [asset, sale price)
        self.charityTurnsRemaining = 0
        self.skippedTurnsRemaining = 0
        self.amIRich = False
        self.amIBroke = False
        #print("\n\n\nCreating Player:\n   self.name:", self.name,
        #      "\nprofession:", self.profession,
        #      "\nsalary:", self.salary,
        #      "\nexpenseTaxes:", self.expenseTaxes,
        #      "\nexpenseOther:", self.expenseOther,
        #      "\ncostPerChild:", self.costPerChild,
        #      "\nsavings:", self.savings,
        #      "\n# Loans:", len(self.loanList),
        #      "\n# Loans in strategy:", len(profession.getLoans()),
        #      "\nstrategy:", self.strategy.getName(),
        #      "\nnoChildren:", self.noChildren,
        #      "\n# Stock:", len(self.stockAssets),
        #      "\n# Real Estate Assets:", len(self.realEstateAssets),
        #      "\n# Business Assets:", len(self.businessAssets),
        #      "\n# Sold Assets:", len(self.soldAssets),
        #      "\nCharity Turns:", self.charityTurnsRemaining,
        #      "\nSkipped Turns:", self.skippedTurnsRemaining,
        #      "\namIRich:", self.amIRich,
        #      "\namIPoor:", self.amIBroke)
        #input("Enter to continue")
    def getName(self):
        return self.name
    def getProfession(self):
        return self.profession
    def getStrategy(self):
        return self.strategy
    def getSalary(self):
        return self.salary
    def earnSalary(self):
        self.refresh()
        self.savings = int(self.savings + self.monthlyCashFlow)
        return
    def getTaxes(self):
        return self.expenseTaxes
    def getOtherExpenses(self):
        return self.expenseOther
    def getChildCost(self):
        return self.costPerChild
    def getSavings(self):
        return self.savings
    def getPassiveIncome(self):
        self.passiveIncome = 0
        for stock in self.stockAssets:
            self.passiveIncome += stock.getDividendInterest()
        for realEstate in self.realEstateAssets:
            self.passiveIncome += realEstate.getCashFlow()
        for business in self.businessAssets:
            self.passiveIncome += business.getCashFlow()
        return self.passiveIncome
    def getLoans(self):
        return self.loanList
    def getSoldAssets(self):
        return self.soldAssets
    def getNoChildren(self):
        return self.noChildren
    def getMonthlyCashFlow(self):
        self.refresh()
        return self.monthlyCashFlow
    def makeLoan(self, loan):
        self.loanList.append(loan)
        self.savings += loan.getBalance()
    def setStrategy(self, strategy):
        self.strategy = strategy        #as a strategy object
        return
    def startCharityTurns(self):
        self.charityTurnsRemaining = 3
        return
    def getCharityTurns(self):
        return self.charityTurnsRemaining
    def useCharityTurn(self):
        self.charityTurnsRemaining -= 1
    def startLayoff(self):
        self.skippedTurnsRemaining = 2
        return
    def getSkippedTurnsRemaining(self):
        return self.skippedTurnsRemaining
    def useLayoff(self):
        self.skippedTurnsRemaining -= 1
    def makePayment(self, payment):
        self.savings -= payment
    def getTotalExpenses(self):
        loanCost = 0
        for loan in self.loanList:
            loanCost += loan.getMonthlyPayment()
        self.totalExpenses = (  self.expenseTaxes
                              + self.expenseOther
                                + self.costPerChild * self.noChildren
                                + loanCost)
        return self.totalExpenses
    def payoffLoan(self, loanNumber):
        if self.savings >= self.loanList[loanNumber].getBalance():
            self.savings -= self.loanList[loanNumber].getBalance()
            self.loanList.pop(loanNumber)
            return True
        else:
            return False

    def buyStock(self, stockAsset, costPerShare=0, verbose=True):
        if costPerShare == 0:
            costPerShare = stockAsset.getCostPerShare()
        if (stockAsset.getNoShares() * stockAsset.getCostPerShare()) > self.savings:
            loanAmount = int(round((float(costPerShare * stockAsset.getNoShares() - self.savings)/1000.0)+0.4999,0)*1000)
            if assets.chooseToGetLoanToBuyAsset(self, stockAsset, loanAmount, verbose):
                self.makeLoan(loans.Loan("Bank Loan", loanAmount, int(loanAmount / 10), True))
            else:
                return False
        self.stockAssets.append(stockAsset)
        self.savings -= stockAsset.getNoShares() * costPerShare
        return True

    def sellStock(self, asset, price, noShares, verbose=True):
        if asset in self.stockAssets:
            ownedShares = asset.getNoShares()
            if noShares > ownedShares:
                if verbose:
                    print("Requested to sell " + noShares + " but you only have " + ownedShares + "." +
                          "\nSelling all")
                noShares = ownedShares
            if noShares < ownedShares:
                if verbose:
                    print("Partial sale of " + noShares + " of " + ownedShares + ".")
                asset.reduceNoShares(noShares)
            else:
                if verbose:
                    print("Selling all " + noShares + " of " + asset.getName())
                self.stockAssets.remove(asset)
                self.soldAssets.append([asset, price*noShares])
            self.savings += price * noShares

    def buyRealEstate(self, realEstateAsset, verbose=True):
        if realEstateAsset.getDownPayment() > self.savings:
            loanAmount = int(round((float(realEstateAsset.getDownPayment() - self.savings)/1000.0)+0.4999,0)*1000)
            if player_choice.chooseToGetLoanToBuyAsset(self, realEstateAsset, loanAmount, verbose):
                self.makeLoan(loans.Loan("Bank Loan", loanAmount, int(loanAmount / 10), True))
            else:
                return False
        self.realEstateAssets.append(realEstateAsset)
        self.savings -= realEstateAsset.getDownPayment()
        return True

    def sellRealEstate(self, asset, price, verbose):
        if asset in self.realEstateAssets:
            self.savings += (price - asset.getLoanAmount())
            self.realEstateAssets.remove(asset)
            self.soldAssets.append([asset, price])
            if verbose:
                print("Sold " + asset.getName() + ", " + asset.getType() + " for " + str(price) + ".")

    def buyBusiness(self, businessAsset, verbose=True):
        if businessAsset.getDownPayment() > self.savings:
            loanAmount = int(round((float(businessAsset.getDownPayment() - self.savings)/1000.0)+0.4999,0)*1000)
            if player_choice.chooseToGetLoanToBuyAsset(self, businessAsset, loanAmount, verbose):
                self.makeLoan(loans.Loan("Bank Loan", loanAmount, int(loanAmount / 10), True))
            else:
                return False
        self.businessAssets.append(businessAsset)
        self.savings -= businessAsset.getDownPayment()
        return True

    def sellBusiness(self, asset, price, verbose=True):
        if asset in self.businessAssets:
            self.businessAssets.remove(asset)
            self.savings += (price - asset.getLoanAmount())
            self.soldAssets.append([asset, price])
            if verbose:
                print("Sold " + asset.getName() + ", " + asset.getType() + " for " + price + ".")
    def getStockAssets(self):
        return self.stockAssets
    def getRealEstateAssets(self):
        return self.realEstateAssets
    def getBusinessAssets(self):
        return self.businessAssets
    def haveChild(self, verbose=False):
        if self.noChildren >= 3:
            if verbose:
                print("Three kids is enough for anyone")
            return self.noChildren
        self.noChildren += 1
        return self.noChildren
    def refresh(self):      #recalculate total income, passive income, total expenses, amIRich, amIPoor
        self.passiveIncome = self.getPassiveIncome()
        self.totalExpenses = self.getTotalExpenses()
#        int(self.expenseTaxes + self.expenseOther + self.costPerChild * self.noChildren)
#        for stock in self.stockAssets:
#            self.passiveIncome += stock.getDividendInterest()
#        for realEstate in self.realEstateAssets:
#            self.passiveIncome += realEstate.getCashFlow()
#        for business in self.businessAssets:
#            self.passiveIncome += business.getCashFlow()
#        for loan in self.loanList:
#            self.totalExpenses += loan.getMonthlyPayment()
        self.totalIncome = self.salary + self.passiveIncome
        self.monthlyCashFlow = self.totalIncome - self.totalExpenses
        if self.monthlyCashFlow < 0 and (-1 * self.monthlyCashFlow > self.savings):     #Sorry, you're broke!
            self.amIBroke = True
            self.amIRich = False
        elif self.passiveIncome > self.totalExpenses:   #Congratulatios, you're rich!
            self.amIBroke = False
            self.amIRich = True
        else:
            self.amIBroke = False
            self.amIRich = False
        return self.amIRich, self.amIBroke
    def __str__(self):
        self.refresh()
        loanStrList = ""
        for loan in self.loanList:
            loanStrList = loanStrList + str(loan) + "\n"
        loanStrList = loanStrList[:-1]
        assetStrList = ""
        for asset in self.stockAssets:
            assetStrList = assetStrList + str(asset) + "\n"
        for asset in self.realEstateAssets:
            assetStrList = assetStrList + str(asset) + "\n"
        for asset in self.businessAssets:
            assetStrList = assetStrList + str(asset) + "\n"
        assetStrList = assetStrList[:-1]
        return ("\nName:              " + self.name +           #TO DO, right justify and format numbers
                "\nProfession:        " + self.profession +
                "\nSalary:            " + str(self.salary) +
                "\nTaxes:             " + str(self.expenseTaxes) +
                "\nOther Expenses:    " + str(self.expenseOther) +
                "\nChildren:          " + str(self.noChildren) +
                "\nCost per Child:    " + str(self.costPerChild) +
                "\nSavings:           " + str(self.savings) +
                "\nTotal Income:      " + str(self.totalIncome) +
                "\nPassive Income:    " + str(self.passiveIncome) +
                "\nTotal Expenses:    " + str(self.totalExpenses) +
                "\nMonthly Cash Flow: " + str(self.monthlyCashFlow) +
                "\n\nNo. Loans:         " + str(len(self.loanList)) +
                "\n"                    + loanStrList +
                "\n\nNo. Assets:        " + str(len(self.stockAssets)+len(self.realEstateAssets)+len(self.businessAssets)) +
                assetStrList +
                "\nStrategy:          " + str(self.strategy))

def getProfessionDict(professionDictFileName):
    try:
        professionDictTemp = jsonReadWriteFile.load_json(professionDictFileName)
    except OSError:
        print("No good Profession dict json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good Profession dict json file found, ValueError, please fix")
        raise ValueError
    else:
        #noProfessions = len(professionDictTemp)
        #print(noProfessions, "professions loaded")
        professionDict = {}
        for profession in iter(professionDictTemp):
            listOfLoans = []
            for loan in iter(professionDictTemp[profession]["Loans"]):
                if loan == "Bank Loan":
                    partialPaymentAllowed = True
                else:
                    partialPaymentAllowed = False
                listOfLoans.append(loans.Loan(loan,
                                              professionDictTemp[profession]["Loans"][loan]["Balance"],
                                              professionDictTemp[profession]["Loans"][loan]["Payment"],
                                              partialPaymentAllowed))
            professionDict[profession] = Profession(profession,
                                                    professionDictTemp[profession]["Salary"],
                                                    professionDictTemp[profession]["ExpenseTaxes"],
                                                    professionDictTemp[profession]["ExpenseOther"],
                                                    professionDictTemp[profession]["CostPerChild"],
                                                    professionDictTemp[profession]["Savings"],
                                                    listOfLoans)
    return professionDict


def getStrategyDict(strategyDictFileName, verbose = False):
    try:
        strategyDictTemp = jsonReadWriteFile.load_json(strategyDictFileName)
    except OSError:
        print("No good Strategies dict json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good Strategies dict json file found, ValueError, please fix")
        raise ValueError
    else:
        noStrategies = len(strategyDictTemp)
        if verbose:
            print(noStrategies, "strategies loaded")
        strategyDict = {}
        for strategy in iter(strategyDictTemp):
            if strategyDictTemp[strategy].get("manual", "True") == "True":
                manualTemp = True
            else:
                manualTemp = False
            if strategyDictTemp[strategy].get("takeDownpaymentLoans", "True") == "True":
                takeDownpaymentLoansTemp = True
            else:
                takeDownpaymentLoansTemp = False
            if strategyDictTemp[strategy].get("takeAnyLoans", "True") == "True":
                takeAnyLoansTemp = True
            else:
                takeAnyLoansTemp = False
            if strategyDictTemp[strategy].get("charitable", "True") == "True":
                charitableTemp = True
            else:
                charitableTemp = False
            strategyDict[strategy] = Strategy(strategy,
                                              manualTemp,
                                              float(strategyDictTemp[strategy].get("roiThreshold", 0.2)),
                                              float(strategyDictTemp[strategy].get("priceRatioThreshold", 0.5)),
                                              takeDownpaymentLoansTemp,
                                              takeAnyLoansTemp,
                                              charitableTemp,
                                              int(strategyDictTemp[strategy].get("bigDealSmallDealThreshold", 5000)),
                                              str(strategyDictTemp[strategy].get("loanPayback", "Highest Interest")))
    return strategyDict


if __name__ == '__main__':      #test Player Object
    #professionDict = getProfessionDict("ProfessionsList.txt")
    professionDict = getProfessionDict("ProfessionsList.json")
    list_of_players  = []
    #Make Available Strategies to Test
    strategyDict = getStrategyDict("Strategies.json")

    """
    manualStrategy = Strategy(strategyName="Manual", manual = True)
    standardAutoStrategy = Strategy(strategyName="Standard Auto", manual = False)
    daveRamseyAutoStrategy = Strategy(strategyName="Dave Ramsey",
                                      manual = True,
                                      roiThreshold = 0.20,
                                      priceRatioThreshold = 0.5,
                                      takeDownpaymentLoans = False,
                                      takeAnyLoans = False)
    noDownPaymentLoanAutoStrategy = Strategy(strategyName="No Down Payment Loans",
                                             manual = True,
                                             roiThreshold = 0.20,
                                             priceRatioThreshold = 0.5,
                                             takeDownpaymentLoans = False,
                                             takeAnyLoans = True)
    """
    
    for profession in professionDict:       #create player example for each profession
        name = profession + " Player"
        list_of_players.append(Player(name, professionDict[profession], strategyDict["Standard Auto"]))
    print(len(list_of_players), "players created")
    for aPlayer in list_of_players:
        print(aPlayer)
    print("End")

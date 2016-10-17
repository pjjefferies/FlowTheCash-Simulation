class Loan(object):
    def __init__(self,
                 name,
                 balance,
                 monthlyPayment,
                 partialPaymentAllowed = False):
        self.name = name
        self.balance = balance
        self.monthlyPayment = monthlyPayment
        self.partialPaymentAllowed = partialPaymentAllowed
    def getName(self):
        return self.name
    def getBalance(self):
        return self.balance
    def getMonthlyPayment(self):
        return self.monthlyPayment
    def getPartialPaymentAllowed(self):
        return self.partialPaymentAllowed
    def makePayment(self, payment):
        if payment == self.balance or (self.partialPaymentAllowed and
                                       (payment % 1000) == 0 and
                                       payment >= 1000 and
                                       payment <= self.balance):
            self.balance -= payment
            if self.balance == 0:
                return 0, 0
            self.monthlyPayment = int(self.balance * 0.10)     #Rule for Bank Loan, the only partially payable loan
            return self.balance, self.monthlyPayment
        else:
            return None, None
    def __str__(self):
        return ("  Loan Name:          " + self.name +
                "\n   Loan Balance:       " + str(self.balance) +
                "\n   Loan Payment:       " + str(self.monthlyPayment) +
                "\n   Part. Pay. Allowed: " + str(self.partialPaymentAllowed))


if __name__ == '__main__':      #test loan object
    myFirstLoan = Loan("Mortgage", 105000, 1500, False)
    print("My First Loan:" +
          "\nName:             " + myFirstLoan.getName() +
          "\nBalance:          " + str(myFirstLoan.getBalance()) +
          "\nMonthly Payment:  " + str(myFirstLoan.getMonthlyPayment()) +
          "\nPart. Pay. All.?: " + str(myFirstLoan.getPartialPaymentAllowed()))

    print("\nMy Frist Loan String Conversion:\n", myFirstLoan)
    
    print("\nTry partial payment, shouldn't work, return: None, None")
    newBalance, newPayment = myFirstLoan.makePayment(50000)
    print("New Balance:", newBalance, ", New Payment:", newPayment)

    print("\nTry paying-off, should work, return: 0, 0")
    newBalance, newPayment = myFirstLoan.makePayment(105000)
    print("New Balance:", newBalance, ", New Payment:", newPayment)


    mySecondLoan = Loan("Bank Loan", 100000, 10000, True)
    print("\n\n\nMy Second Loan:" +
          "\nName:             " + mySecondLoan.getName() +
          "\nBalance:          " + str(mySecondLoan.getBalance()) +
          "\nMonthly Payment:  " + str(mySecondLoan.getMonthlyPayment()) +
          "\nPart. Pay. All.?: " + str(mySecondLoan.getPartialPaymentAllowed()))

    print("\nMy Seoond Loan String Conversion:\n", mySecondLoan)
    
    print("\nTry partial payment of 6500, shouldn' work, return: None, None")
    newBalance, newPayment = mySecondLoan.makePayment(6500)
    print("New Balance:", newBalance, ", New Payment:", newPayment)

    print("\nTry partial payment of 500, shouldn' work, return: None, None")
    newBalance, newPayment = mySecondLoan.makePayment(500)
    print("New Balance:", newBalance, ", New Payment:", newPayment)

    print("\nTry partial payment of 101000, shouldn' work, return: None, None")
    newBalance, newPayment = mySecondLoan.makePayment(101000)
    print("New Balance:", newBalance, ", New Payment:", newPayment)

    print("\nTry partial paying-off, should work, return: 50000, 5000")
    newBalance, newPayment = mySecondLoan.makePayment(50000)
    print("New Balance:", newBalance, ", New Payment:", newPayment)

    print("\nTry paying-off, should work, return: 0, 0")
    newBalance, newPayment = mySecondLoan.makePayment(50000)
    print("New Balance:", newBalance, ", New Payment:", newPayment)

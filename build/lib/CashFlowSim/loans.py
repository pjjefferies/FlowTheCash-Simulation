"""Object and functions for working with Loans for Game Simulations."""


class Loan(object):
    """Object to manage Loans in Game Simulations."""

    def __init__(self,
                 name,
                 balance,
                 monthly_payment,
                 partial_payment_allowed=False):
        """Create a Loan."""
        self.name = name
        self.balance = balance
        self.monthly_payment = monthly_payment
        self.partial_payment_allowed = partial_payment_allowed

    def make_payment(self, payment):
        """Make a Payment on a Loan."""
        if payment == self.balance or (self.partial_payment_allowed and
                                       (payment % 1000) == 0 and
                                       payment >= 1000 and
                                       payment <= self.balance):
            self.balance -= payment
            if self.balance == 0:
                return True
                # return 0, 0

            # Rule for Bank Loan, the only partially payable loan
            self.monthly_payment = int(self.balance * 0.10)
            # Return nothing, see who complains and why they can't get from
            # properties
            return True
            # return self.balance, self.monthly_payment
        else:
            return False
            # raise valueError(...)
            # return None, None

    def __str__(self):
        """Create string to be returned when str method is called."""
        return ("  Loan Name:          " + self.name +
                "\n   Loan Balance:       " + str(self.balance) +
                "\n   Loan Payment:       " + str(self.monthly_payment) +
                "\n   Part. Pay. Allowed: " +
                str(self.partial_payment_allowed))


if __name__ == '__main__':
    import unittest
    unittest.main(module='loans_test', verbosity=2)

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 23:29:08 2020

@author: PaulJ
"""

import unittest
import cashflowsim.loans as loans


class TestLoans(unittest.TestCase):
    """Test Class to test loans objects in loans module."""

    tests = [{'name': 'Mortgage',
              'initial_balance': 105000,
              'monthly_payment': 1500,
              'partial_payment_allowed': False,
              'payment': 50000,
              'result': False,
              'new_balance': 105000},
             {'name': 'Mortgage',
              'initial_balance': 105000,
              'monthly_payment': 1500,
              'partial_payment_allowed': False,
              'payment': 105000,
              'result': True,
              'new_balance': 0},
             {'name': 'Bank Loan',
              'initial_balance': 100000,
              'monthly_payment': 10000,
              'partial_payment_allowed': True,
              'payment': 6500,
              'result': False,
              'new_balance': 100000},
             {'name': 'Bank Loan',
              'initial_balance': 100000,
              'monthly_payment': 10000,
              'partial_payment_allowed': True,
              'payment': 500,
              'result': False,
              'new_balance': 100000},
             {'name': 'Bank Loan',
              'initial_balance': 100000,
              'monthly_payment': 10000,
              'partial_payment_allowed': True,
              'payment': 10100,
              'result': False,
              'new_balance': 100000},
             {'name': 'Bank Loan',
              'initial_balance': 100000,
              'monthly_payment': 10000,
              'partial_payment_allowed': True,
              'payment': 10000,
              'result': True,
              'new_balance': 90000}
             ]

    def test_loan_and_payment(self):
        """General test using list of tests above."""
        for a_test in self.tests:
            my_loan = loans.Loan(
                name=a_test['name'],
                balance=a_test['initial_balance'],
                monthly_payment=a_test['monthly_payment'],
                partial_payment_allowed=a_test['partial_payment_allowed'])

            result = my_loan.make_payment(a_test['payment'])
            self.assertEqual(result, a_test['result'])
            self.assertEqual(my_loan.balance, a_test['new_balance'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

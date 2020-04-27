# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:31:45 2020

@author: PaulJ
"""

import loans
import json_read_write_file


class Profession(object):
    """Object to manage Professions in Game Simulations."""

    def __init__(self, name, salary, expense_taxes, expense_other,
                 cost_per_child, savings, loan_list=None):
        """Create a profession."""
        self.name = name
        self.salary = salary
        self.expense_taxes = expense_taxes
        self.expense_other = expense_other
        self.cost_per_child = cost_per_child
        self.savings = savings
        if loan_list is None:
            self.loan_list = []
        else:
            self.loan_list = loan_list

    def __str__(self):
        """Create string to be returned when str method is called."""
        loan_str_list = ""
        for loan in self.loan_list:
            loan_str_list = loan_str_list + str(loan) + "\n"
        loan_str_list = loan_str_list[:-1]
        return ("\nProfession:     " + self.name +
                "\nSalary:         " + str(self.salary) +
                "\nTaxes:          " + str(self.expense_taxes) +
                "\nOther Expenses: " + str(self.expense_other) +
                "\nCost per Child: " + str(self.cost_per_child) +
                "\nSavings:        " + str(self.savings) +
                "\nNo. Loans:      " + str(len(self.loan_list)) +
                "\n" + loan_str_list)


def get_profession_defs(profession_defs_fn):
    """Load Professions."""
    try:
        profession_defs_temp = json_read_write_file.load_json(
            profession_defs_fn)
    except OSError:
        print("No good Profession dict json file found, file not found, " +
              "please fix")
        raise OSError
    except ValueError:
        print("No good Profession dict json file found, ValueError, " +
              "please fix")
        raise ValueError
    else:
        profession_defs = {}
        for profession in iter(profession_defs_temp):
            loan_list = []
            for a_loan in iter(profession_defs_temp[profession]["Loans"]):
                if a_loan == "Bank Loan":
                    partial_payment_allowed = True
                else:
                    partial_payment_allowed = False
                loan_list.append(loans.Loan(
                    a_loan,
                    profession_defs_temp[profession]["Loans"][a_loan][
                        "Balance"],
                    profession_defs_temp[profession]["Loans"][a_loan][
                        "Payment"],
                    partial_payment_allowed))
            profession_defs[profession] = Profession(
                profession,
                profession_defs_temp[profession]["Salary"],
                profession_defs_temp[profession]["ExpenseTaxes"],
                profession_defs_temp[profession]["ExpenseOther"],
                profession_defs_temp[profession]["CostPerChild"],
                profession_defs_temp[profession]["Savings"],
                loan_list)
    return profession_defs

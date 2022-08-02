# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:31:45 2020

@author: PaulJ
"""
import logging

from dataclasses import dataclass, field
from typing import Any
from cashflowsim.loans import Loan
from cashflowsim import json_read_write_file

log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Profession(object):
    """Object to manage Professions in Game Simulations."""

    name: str
    salary: int = 0
    expense_taxes: int = 0
    expense_other: int = 0
    cost_per_child: int = 0
    savings: int = 0
    loan_list: list[Loan] = field(default_factory=list)

    def __str__(self) -> str:
        """Create string to be returned when str method is called."""

        loan_str_list = "\n".join(f"{loan}" for loan in self.loan_list)

        prof_header = (
            f"\nProfession:     {self.name}"
            f"\nSalary:         {str(self.salary)}"
            f"\nTaxes:          {str(self.expense_taxes)}"
            f"\nOther Expenses: {str(self.expense_other)}"
            f"\nCost per Child: {str(self.cost_per_child)}"
            f"\nSavings:        {str(self.savings)}"
            f"\nNo. Loans:      {str(len(self.loan_list))}\n"
        )
        return "".join([prof_header, loan_str_list])


def get_profession_defs(profession_defs_fn: str) -> dict[str, Profession]:
    """Load Professions."""
    try:
        profession_defs_temp: dict[
            str, dict[str, Any]
        ] = json_read_write_file.load_json(file_name=profession_defs_fn)
    except OSError:
        err_msg = f"{profession_defs_fn} file not found for loading professions from, please fix...unless this is a test"
        log.error(err_msg)
        raise OSError(err_msg)
    except ValueError:
        err_msg = f"No good Profession dict found in {profession_defs_fn}, ValueError, please fix...unless this is a test"
        log.error(err_msg)
        raise ValueError(err_msg)
    else:
        profession_defs: dict[str, Profession] = {}
        for profession in profession_defs_temp:
            loan_list: list[Loan] = []
            for a_loan in profession_defs_temp[profession]["Loans"]:
                partial_payment_allowed: bool = a_loan == "Bank Loan"
                loan_list.append(
                    Loan(
                        name=a_loan,
                        balance=profession_defs_temp[profession]["Loans"][a_loan][
                            "Balance"
                        ],
                        monthly_payment=profession_defs_temp[profession]["Loans"][
                            a_loan
                        ]["Payment"],
                        partial_payment_allowed=partial_payment_allowed,
                    )
                )
            profession_defs[profession] = Profession(
                name=profession,
                salary=profession_defs_temp[profession]["Salary"],
                expense_taxes=profession_defs_temp[profession]["ExpenseTaxes"],
                expense_other=profession_defs_temp[profession]["ExpenseOther"],
                cost_per_child=profession_defs_temp[profession]["CostPerChild"],
                savings=profession_defs_temp[profession]["Savings"],
                loan_list=loan_list,
            )
    return profession_defs

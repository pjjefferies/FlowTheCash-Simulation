# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:37:08 2020

@author: PaulJ
"""

from cashflowsim import json_read_write_file


class Strategy(object):
    """Manage Strategy for automatically played players."""

    def __init__(self, name, manual=True, roi_threshold=0.20,
                 price_ratio_threshold=0.5, take_downpayment_loans=False,
                 take_any_loans=True, charitable=True,
                 big_deal_small_deal_threshold=5000,
                 loan_payback="Highest Interest"):
        """Create a Strategy."""
        self.name = name
        self.manual = bool(manual)
        self.roi_threshold = float(roi_threshold)
        self.price_ratio_threshold = float(price_ratio_threshold)
        self.take_downpayment_loans = bool(take_downpayment_loans and
                                           take_any_loans)
        self.take_any_loans = bool(take_any_loans)
        self.charitable = bool(charitable)
        self.big_deal_small_deal_threshold = big_deal_small_deal_threshold
        self.loan_payback = (loan_payback if loan_payback in [
            "Smallest", "Largest", "Never", "Higest Interest"] else
            "Highest Interest")

    def __str__(self):
        """Create string to be returned when str method is called."""
        return ("\n Strategy Name:              " + str(self.name) +
                "\n Manual:                     " + str(self.manual) +
                "\n ROI Threshold:              " + str(self.roi_threshold) +
                "\n Price Ratio Threshold:      " +
                str(self.price_ratio_threshold) +
                "\n Take Downpayment Loans:     " +
                str(self.take_downpayment_loans) +
                "\n Take Any Loans:             " + str(self.take_any_loans) +
                "\n Charitable:                 " + str(self.charitable) +
                "\n Big Deal Savings Threshold: " +
                str(self.big_deal_small_deal_threshold) +
                "\n Loan Payback Strategy:      " + str(self.loan_payback))


def get_strategy_defs(strategy_defs_fn, verbose=False):
    """Load Strategies."""
    try:
        strategy_defs_temp = json_read_write_file.load_json(strategy_defs_fn)
    except OSError:
        print("No good Strategies dict json file found, file not found, " +
              "please fix. Filename:", strategy_defs_fn)
        raise OSError
    except ValueError:
        print("No good Strategies dict json file found, ValueError, " +
              "please fix. Filename:", strategy_defs_fn)
        raise ValueError
    else:
        if verbose:
            print(len(strategy_defs_temp), "strategies loaded")
        strategy_defs = {}
        for strategy in iter(strategy_defs_temp):
            if strategy_defs_temp[strategy].get("manual", "True") == "True":
                is_manual = True
            else:
                is_manual = False
            if strategy_defs_temp[strategy].get("takeDownpaymentLoans",
                                                "True"):
                take_downpayment_loans = True
            else:
                take_downpayment_loans = False
            if strategy_defs_temp[strategy].get("takeAnyLoans", "True"):
                take_any_loans = True
            else:
                take_any_loans = False
            if strategy_defs_temp[strategy].get("charitable", "True"):
                charitable = True
            else:
                charitable = False
            strategy_defs[strategy] = Strategy(
                strategy,
                is_manual,
                float(strategy_defs_temp[strategy].get("roiThreshold", 0.2)),
                float(strategy_defs_temp[strategy].get("priceRatioThreshold",
                                                       0.5)),
                take_downpayment_loans,
                take_any_loans,
                charitable,
                int(strategy_defs_temp[strategy].get(
                    "bigDealSmallDealThreshold",
                    5000)),
                str(strategy_defs_temp[strategy].get("loanPayback",
                                                     "Highest Interest")))
    return strategy_defs

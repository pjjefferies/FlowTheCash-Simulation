# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:37:08 2020

@author: PaulJ
"""
import logging
from dataclasses import dataclass
from typing import Dict
from cashflowsim import json_read_write_file

log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Strategy:
    """Manage Strategy for automatically played players."""

    name: str
    manual: bool = True
    roi_threshold: float = 0.20
    price_ratio_threshold: float = 0.5
    take_downpayment_loans: bool = True
    take_any_loans: bool = True
    charitable: bool = True
    big_deal_small_deal_threshold: int = 5000
    loan_payback: str = "Highest Interest"

    def __post_init__(self):
        self.take_downpayment_loans = bool(
            self.take_downpayment_loans and self.take_any_loans
        )
        self.loan_payback = (
            self.loan_payback
            if self.loan_payback in ["Smallest", "Largest", "Never", "Higest Interest"]
            else "Highest Interest"
        )

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"\n Strategy Name:              {str(self.name)}"
            f"\n Manual:                     {str(self.manual)}"
            f"\n ROI Threshold:              {str(self.roi_threshold)}"
            f"\n Price Ratio Threshold:      "
            f"{str(self.price_ratio_threshold)}"
            f"\n Take Downpayment Loans:     "
            f"{str(self.take_downpayment_loans)}"
            f"\n Take Any Loans:             {str(self.take_any_loans)}"
            f"\n Charitable:                 {str(self.charitable)}"
            f"\n Big Deal Savings Threshold: "
            f"{str(self.big_deal_small_deal_threshold)}"
            f"\n Loan Payback Strategy:      {str(self.loan_payback)}"
        )


def get_strategy_defs(*, strategy_defs_fn: str) -> Dict[str, Strategy]:
    """Load Strategies."""
    try:
        strategy_defs_temp = json_read_write_file.load_json(file_name=strategy_defs_fn)
    except OSError:
        print(
            "No good Strategies dict json file found, file not found, "
            + "please fix. Filename:",
            strategy_defs_fn,
        )
        raise OSError
    except ValueError:
        print(
            "No good Strategies dict json file found, ValueError, "
            + "please fix. Filename:",
            strategy_defs_fn,
        )
        raise ValueError
    log.info(f"{len(strategy_defs_temp)} strategies loaded")

    strategy_defs: Dict[str, Strategy] = {}
    for strategy in iter(strategy_defs_temp):
        # log.info(f"Strategy Dict:\n{strategy}\n{strategy_defs_temp[strategy]}\n")
        if strategy_defs_temp[strategy].get("manual", "True") == "True":
            is_manual = True
        else:
            is_manual = False

        if "takeDownpaymentLoans" in strategy_defs_temp[strategy]:
            log.info(
                f"takeDownpaymentLoans: {strategy_defs_temp[strategy]['takeDownpaymentLoans']}"
            )
        if strategy_defs_temp[strategy].get("takeDownpaymentLoans", "True") == "True":
            take_downpayment_loans = True
        else:
            take_downpayment_loans = False

        if strategy_defs_temp[strategy].get("takeAnyLoans", "True") == "True":
            take_any_loans = True
        else:
            take_any_loans = False

        if strategy_defs_temp[strategy].get("charitable", "True") == "True":
            charitable = True
        else:
            charitable = False

        strategy_defs[strategy] = Strategy(
            name=strategy,
            manual=is_manual,
            roi_threshold=float(strategy_defs_temp[strategy].get("roiThreshold", 0.2)),
            price_ratio_threshold=float(
                strategy_defs_temp[strategy].get("priceRatioThreshold", 0.5)
            ),
            take_downpayment_loans=take_downpayment_loans,
            take_any_loans=take_any_loans,
            charitable=charitable,
            big_deal_small_deal_threshold=int(
                strategy_defs_temp[strategy].get("bigDealSmallDealThreshold", 5000)
            ),
            loan_payback=str(
                strategy_defs_temp[strategy].get("loanPayback", "Highest Interest")
            ),
        )
    return strategy_defs

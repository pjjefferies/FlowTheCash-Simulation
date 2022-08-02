"""Object and functions to manage Professions in Game Simulation."""


from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any  # , List
import logging

import cashflowsim.loans as cfs_loans
import cashflowsim.assets as cfs_assets
import cashflowsim.player_choice as cfs_player_choice
import cashflowsim.profession as cfs_profession
import cashflowsim.strategy as cfs_strategy

log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Player:
    """Object to manage Player actions in Game Simulations."""

    name: str
    profession: cfs_profession.Profession
    strategy: cfs_strategy.Strategy
    no_children: int = 0
    charity_turns_remaining: int = 0
    skipped_turns_remaining: int = 0
    am_i_rich: bool = False
    am_i_broke: bool = False
    board_space_no: int = 0
    stock_assets: list[cfs_assets.Stock] = field(default_factory=list)
    real_estate_assets: list[cfs_assets.RealEstate] = field(default_factory=list)
    business_assets: list[cfs_assets.Business] = field(default_factory=list)
    sold_assets: list[tuple[Any, int]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize player."""
        self.salary: int = self.profession.salary
        self.taxes: int = self.profession.expense_taxes
        self.expense_other: int = self.profession.expense_other
        self.cost_per_child: int = self.profession.cost_per_child
        self.savings: int = self.profession.savings
        self.loan_list: list[cfs_loans.Loan] = self.profession.loan_list.copy()

    def earn_salary(self):
        """Earn a salary."""
        self.refresh()
        self.savings = int(self.savings + self.monthly_cash_flow)
        return

    @property
    def passive_income(self) -> int:
        """Return the passive income calculated for the player."""
        passive_income: int = (
            sum([stock.dividend_interest for stock in self.stock_assets])
            + sum([real_estate.cash_flow for real_estate in self.real_estate_assets])
            + sum([business.cash_flow for business in self.business_assets])
        )
        return passive_income

    @property
    def monthly_cash_flow(self) -> int:
        """Return monthly cash flow."""
        return self.total_income - self.total_expenses

    @property
    def total_income(self) -> int:
        """Return total monthly income."""
        return self.salary + self.passive_income

    def make_loan(self, *, loan: cfs_loans.Loan) -> None:
        """Make a new loan if you can."""
        self.loan_list.append(loan)
        self.savings += loan.balance

    def start_charity_turns(self) -> None:
        """Start charity turns where you can roll multiple dies."""
        self.charity_turns_remaining = 3

    def use_charity_turn(self) -> None:
        """Use a charity turn."""
        self.charity_turns_remaining -= 1

    def start_layoff(self) -> None:
        """Start a layoff for two turns."""
        self.skipped_turns_remaining = 2

    def use_layoff(self) -> None:
        """Use a layoff day."""
        self.skipped_turns_remaining -= 1

    def make_payment(self, *, payment: int) -> None:
        """Make a payment."""
        self.savings -= payment

    @property
    def total_expenses(self) -> int:
        """Get total expenses for player."""
        loan_cost: int = 0
        for loan in self.loan_list:
            loan_cost += loan.monthly_payment
        return (
            self.taxes
            + self.expense_other
            + self.cost_per_child * self.no_children
            + loan_cost
        )

    def payoff_loan(self, *, loan_number: int) -> None:
        """Payoff a loan."""
        self.savings -= self.loan_list[loan_number].balance
        self.loan_list.pop(loan_number)

    """
    def paydown_loan(self, *, loan_number: int, payment: int) -> bool:
        if (
            payment < 1000
            or payment >= self.loan_list[loan_number].balance
            or payment % 1_000 != 0
            or payment > self.savings
        ):
            return False
        self.loan_list[loan_number].make_payment(payment=payment)
        self.savings -= payment
        return True
    """

    def buy_stock(
        self,
        *,
        stock_asset: cfs_assets.Stock,
        cost_per_share: int = 0,
    ) -> bool:
        """Buy stock."""
        if cost_per_share == 0:
            cost_per_share = stock_asset.cost_per_share
        total_cost = stock_asset.shares * stock_asset.cost_per_share
        log.info(
            f"Checking if need loan to buy stock. Shares: {stock_asset.shares}, Cost per share: {stock_asset.cost_per_share}"
            f", Total Cost: {total_cost}, Savings: {self.savings}"
        )
        if total_cost > self.savings:
            loan_amount: int = int(
                round(
                    (float(total_cost - self.savings) / 1000) + 0.4999,
                    0,
                )
                * 1000
            )
            log.info(f"Need loan of {loan_amount} to buy stock")
            if cfs_player_choice.choose_to_get_loan_to_buy_asset(
                a_player=self,
                asset=stock_asset,
                loan_amount=loan_amount,
            ):
                log.info(f"Chose to take loan to buy stock")
                self.make_loan(
                    loan=cfs_loans.Loan(
                        name="Bank Loan",
                        balance=loan_amount,
                        monthly_payment=int(loan_amount / 10),
                        partial_payment_allowed=True,
                    )
                )
            else:
                log.info(f"Chose not to take loan to buy stock")
                return False
        self.stock_assets.append(stock_asset)
        self.savings -= stock_asset.shares * cost_per_share
        return True

    def sell_stock(
        self,
        *,
        asset: cfs_assets.Stock,
        price: int,
        no_shares: int,
    ) -> None:
        """Sell some stock."""
        if asset in self.stock_assets:
            owned_shares: int = asset.shares
            if no_shares > owned_shares:
                log.info(
                    f"Requested to sell {no_shares} shares but you only have "
                    f"{owned_shares} shares. Selling all"
                )
                no_shares = owned_shares
            if no_shares < owned_shares:
                log.info(f"Partial sale of {no_shares} of {owned_shares} shares.")
                asset.reduce_no_shares(no_shares)
            else:
                log.info("Selling all {shares} shares of {asset.name}")
                self.stock_assets.remove(asset)
                self.sold_assets.append((asset, price * no_shares))
            self.savings += price * no_shares
        else:
            err_msg = f"Tried to sell stock, {asset.name} when it is not owned"
            log.error(err_msg)
            raise ValueError(err_msg)

    def buy_real_estate(self, *, real_estate_asset: cfs_assets.RealEstate) -> bool:
        """Buy real estate."""
        if real_estate_asset.down_payment > self.savings:
            loan_amount: int = int(
                round(
                    (float(real_estate_asset.down_payment - self.savings) / 1000)
                    + 0.4999,
                    0,
                )
                * 1000
            )
            log.info(
                f"Player {self.name} needs loan of {loan_amount} to buy real estate"
            )
            if cfs_player_choice.choose_to_get_loan_to_buy_asset(
                a_player=self, asset=real_estate_asset, loan_amount=loan_amount
            ):
                log.info(f"Chose to take loan ({loan_amount}) to buy real estate")
                self.make_loan(
                    loan=cfs_loans.Loan(
                        name="Bank Loan",
                        balance=loan_amount,
                        monthly_payment=int(loan_amount / 10),
                        partial_payment_allowed=True,
                    )
                )
            else:
                log.info(f"Chose not to take loan to buy real_estate_asset")
                return False
        self.real_estate_assets.append(real_estate_asset)
        self.savings -= real_estate_asset.down_payment
        log.info(f"Real estate asset {real_estate_asset.name} purchased")
        return True

    def sell_real_estate(self, *, asset: cfs_assets.RealEstate, price: int) -> None:
        """Sell real estate."""
        if asset in self.real_estate_assets:
            self.savings += price - asset.loan_amount
            self.real_estate_assets.remove(asset)
            self.sold_assets.append([asset, price])  # type: ignore
            log.info(f"Sold {asset.name}, {asset.asset_type} for {price}.")
            return
        err_msg = f"Real estate asset {asset.name} cannot be sold as it is not owned by player {self.name}."
        log.error(err_msg)
        raise ValueError(err_msg)

    def buy_business(self, *, business_asset: cfs_assets.Business) -> bool:
        """Buy a business."""
        if business_asset.down_payment > self.savings:
            loan_amount: int = int(
                round(
                    (float(business_asset.down_payment - self.savings) / 1000) + 0.4999,
                    0,
                )
                * 1000
            )
            log.info(f"Player {self.name} needs loan of {loan_amount} to buy business")
            if cfs_player_choice.choose_to_get_loan_to_buy_asset(
                a_player=self,
                asset=business_asset,
                loan_amount=loan_amount,
            ):
                log.info(f"Chose to take loan ({loan_amount}) to buy buisiness")
                self.make_loan(
                    loan=cfs_loans.Loan(
                        name="Bank Loan",
                        balance=loan_amount,
                        monthly_payment=int(loan_amount / 10),
                        partial_payment_allowed=True,
                    )
                )
            else:
                log.info(f"Chose not to take loan to buy business")
                return False
        self.business_assets.append(business_asset)
        self.savings -= business_asset.down_payment
        log.info(f"Buisiness {business_asset.name} purchased")
        return True

    def sell_business(self, *, asset: cfs_assets.Business, price: int) -> None:
        """Sell a business."""
        if asset in self.business_assets:
            self.business_assets.remove(asset)
            self.savings += price - asset.loan_amount
            self.sold_assets.append((asset, price))
            log.info(f"Sold {asset.name}, {asset.asset_type} for {price}.")
            return
        err_msg = f"Business {asset.name} cannot be sold as it is not owned by player {self.name}."
        log.error(err_msg)
        raise ValueError(err_msg)

    def have_child(self) -> None:
        """Have a child."""
        if self.no_children >= 3:
            log.info("Three kids is enough for anyone")
            return
        self.no_children += 1
        log.info(
            f"Congratulations! You had a child. You now have {self.no_children} child{'ren' if self.no_children > 1 else ''}."
        )

    def refresh(self) -> tuple[bool, bool]:
        """Recalc. tot. inc.,passive income,total expenses,am Irich,amIPoor."""
        return (
            (True, False)  # I am rich, I am not poor
            if self.passive_income > self.total_expenses
            else (False, True)  # I am not rich, I am poor
            if (self.monthly_cash_flow < 0 and (-self.monthly_cash_flow > self.savings))
            else (False, False)  # I am not rich, I am not poor
        )

    def __str__(self) -> str:
        """Create string to be returned when str method is called."""
        self.refresh()
        loan_str_list: str = "\n".join([f"{loan}" for loan in self.loan_list])

        asset_str_list1: str = "\n".join([f"{asset}" for asset in self.stock_assets])
        asset_str_list2: str = "\n".join(
            [f"{asset}" for asset in self.real_estate_assets]
        )
        asset_str_list3: str = "\n".join([f"{asset}" for asset in self.business_assets])
        asset_str_list: str = "\n".join(
            [asset_str_list1, asset_str_list2, asset_str_list3]
        )

        no_assets = (
            len(self.stock_assets)
            + len(self.real_estate_assets)
            + len(self.business_assets)
        )
        # TO DO, right justify and format numbers
        return (
            f"\nName:              {self.name}"
            f"\nProfession:        {self.profession}"
            f"\n"
            f"\nSalary:            {self.salary}"
            f"\nTaxes:             {self.taxes}"
            f"\nOther Expenses:    {self.expense_other}"
            f"\nChildren:          {self.no_children}"
            f"\nCost per Child:    {self.cost_per_child}"
            f"\nSavings:           {self.savings}"
            f"\nTotal Income:      {self.total_income}"
            f"\nPassive Income:    {self.passive_income}"
            f"\nTotal Expenses:    {self.total_expenses}"
            f"\nMonthly Cash Flow: {self.monthly_cash_flow}"
            f"\nNo. Loans:         {len(self.loan_list)}"
            f"\n{loan_str_list}"
            f"\n\nNo. Assets:        {str(no_assets)}"
            f"\n{asset_str_list}"
            f"\nStrategy:          {str(self.strategy)}"
        )

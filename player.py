"""Object and functions to manage Professions in Game Simulation."""

import loans
import assets
import player_choice


class Player(object):
    """Object to manage Player actions in Game Simulations."""

    def __init__(self, name, profession, strategy):
        """Create a Player object."""
        self.name = name
        self.profession = profession.name
        self.salary = profession.salary
        self.taxes = profession.expense_taxes
        self.expense_other = profession.expense_other
        self.cost_per_child = profession.cost_per_child
        self.savings = profession.savings
        self.loan_list = profession.loan_list.copy()
        self.strategy = strategy
        self.no_children = 0
        self.stock_assets = []
        self.real_estate_assets = []
        self.business_assets = []
        self.sold_assets = []   # list of sold assets: [asset, sale price)
        self.charity_turns_remaining = 0
        self.skipped_turns_remaining = 0
        self.am_i_rich = False
        self.am_i_broke = False

    def earn_salary(self):
        """Earn a salary."""
        self.refresh()
        self.savings = int(self.savings + self.monthly_cash_flow)
        return

    @property
    def passive_income(self):
        """Return the passive income calculated for the player."""
        self.passive_income_temp = 0
        for stock in self.stock_assets:
            self.passive_income_temp += stock.dividend_interest
        for real_estate in self.real_estate_assets:
            self.passive_income_temp += real_estate.cash_flow
        for business in self.business_assets:
            self.passive_income_temp += business.cash_flow
        return self.passive_income_temp

    @property
    def monthly_cash_flow(self):
        """Return monthly cash flow."""
        return self.total_income - self.total_expenses

    @property
    def total_income(self):
        """Return total monthly income."""
        return self.salary + self.passive_income

    def make_loan(self, loan):
        """Make a new loan if you can."""
        self.loan_list.append(loan)
        self.savings += loan.balance

    def start_charity_turns(self):
        """Start charity turns where you can roll multiple dies."""
        self.charity_turns_remaining = 3

    def use_charity_turn(self):
        """Use a charity turn."""
        self.charity_turns_remaining -= 1

    def start_layoff(self):
        """Start a layoff for two turns."""
        self.skipped_turns_remaining = 2

    def use_layoff(self):
        """Use a layoff day."""
        self.skipped_turns_remaining -= 1

    def make_payment(self, payment):
        """Make a payment."""
        self.savings -= payment

    @property
    def total_expenses(self):
        """Get total expenses for player."""
        loan_cost = 0
        for loan in self.loan_list:
            loan_cost += loan.monthly_payment
        return (self.taxes +
                self.expense_other +
                self.cost_per_child * self.no_children +
                loan_cost)

    def payoff_loan(self, loan_number):
        """Payoff a loan."""
        if self.savings >= self.loan_list[loan_number].balance:
            self.savings -= self.loan_list[loan_number].balance
            self.loan_list.pop(loan_number)
            return True
        else:
            return False

    def buy_stock(self, stock_asset, cost_per_share=0, verbose=True):
        """Buy stock."""
        if cost_per_share == 0:
            cost_per_share = stock_asset.cost_per_share
        if ((stock_asset.no_shares * stock_asset.cost_per_share) >
                self.savings):
            loan_amount = int(round((float(cost_per_share *
                                           stock_asset.no_shares -
                                           self.savings)/1000) + 0.4999, 0) *
                              1000)
            if assets.choose_to_get_loan_to_buy_asset(
                    self, stock_asset, loan_amount, verbose):
                self.make_loan(loans.Loan("Bank Loan", loan_amount,
                                          int(loan_amount / 10), True))
            else:
                return False
        self.stock_assets.append(stock_asset)
        self.savings -= stock_asset.no_shares * cost_per_share
        return True

    def sell_stock(self, asset, price, no_shares, verbose=True):
        """Sell some stock."""
        if asset in self.stock_assets:
            owned_shares = asset.no_shares
            if no_shares > owned_shares:
                if verbose:
                    print("Requested to sell " + no_shares +
                          " but you only have " + owned_shares +
                          ".\nSelling all")
                no_shares = owned_shares
            if no_shares < owned_shares:
                if verbose:
                    print("Partial sale of " + no_shares + " of " +
                          owned_shares + ".")
                asset.reduce_no_shares(no_shares)
            else:
                if verbose:
                    print("Selling all " + no_shares + " of " + asset.name)
                self.stock_assets.remove(asset)
                self.sold_assets.append([asset, price*no_shares])
            self.savings += price * no_shares

    def buy_real_estate(self, real_estate_asset, verbose=True):
        """Buy real estate."""
        if real_estate_asset.down_payment > self.savings:
            loan_amount = int(round((float(real_estate_asset.down_payment -
                                           self.savings) / 1000) + 0.4999, 0) *
                              1000)
            if player_choice.choose_to_get_loan_to_buy_asset(
                    self, real_estate_asset, loan_amount, verbose):
                self.make_loan(loans.Loan("Bank Loan", loan_amount,
                                          int(loan_amount / 10), True))
            else:
                return False
        self.real_estate_assets.append(real_estate_asset)
        self.savings -= real_estate_asset.down_payment
        return True

    def sell_real_estate(self, asset, price, verbose):
        """Sell real estate."""
        if asset in self.real_estate_assets:
            self.savings += (price - asset.loan_amount)
            self.real_estate_assets.remove(asset)
            self.sold_assets.append([asset, price])
            if verbose:
                print("Sold " + asset.name + ", " + asset.asset_type +
                      " for " + str(price) + ".")

    def buy_business(self, business_asset, verbose=True):
        """Buy a business."""
        if business_asset.down_payment > self.savings:
            loan_amount = int(round((float(business_asset.down_payment -
                                           self.savings) / 1000) + 0.4999,
                                    0) * 1000)
            if player_choice.choose_to_get_loan_to_buy_asset(
                    self, business_asset, loan_amount, verbose):
                self.make_loan(loans.Loan("Bank Loan", loan_amount,
                                          int(loan_amount / 10), True))
            else:
                return False
        self.business_assets.append(business_asset)
        self.savings -= business_asset.down_payment
        return True

    def sell_business(self, asset, price, verbose=True):
        """Sell a business."""
        if asset in self.business_assets:
            self.business_assets.remove(asset)
            self.savings += (price - asset.loan_amount)
            self.sold_assets.append([asset, price])
            if verbose:
                print("Sold " + asset.name + ", " + asset.asset_type +
                      " for " + price + ".")

    def have_child(self, verbose=False):
        """Have a child."""
        if self.no_children >= 3:
            if verbose:
                print("Three kids is enough for anyone")
            # return self.no_children
        self.no_children += 1
        # return self.no_children

    def refresh(self):
        """Recalc. tot. inc.,passive income,total expenses,am Irich,amIPoor."""
        if self.monthly_cash_flow < 0 and (-self.monthly_cash_flow >
                                           self.savings):  # You're broke!
            return False, True  # am_i_rich, am_i_broke
        elif self.passive_income > self.total_expenses:  # You're rich!
            return True, False  # am_i_rich, am_i_broke
        else:
            return False, False  # am_i_rich, am_i_broke

    def __str__(self):
        """Create string to be returned when str method is called."""
        self.refresh()
        loan_str_list = ""
        for loan in self.loan_list:
            loan_str_list = loan_str_list + str(loan) + "\n"
        loan_str_list = loan_str_list[:-1]
        asset_str_list = ""
        for asset in self.stock_assets:
            asset_str_list = asset_str_list + str(asset) + "\n"
        for asset in self.real_estate_assets:
            asset_str_list = asset_str_list + str(asset) + "\n"
        for asset in self.business_assets:
            asset_str_list = asset_str_list + str(asset) + "\n"
        asset_str_list = asset_str_list[:-1]
        # TO DO, right justify and format numbers
        return ("\nName:              " + self.name +
                "\nProfession:        " + self.profession +
                "\nSalary:            " + str(self.salary) +
                "\nTaxes:             " + str(self.taxes) +
                "\nOther Expenses:    " + str(self.expense_other) +
                "\nChildren:          " + str(self.no_children) +
                "\nCost per Child:    " + str(self.cost_per_child) +
                "\nSavings:           " + str(self.savings) +
                "\nTotal Income:      " + str(self.total_income) +
                "\nPassive Income:    " + str(self.passive_income) +
                "\nTotal Expenses:    " + str(self.total_expenses) +
                "\nMonthly Cash Flow: " + str(self.monthly_cash_flow) +
                "\n\nNo. Loans:         " + str(len(self.loan_list)) +
                "                   \n" + loan_str_list +
                "\n\nNo. Assets:        " + str(len(self.stock_assets) +
                                                len(self.real_estate_assets) +
                                                len(self.business_assets)) +
                asset_str_list +
                "\nStrategy:          " + str(self.strategy))


if __name__ == '__main__':
    import unittest
    unittest.main(module='player_test', verbosity=2)

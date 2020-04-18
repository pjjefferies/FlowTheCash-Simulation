"""Object and functions to manage Professions in Game Simulation."""

import loans
import assets
import player_choice
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
        self.big_deal_small_deal_threshold = int(big_deal_small_deal_threshold)
        if loan_payback in ["Smallest", "Largest", "Never", "Higest Interest"]:
            self.loan_payback = loan_payback
        else:
            self.loan_payback = "Highest Interest"

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

    def earnSalary(self):
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
        self.refresh()
        return self.monthly_cash_flow

    def make_loan(self, loan):
        """Make a new loan if you can."""
        self.loan_list.append(loan)
        self.savings += loan.balance

    def start_charity_turns(self):
        """Start charity turns where you can roll multiple dies."""
        self.charity_turns_remaining = 3
        return

    def use_charity_turn(self):
        """Use a charity turn."""
        self.charity_turns_remaining -= 1

    def start_layoff(self):
        """Start a layoff for two turns."""
        self.skipped_turns_remaining = 2
        return

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
        self.total_expenses = (self.expense_taxes +
                               self.expense_other +
                               self.cost_per_child * self.no_children +
                               loan_cost)
        return self.total_expenses

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
            loan_amount = int(round((float(real_estate_asset.down_payment() -
                                           self.savings) / 1000) + 0.4999, 0) *
                              1000)
            if player_choice.choose_to_get_loan_to_buy_asset(
                    self, real_estate_asset, loan_amount, verbose):
                self.make_loan(loans.Loan("Bank Loan", loan_amount,
                                          int(loan_amount / 10), True))
            else:
                return False
        self.real_estate_assets.append(real_estate_asset)
        self.savings -= real_estate_asset.down_payment()
        return True

    def sell_real_estate(self, asset, price, verbose):
        """Sell real estate."""
        if asset in self.real_estate_assets:
            self.savings += (price - asset.loan_amount)
            self.real_estate_assets.remove(asset)
            self.sold_assets.append([asset, price])
            if verbose:
                print("Sold " + asset.name + ", " + asset.type +
                      " for " + str(price) + ".")

    def buy_business(self, business_asset, verbose=True):
        """Buy a business."""
        if business_asset.down_payment() > self.savings:
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
        self.savings -= business_asset.down_payment()
        return True

    def sell_business(self, asset, price, verbose=True):
        """Sell a business."""
        if asset in self.business_assets:
            self.business_assets.remove(asset)
            self.savings += (price - asset.loan_amount)
            self.sold_assets.append([asset, price])
            if verbose:
                print("Sold " + asset.name + ", " + asset.type + " for " +
                      price + ".")

    def have_child(self, verbose=False):
        """Have a child."""
        if self.no_children >= 3:
            if verbose:
                print("Three kids is enough for anyone")
            return self.no_children
        self.no_children += 1
        return self.no_children

    def refresh(self):
        """Recalc. tot. inc.,passive income,total expenses,am Irich,amIPoor."""
        self.passive_income
        self.total_expenses = self.total_expenses
        self.total_income = self.salary + self.passive_income
        self.monthly_cash_flow = self.total_income - self.total_expenses
        if self.monthly_cash_flow < 0 and (-1 * self.monthly_cash_flow >
                                           self.savings):  # You're broke!
            self.am_i_broke = True
            self.am_i_rich = False
        elif self.passive_income > self.total_expenses:  # You're rich!
            self.am_i_broke = False
            self.am_i_rich = True
        else:
            self.am_i_broke = False
            self.am_i_rich = False
        return self.am_i_rich, self.am_i_broke

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
                "\nTaxes:             " + str(self.expense_taxes) +
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


def get_profession_defs(profession_defs_fn):
    """Load Professions."""
    try:
        profession_defs_temp = jsonReadWriteFile.load_json(
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


def get_strategy_defs(strategy_defs_fn, verbose=False):
    """Load Strategies."""
    try:
        strategy_defs_temp = jsonReadWriteFile.load_json(strategy_defs_fn)
    except OSError:
        print("No good Strategies dict json file found, file not found, " +
              "please fix")
        raise OSError
    except ValueError:
        print("No good Strategies dict json file found, ValueError, " +
              "please fix")
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
            if strategy_defs_temp[strategy].get("takeDownpaymentLoans", "True"):
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
                int(strategy_defs_temp[strategy].get("bigDealSmallDealThreshold",
                                                     5000)),
                str(strategy_defs_temp[strategy].get("loanPayback",
                                                     "Highest Interest")))
    return strategy_defs


if __name__ == '__main__':  # test Player Object
    PROFESSION_DEFS = get_profession_defs("ProfessionsList.json")
    LIST_OF_PLAYERS = []
    # Make Available Strategies to Test
    STRATEGY_DEFS = get_strategy_defs("Strategies.json")

    """
    manualStrategy = Strategy(name="Manual", manual = True)
    standardAutoStrategy = Strategy(name="Standard Auto", manual=False)
    daveRamseyAutoStrategy = Strategy(name="Dave Ramsey",
                                      manual = True,
                                      roiThreshold = 0.20,
                                      priceRatioThreshold = 0.5,
                                      takeDownpaymentLoans = False,
                                      takeAnyLoans = False)
    noDownPaymentLoanAutoStrategy = Strategy(
        name="No Down Payment Loans",
        manual = True,
        roiThreshold = 0.20,
        priceRatioThreshold = 0.5,
        takeDownpaymentLoans = False,
        takeAnyLoans = True)
    """

    for PROFESSION in PROFESSION_DEFS:  # create player example for each prof.
        name = PROFESSION + " Player"
        LIST_OF_PLAYERS.append(Player(name, PROFESSION_DEFS[PROFESSION],
                                      STRATEGY_DEFS["Standard Auto"]))
    print(len(LIST_OF_PLAYERS), "players created")
    for A_PLAYER in LIST_OF_PLAYERS:
        print(A_PLAYER)
    print("End")

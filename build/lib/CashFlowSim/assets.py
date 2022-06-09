"""Module containing Asset Object."""


class Asset(object):
    """Create Object to represent Assets."""

    def __init__(self, name, asset_type, cost, down_payment,
                 cash_flow, price_range_low, price_range_high):
        """Create Asset Object."""
        self.name = name
        self.asset_type = asset_type
        self.cost = cost
        self.down_payment = down_payment
        self.cash_flow = cash_flow
        self.price_range_low = price_range_low
        self.price_range_high = price_range_high

    @property
    def roi(self):
        """Return return on investment (aka ROI)."""
        if self.down_payment > 0:
            return float(self.cash_flow)*12.0/float(self.down_payment)
        else:
            return 1.0

    @property
    def loan_amount(self):
        """Return loan amount for asset."""
        return self.cost - self.down_payment

    def __str__(self):
        """Create string to be returned when str method is called."""
        return ("\n  Type:         " + self.asset_type +
                "\n   Name:        " + self.name +
                "\n   Cost:        " + str(self.cost) +
                "\n   Down Payment:" + str(self.down_payment) +
                "\n   Cash Flow:   " + str(self.cash_flow) +
                "\n   Price Range: " + str(self.price_range_low) + " - " +
                str(self.price_range_high) +
                "\n   ROI:         " + str(self.roi))


class Stock(Asset):
    """Create Stock Asset Object."""

    def __init__(self, name, shares, cost_per_share, dividend_interest,
                 price_range_low, price_range_high):
        """Create Stock Asset Object."""
        Asset.__init__(self, name, "Stock", 0, 0, 0,
                       price_range_low, price_range_high)
        self.shares = shares
        self.cost_per_share = cost_per_share
        self.dividend_interest = dividend_interest

    @property
    def total_cost(self):
        """Calculate the total cost of a stock."""
        return self.shares * self.cost_per_share

    def stock_split(self, ratio):
        """Increase number of shares in a stock split."""
        self.shares *= ratio

    def reduce_no_shares(self, shares_to_reduce):
        """Reduce the number of shares as specified."""
        if shares_to_reduce < self.shares:
            self.shares -= shares_to_reduce
        return self.shares

    @property
    def roi(self):
        """Return the return on investment."""
        if self.dividend_interest == 0:
            return 0.0
        elif self.cost_per_share > 0:
            return (float(self.dividend_interest) * 12.0 /
                    float(self.cost_per_share))
        else:
            return 1.0

    def __str__(self):
        """Create string to be returned when str method is called."""
        return ("\n  Type:              " + "Stock" +
                "\n   Symbol:           " + self.name +
                "\n   Shares:           " + str(self.shares) +
                "\n   Cost per Share:   " + str(self.cost_per_share) +
                "\n   Total Cost:       " + str(
                    self.shares * self.cost_per_share) +
                "\n   Dividends/share:  " + str(self.dividend_interest) +
                "\n   Price Range: " + str(self.price_range_low) + " - " +
                str(self.price_range_high) +
                "\n   ROI:              " + str(self.roi))


class RealEstate(Asset):
    """Create Real Estate Asset."""

    def __init__(self, name, real_estate_type, house_or_condo, cost,
                 down_payment, cash_flow=0, price_range_low=0,
                 price_range_high=0, units=0, acres=0):
        """Create Real Estate Asset."""
        Asset.__init__(self, name, real_estate_type, cost, down_payment,
                       cash_flow, price_range_low, price_range_high)
        self.house_or_condo = house_or_condo
        self.units = units
        self.acres = acres

    def __str__(self):
        """Create string to be returned when str method is called."""
        return ("\n  Type:        " + self.asset_type +
                "\n   Name:        " + self.name +
                "\n   house_or_condo " + str(self.house_or_condo) +
                "\n   Cost:        " + str(self.cost) +
                "\n   Down Payment:" + str(self.down_payment) +
                "\n   Cash Flow:   " + str(self.cash_flow) +
                "\n   Units:       " + str(self.units) +
                "\n   Acres:       " + str(self.acres) +
                "\n   Price Range: " + str(self.price_range_low) + " - " +
                str(self.price_range_high) +
                "\n   ROI:         " + str(self.roi))


class Business(Asset):
    """Create Business Asset."""

    def __init__(self, name, card_type, cost, down_payment, cash_flow=0,
                 price_range_low=0, price_range_high=0):
        """Create Business Asset."""
        Asset.__init__(self, name, card_type, cost, down_payment,
                       cash_flow, price_range_low, price_range_high)

    def increase_cash_flow(self, increase_amount):
        """Increase Cash Flow by increaseAmount."""
        self.cash_flow += increase_amount
        return self.cash_flow


if __name__ == '__main__':
    import unittest
    unittest.main(module='assets_test', verbosity=2)

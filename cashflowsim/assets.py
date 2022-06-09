"""Module containing Asset Object."""

from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Asset:
    """Create Object to represent Assets."""

    name: str
    asset_type: str
    cost: int
    down_payment: int
    cash_flow: int
    price_range_low: int
    price_range_high: int
    # roi: float = field(init=False)
    # loan_amount: float = field(init=False)

    @property
    def roi(self):
        """Return return on investment (aka ROI)."""
        if self.down_payment > 0:
            return float(self.cash_flow) * 12.0 / float(self.down_payment)
        else:
            return 1.0

    @property
    def loan_amount(self) -> float:
        """Return loan amount for asset."""
        return self.cost - self.down_payment

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"\nType:            {self.asset_type}"
            f"\n   Name:         {self.name}"
            f"\n   Cost:         {str(self.cost)}"
            f"\n   Type:         {self.asset_type}"
            f"\n   Down Payment: {str(self.down_payment)}"
            f"\n   Cash Flow:    {str(self.cash_flow)}"
            f"\n   Price Range:  {str(self.price_range_low)} - "
            f"{str(self.price_range_high)}"
            f"\n   ROI:          {str(self.roi)}"
        )


@dataclass(slots=True, kw_only=True)
class Stock(Asset):
    """Create Stock Asset Object."""

    name: str
    shares: int
    cost_per_share: int
    dividend_interest: int
    price_range_low: int
    price_range_high: int

    # Asset.__init__(self, name, "Stock", 0, 0, 0, price_range_low, price_range_high)

    @property
    def total_cost(self) -> int:
        """Calculate the total cost of a stock."""
        return self.shares * self.cost_per_share

    def stock_split(self, ratio: float) -> None:
        """Increase number of shares in a stock split."""
        self.shares = int(self.shares * ratio)

    def reduce_no_shares(self, shares_to_reduce: int) -> int:
        """Reduce the number of shares as specified."""
        if shares_to_reduce < self.shares:
            self.shares -= shares_to_reduce
        return self.shares

    @property
    def roi(self) -> float:
        """Return the return on investment."""
        if self.dividend_interest == 0:
            return 0.0
        elif self.cost_per_share > 0:
            return float(self.dividend_interest) * 12.0 / float(self.cost_per_share)
        else:
            return 1.0

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"\nType:                Stock"
            f"\n   Symbol:           {self.name}"
            f"\n   Shares:           {str(self.shares)}"
            f"\n   Cost per Share:   {str(self.cost_per_share)}"
            f"\n   Total Cost:       {str(self.shares * self.cost_per_share)}"
            f"\n   Dividends/share:  {str(self.dividend_interest)}"
            f"\n   Price Range:      {str(self.price_range_low)} - "
            f"{str(self.price_range_high)}"
            f"\n   ROI:              {str(self.roi)}"
        )


@dataclass(slots=True, kw_only=True)
class RealEstate(Asset):
    """Create Real Estate Asset."""

    name: str
    real_estate_type: str
    house_or_condo: str
    cost: int
    down_payment: int
    cash_flow: int = 0
    price_range_low: int = 0
    price_range_high: int = 0
    units: int = 0
    acres: int = 0

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"\n Type:             {self.asset_type}"
            f"\n   Name:           {self.name}"
            f"\n   house_or_condo: {str(self.house_or_condo)}"
            f"\n   Cost:           {str(self.cost)}"
            f"\n   Down Payment:   {str(self.down_payment)}"
            f"\n   Cash Flow:      {str(self.cash_flow)}"
            f"\n   Units:          {str(self.units)}"
            f"\n   Acres:          {str(self.acres)}"
            f"\n   Price Range:    {str(self.price_range_low)} - "
            f"{str(self.price_range_high)}"
            f"\n   ROI:            {str(self.roi)}"
        )


@dataclass(slots=True, kw_only=True)
class Business(Asset):
    """Create Business Asset."""

    name: str
    card_type: str
    cost: int
    down_payment: int
    cash_flow: int = 0
    price_range_low: int = 0
    price_range_high: int = 0

    def increase_cash_flow(self, increase_amount: int) -> int:
        """Increase Cash Flow by increaseAmount."""
        self.cash_flow += increase_amount
        return self.cash_flow

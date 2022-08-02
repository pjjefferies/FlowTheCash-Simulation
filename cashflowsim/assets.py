"""Module containing Asset Object."""

from __future__ import annotations
from dataclasses import dataclass
import logging

log = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Asset:
    """Create Object to represent Assets."""

    name: str
    asset_type: str
    cost: int = 0
    down_payment: int = 0
    cash_flow: int = 0
    price_range_low: int = 0
    price_range_high: int = 1_000_000

    @property
    def roi(self):
        """Return return on investment (aka ROI)."""
        if self.down_payment > 0:
            roi_result = float(self.cash_flow) * 12.0 / float(self.down_payment)
            log.info(f"ROI: {roi_result}")
            return roi_result
        else:
            return 1.0

    @property
    def loan_amount(self) -> int:
        """Return loan amount for asset."""
        return self.cost - self.down_payment

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"Type:            {self.asset_type}"
            f"\n   Name:         {self.name}"
            f"\n   Cost:         {self.cost}"
            f"\n   Type:         {self.asset_type}"
            f"\n   Down Payment: {self.down_payment}"
            f"\n   Cash Flow:    {self.cash_flow}"
            f"\n   Price Range:  {self.price_range_low} - {self.price_range_high}"
            f"\n   ROI:          {self.roi}"
        )


def roi(asset: Asset | RealEstate | Business) -> float:
    """Return return on investment (aka ROI)."""
    if asset.down_payment > 0:
        roi_result = float(asset.cash_flow) * 12.0 / float(asset.down_payment)
        log.info(f"ROI: {roi_result}")
        return roi_result
    else:
        return 1.0


@dataclass(kw_only=True)
class Stock(Asset):
    """Create Stock Asset Object."""

    cost_per_share: int = 0
    dividend_interest: int = 0
    shares: int = 0

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
            f"Type:                Stock"
            f"\n   Symbol:           {self.name}"
            f"\n   Shares:           {self.shares}"
            f"\n   Cost per Share:   {self.cost_per_share}"
            f"\n   Total Cost:       {self.shares * self.cost_per_share}"
            f"\n   Dividends/share:  {self.dividend_interest}"
            f"\n   Price Range:      {self.price_range_low} - {self.price_range_high}"
            f"\n   ROI:              {self.roi}"
        )


@dataclass(kw_only=True)
class RealEstate(Asset):
    """Create Real Estate Asset."""

    # real_estate_type: str
    house_or_condo: str
    units: int = 0
    acres: int = 0

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f" Type:             {self.asset_type}"
            f"\n   Name:           {self.name}"
            f"\n   house_or_condo: {self.house_or_condo}"
            f"\n   Cost:           {self.cost}"
            f"\n   Down Payment:   {self.down_payment}"
            f"\n   Cash Flow:      {self.cash_flow}"
            f"\n   Units:          {self.units}"
            f"\n   Acres:          {self.acres}"
            f"\n   Price Range:    {self.price_range_low} - {self.price_range_high}"
            f"\n   ROI:            {roi(self)}"
        )


@dataclass(kw_only=True)
class Business(Asset):
    """Create Business Asset."""

    def increase_cash_flow(self, *, increase_amount: int) -> int:
        """Increase Cash Flow by increaseAmount."""
        self.cash_flow += increase_amount
        return self.cash_flow

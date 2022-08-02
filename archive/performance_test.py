from sys import dont_write_bytecode
import timeit

from cv2 import DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS


def function1():
    asset_type = "An Asset"
    name = "A Name"
    house_or_condo = "House"
    cost = 50000
    down_payment = 10000
    cash_flow = 5000
    units = 4
    acres = 42
    price_range_low = 40000
    price_range_high = 60000
    roi = 0.20

    return f"\n".join(
        [
            f" Type:             {asset_type}",
            f"   Name:           {name}",
            f"   house_or_condo: {house_or_condo}",
            f"   Cost:           {cost}",
            f"   Down Payment:   {down_payment}",
            f"   Cash Flow:      {cash_flow}",
            f"   Units:          {units}",
            f"   Acres:          {acres}",
            f"   Price Range:    {price_range_low} - {price_range_high}",
            f"   ROI:            {roi}",
        ]
    )


def function2():
    asset_type = "An Asset"
    name = "A Name"
    house_or_condo = "House"
    cost = 50000
    down_payment = 10000
    cash_flow = 5000
    units = 4
    acres = 42
    price_range_low = 40000
    price_range_high = 60000
    roi = 0.20

    return (
        f"\n Type:             {asset_type}"
        f"\n   Name:           {name}"
        f"\n   house_or_condo: {house_or_condo}"
        f"\n   Cost:           {cost}"
        f"\n   Down Payment:   {down_payment}"
        f"\n   Cash Flow:      {cash_flow}"
        f"\n   Units:          {units}"
        f"\n   Acres:          {acres}"
        f"\n   Price Range:    {price_range_low} - {price_range_high}"
        f"\n   ROI:            {roi}"
    )


print("function1: ", timeit.Timer(function1).timeit(10000))

print("function2: ", timeit.Timer(function2).timeit(10000))

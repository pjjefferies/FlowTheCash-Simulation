"""Manage cards for Game simulation."""
import json_read_write_file


class Card(object):
    """Create card object."""

    def __init__(self, title, card_type):
        """Create card object."""
        self.title = title
        self.card_type = card_type


class DoodadCard(Card):
    """Object to manage Doodad Cards."""

    def __init__(self, title, card_type, one_time_payment=0,
                 any_child_payment=0, each_child_payment=0,
                 loan_title='', loan_amount=0, loan_payment=0):
        """Create Doodad Card Object."""
        assert ((card_type == "OneTimeExpense" and one_time_payment > 0) or
                (card_type == "ChildCost" and ((any_child_payment > 0) or
                                               (each_child_payment > 0))) or
                (card_type == "NewLoan" and loan_title != "" and
                 loan_amount > 0 and loan_payment > 0))
        Card.__init__(self, title, card_type)
        if self.card_type == "OneTimeExpense":
            self.one_time_payment = one_time_payment
        elif self.card_type == "ChildCost":
            self.any_child_payment = any_child_payment
            self.each_child_payment = each_child_payment
        elif self.card_type == "NewLoan":
            self.loan_title = loan_title
            self.loan_amount = loan_amount
            self.loan_payment = loan_payment
            self.one_time_payment = one_time_payment
        else:
            print("Card Type: ", self.card_type, "no found in Card creation")

    def __str__(self):
        """Create string to be returned when str method is called."""
        if self.card_type == "OneTimeExpense":
            return ("\nTitle:           " + self.title +
                    "\nType:            " + self.card_type +
                    "\nOne Time Payment:" + str(self.one_time_payment))
        elif self.card_type == "ChildCost":
            return ("\nTitle:           " + self.title +
                    "\nType:            " + self.card_type +
                    "\nAny Child Cost:  " + str(self.any_child_payment) +
                    "\nEach Child Cost: " + str(self.each_child_payment))
        elif self.card_type == "NewLoan":
            return ("\nTitle:           " + self.title +
                    "\nType:            " + self.card_type +
                    "\nLoan Title  :    " + self.loan_title +
                    "\nLoan Amount :    " + str(self.loan_amount) +
                    "\nLoan Payment:    " + str(self.loan_payment))
        else:
            print("Card Type: ", self.card_type,
                  " not found in string conversion")


class MarketCard(Card):
    """Object to represent Market Card in Game Simulation."""

    def __init__(self, title_card_type, price=0, increased_cash_flow=0,
                 must_sell=False, self_only=False):
        """Create Market Card object."""
        assert ((title_card_type == "Small Business Improves" and
                 increased_cash_flow > 0) or
                (title_card_type == "Condo Buyer - 2Br/1Ba" and price > 0) or
                (title_card_type == "Shopping Mall Wanted" and price > 0) or
                (title_card_type == "Buyer for 20 Acres" and price > 0) or
                (title_card_type == "Price of Gold Soars" and price > 0) or
                (title_card_type == "Car Wash Buyer" and price > 0) or
                (title_card_type == "Software Company Buyer" and price > 0) or
                (title_card_type == "Apartment House Buyer" and price > 0) or
                (title_card_type == "House Buyer - 3Br/2Ba" and price > 0) or
                (title_card_type == "Plex Buyer" and price > 0) or
                (title_card_type == "Limited Partnership Sold" and
                 price > 0) or
                (title_card_type == "Interest Rates Drop!" and price > 0) or
                (title_card_type == "Inflation Hits!"))
        Card.__init__(self, title_card_type, title_card_type)

        self.must_sell = True if must_sell == "True" else False

        self.self_only = True if self_only == "True" else False

        if self.title == "Small Business Improves":
            self.increased_cash_flow = increased_cash_flow
        elif self.title in ["Condo Buyer - 2Br/1Ba", "Shopping Mall Wanted",
                            "Buyer for 20 Acres", "Price of Gold Soars",
                            "Car Wash Buyer", "Software Company Buyer",
                            "Apartment House Buyer", "House Buyer - 3Br/2Ba",
                            "Plex Buyer"]:
            self.price = price
        elif self.title == "Limited Partnership Sold":
            self.price = price
        elif self.title == "Interest Rates Drop!":
            self.added_price = price
        elif self.title == "Inflation Hits!":
            pass
        else:
            print("Unknown Market Card Type:", self.title, "in card creation")

    def __str__(self):
        """Create string to be returned when str method is called."""
        if self.card_type == "Small Business Improves":
            return ("\nTitle:                   " + self.title +
                    "\nIncreased Cash Flow:     " +
                    str(self.increased_cash_flow) +
                    "\nMust Sell:               " + str(self.must_sell))
        elif self.card_type in ["Condo Buyer - 2Br/1Ba",
                                "Shopping Mall Wanted",
                                "Buyer for 20 Acres", "Price of Gold Soars",
                                "Car Wash Buyer", "Software Company Buyer",
                                "Apartment House Buyer",
                                "House Buyer - 3Br/2Ba", "Plex Buyer"]:
            return ("\nTitle:     " + self.title +
                    "\nPrice:     " + str(self.price) +
                    "\nMust Sell: " + str(self.must_sell))
        elif self.card_type == "Limited Partnership Sold":
            return ("\nTitle:          " + self.title +
                    "\nPrice Multiple: " + str(self.price) +
                    "\nMust Sell:      " + str(self.must_sell))
        elif self.card_type == "Interest Rates Drop!":
            return ("\nTitle:       " + self.title +
                    "\nAdded Price: " + str(self.added_price) +
                    "\nMust Sell:   " + str(self.must_sell) +
                    "\nSelf Only:   " + str(self.self_only))
        elif self.card_type == "Inflation Hits!":
            return ("\nTitle:          " + self.title +
                    "\nMust Sell:      " + str(self.must_sell))
        else:
            print("Card Type: ", self.card_type,
                  " not found in card string conversion")


class DealCard(Card):
    """Object to represent Deal Cards in Game Simulations."""

    def __init__(self, title, card_type, house_or_condo, price, down_payment,
                 cash_flow, price_range_low, price_range_high,
                 all_may_buy=False):
        """Create Deal Card Object."""
        assert (card_type != "HouseForSale" or price > 0)
        Card.__init__(self, title, card_type)
        self.house_or_condo = house_or_condo
        self.all_may_buy = all_may_buy
        self.price_range_low = price_range_low
        self.price_range_high = price_range_high
        self.price = price
        self.down_payment = down_payment
        self.cash_flow = cash_flow


class SmallDealCard(DealCard):
    """Object to manage Small Deal Cards in Game Simulation."""

    def __init__(self, title, card_type, house_or_condo, symbol, price,
                 down_payment, cash_flow, split_ratio, price_range_low,
                 price_range_high, all_may_buy=False):
        """Create Small Deal Card to be added to Small Deal Deck."""
        available_stocks = ['OK4U', 'ON2U', 'GRO4US', '2BIG', 'MYT4U', 'CD']
        assert ((card_type == "Stock" and symbol in available_stocks and
                 price > 0) or
                (card_type == "StockSplit" and symbol in available_stocks and
                 split_ratio > 0) or
                (card_type == "HouseForSale" and price > 0) or
                (card_type == "Asset" and price > 0) or
                (card_type == "Land" and price > 0) or
                (card_type == "LoanNotToBeRepaid" and price > 0) or
                (card_type == "CostIfRentalProperty" and price > 0) or
                (card_type == "StartCompany" and price > 0))
        DealCard.__init__(self, title, card_type, house_or_condo, price,
                          down_payment, cash_flow, price_range_low,
                          price_range_high, all_may_buy)
        if self.card_type == "Stock":
            self.symbol = symbol
            self.price = price
            self.dividend = cash_flow
        elif self.card_type == "StockSplit":
            self.symbol = symbol
            self.split_ratio = split_ratio
        elif self.card_type == "StockSplit":
            self.symbol = symbol
            self.split_ratio = split_ratio
        elif self.card_type == "Asset":
            self.price = price
            self.down_payment = price
            self.cash_flow = cash_flow
            self.price_range_low = price_range_low
            self.price_range_high = price_range_high
        elif self.card_type == "Land":
            self.price = price
            self.down_payment = down_payment
            self.acres = cash_flow
            self.house_or_condo = "None"
        elif self.card_type in ["LoanNotToBeRepaid", "CostIfRentalProperty"]:
            self.price = price
        elif self.card_type == "StartCompany":
            self.price = price
            self.down_payment = down_payment
            self.cash_flow = cash_flow

    def __str__(self):
        """Create string to be returned when str method is called."""
        if self.card_type == "Stock":
            return ("\nSmall Deal Card:" +
                    "\nTitle:       " + self.title +
                    "\nType:        " + self.card_type +
                    "\nSymbol:      " + self.symbol +
                    "\nPrice:       " + str(self.price) +
                    "\nDividends:   " + str(self.dividend) +
                    "\nPrice Range: " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "StockSplit":
            return ("\nSmall Deal Card:" +
                    "\nTitle: " + self.title +
                    "\nType: " + self.card_type +
                    "\nSymbol: " + self.symbol +
                    "\nSplit Ratio: " + str(self.split_ratio))
        elif self.card_type == "HouseForSale":
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.card_type +
                    "\nHouse or Condo: " + self.house_or_condo +
                    "\nPrice:          " + str(self.price) +
                    "\nDown Payment:   " + str(self.down_payment) +
                    "\nCash Flow:      " + str(self.cash_flow) +
                    "\nPrice Range:    " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "Asset":
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.card_type +
                    "\nPrice:          " + str(self.price) +
                    "\nCash Flow:      " + str(self.cash_flow) +
                    "\nPrice Range:    " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "Land":
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.card_type +
                    "\nAcres:          " + str(self.acres))
        elif self.card_type in ["LoanNotToBeRepaid", "CostIfRentalProperty"]:
            return ("\nSmall Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.card_type +
                    "\nCost:           " + str(self.price))
        elif self.card_type == "StartCompany":
            return ("\nSmall Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.card_type +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.down_payment) +
                    "\nCash Flow:    " + str(self.cash_flow))
        else:
            print("Small Deal Card Type: ", self.card_type, " not found")


class BigDealCard(DealCard):
    """Object to manage Big Deal Cards in Game Simulation."""

    def __init__(self, title, card_type, price, down_payment, cash_flow, units,
                 acres, price_range_low, price_range_high,
                 cost_if_have_real_estate, cost_if_have8_plex):
        assert ((card_type in ["ApartmentHouseForSale", "XPlex"] and
                 units > 0 and price > 0) or
                (card_type in ["HouseForSale", "Business"] and price > 0) or
                (card_type == "Land" and acres > 0 and price > 0) or
                (card_type == "Expense" and (cost_if_have_real_estate > 0 or
                                             cost_if_have8_plex > 0)))
        DealCard.__init__(self, title, card_type, "None", price, down_payment,
                          cash_flow, price_range_low, price_range_high, False)
        self.acres = acres
        self.units = units
        if self.card_type in ["ApartmentHouseForSale", "XPlex"]:
            self.house_or_condo = "None"
        elif self.card_type == "Expense":
            self.cost_if_have_real_estate = cost_if_have_real_estate
            self.cost_if_have8_plex = cost_if_have8_plex

    def __str__(self):
        """Create string to be returned when str method is called."""
        if self.card_type in ["ApartmentHouseForSale", "XPlex"]:
            return ("\nBig Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.card_type +
                    "\nUnits:          " + str(self.units) +
                    "\nPrice:          " + str(self.price) +
                    "\nDown Payment:   " + str(self.down_payment) +
                    "\nCash Flow:      " + str(self.cash_flow) +
                    "\nPrice Range:    " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "HouseForSale":
            return ("\nBig Deal Card:" +
                    "\nTitle:          " + self.title +
                    "\nType:           " + self.card_type +
                    "\nHouse or Condo: " + self.house_or_condo +
                    "\nDown Payment:   " + str(self.down_payment) +
                    "\nCash Flow:      " + str(self.cash_flow) +
                    "\nPrice Range:    " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "Partnership":
            return ("\nBig Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.card_type +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.down_payment) +
                    "\nCash Flow:    " + str(self.cash_flow) +
                    "\nPrice Range:    " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "Land":
            return ("\nBig Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.card_type +
                    "\nAcres:        " + str(self.acres) +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.down_payment) +
                    "\nCash Flow:    " + str(self.cash_flow))
        elif self.card_type == "Business":
            return ("\nBig Deal Card:" +
                    "\nTitle:        " + self.title +
                    "\nType:         " + self.card_type +
                    "\nPrice:        " + str(self.price) +
                    "\nDown Payment: " + str(self.down_payment) +
                    "\nCash Flow:    " + str(self.cash_flow) +
                    "\nPrice Range:    " + str(self.price_range_low) + " - " +
                    str(self.price_range_high))
        elif self.card_type == "Expense":
            return ("\nBig Deal Card:" +
                    "\nTitle:                    " + self.title +
                    "\nType:                     " + self.card_type +
                    "\nCost if Have Real Estate: " +
                    str(self.cost_if_have_real_estate) +
                    "\nCost if Have 8-Plex     : " +
                    str(self.cost_if_have8_plex))
        else:
            print("big Deal Card Type: ", self.card_type, " not found")


def load_all_doodad_cards(doodad_cards_filename):
    """Load all Doodad Cards."""
    try:
        doodad_cards_dict = json_read_write_file.load_json(
            doodad_cards_filename)
    except OSError:
        print("No good Doodad Cards json file found, file not found, " +
              "please fix")
        raise OSError
    except ValueError:
        print("No good Doodad Cards json file found, ValueError, please fix")
        raise ValueError

    doodad_card_deck = Deck("Doodad Cards")
    for card in doodad_cards_dict:
        if doodad_cards_dict[card]["Type"] == "OneTimeExpense":
            doodad_card_deck.add_card(DoodadCard(
                doodad_cards_dict[card]["Title"],
                doodad_cards_dict[card]["Type"],
                int(doodad_cards_dict[card]["Cost"])))
        elif doodad_cards_dict[card]["Type"] == "ChildCost":
            doodad_card_deck.add_card(DoodadCard(
                doodad_cards_dict[card]["Title"],
                doodad_cards_dict[card]["Type"],
                0,  # 3 - One Time Payment
                int(doodad_cards_dict[card]["Cost if any Child"]),
                int(doodad_cards_dict[card]["Cost per Child"])))
        elif doodad_cards_dict[card]["Type"] == "NewLoan":
            doodad_card_deck.add_card(DoodadCard(
                doodad_cards_dict[card]["Title"],
                doodad_cards_dict[card]["Type"],
                int(doodad_cards_dict[card]["Down Payment"]),
                0,  # 4 - Any Child Payment
                0,  # 5 - Each Child Payment
                doodad_cards_dict[card]["Loan Name"],
                int(doodad_cards_dict[card]["Loan Amount"]),
                int(doodad_cards_dict[card]["Payment"])))
        else:
            print("Known Doodad card not found in row: ",
                  doodad_cards_dict[card])
    return doodad_card_deck


def load_all_market_cards(market_cards_filename):
    """Load all Market Cards from JSON File."""
    try:
        market_cards_dict = json_read_write_file.load_json(
            market_cards_filename)
    except OSError:
        print("No good Market Cards json file found, file not found, " +
              "please fix")
        raise OSError
    except ValueError:
        print("No good Market Cards json file found, ValueError, please fix")
        raise ValueError

    market_card_deck = Deck("Market Cards")
    for card in market_cards_dict:
        if market_cards_dict[card]["Title"] == "Small Business Improves":
            market_card_deck.add_card(MarketCard(
                market_cards_dict[card]["Title"],
                0,  # 2 - Cost/Price not used
                market_cards_dict[card]["Increased Cash Flow"],
                False,  # 4 - must_sell not used
                False))  # 5 - self_only not used.
        elif market_cards_dict[card]["Title"] in ["Condo Buyer - 2Br/1Ba",
                                                  "Shopping Mall Wanted",
                                                  "Buyer for 20 Acres",
                                                  "Price of Gold Soars",
                                                  "Car Wash Buyer",
                                                  "Software Company Buyer",
                                                  "Apartment House Buyer",
                                                  "House Buyer - 3Br/2Ba",
                                                  "Limited Partnership Sold",
                                                  "Plex Buyer"]:
            market_card_deck.add_card(MarketCard(
                market_cards_dict[card]["Title"],
                int(market_cards_dict[card]["Cost"]),
                0,  # 3 Increased Cash Flow not used
                market_cards_dict[card]["Must Sell"]))
        elif market_cards_dict[card]["Title"] == "Interest Rates Drop!":
            market_card_deck.add_card(MarketCard(
                market_cards_dict[card]["Title"],
                int(market_cards_dict[card]["Cost"]),
                0,  # 3  Increased Cash Flow not used
                market_cards_dict[card]["Must Sell"],
                market_cards_dict[card]["Self Only"]))
        elif market_cards_dict[card]["Title"] == "Inflation Hits!":
            market_card_deck.add_card(MarketCard(
                market_cards_dict[card]["Title"],
                0,  # 4 Cost not used),
                0,  # 3 Incr. Cash Flow not used
                True,
                True))
        else:
            print("Known Market card not found in row: ",
                  market_cards_dict[card])
    return market_card_deck


def load_all_small_deal_cards(small_deal_cards_filename):
    """Load all small deal cards for game simulation."""
    try:
        small_deal_cards_dict = json_read_write_file.load_json(
            small_deal_cards_filename)
    except OSError:
        print("No good Small Deal Cards json file found, file not found, " +
              "please fix")
        raise OSError
    except ValueError:
        print("No good Small Deal Cards json file found, ValueError, please " +
              "fix")
        raise ValueError
#    else:
#        noSmallDealCards = len(small_deal_cards_dict)
#        print(noSmallDealCards, "Small Deal Cards loaded")

    small_deal_card_deck = Deck("Small Deal Cards")
    for card in small_deal_cards_dict:
        if small_deal_cards_dict[card]["Type"] == "Stock":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unused for stock
                small_deal_cards_dict[card]["Symbol"],
                int(small_deal_cards_dict[card]["Cost"]),
                0,  # 6-Unused
                int(small_deal_cards_dict[card]["Dividend"]),
                0,  # 8-Unused
                int(small_deal_cards_dict[card]["Price Range Low"]),
                int(small_deal_cards_dict[card]["Price Range High"]),
                True))
        elif small_deal_cards_dict[card]["Type"] == "StockSplit":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unsed for stock split
                small_deal_cards_dict[card]["Symbol"],
                0,  # 5-Unused
                0,  # 6-Unused
                0,  # 7-Unused
                float(small_deal_cards_dict[card]["Split Ratio"]),
                0,  # 9-Unused
                0,  # 10-Unused
                True))
        elif small_deal_cards_dict[card]["Type"] == "HouseForSale":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                small_deal_cards_dict[card]["HouseOrCondo"],
                "",  # 4-Unused
                int(small_deal_cards_dict[card]["Cost"]),
                int(small_deal_cards_dict[card]["Down Payment"]),
                int(small_deal_cards_dict[card]["Cash Flow"]),
                0,  # 8-Unused
                int(small_deal_cards_dict[card]["Price Range Low"]),
                int(small_deal_cards_dict[card]["Price Range High"])))
        elif small_deal_cards_dict[card]["Type"] == "StartCompany":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unused
                "",  # Unsed
                int(small_deal_cards_dict[card]["Cost"]),
                int(small_deal_cards_dict[card]["Down Payment"]),
                int(small_deal_cards_dict[card]["Cash Flow"]),
                0,  # 8-Unused
                0,  # 9-Unused
                0,  # 10-Unused
                0))  # 11-Unused
        elif small_deal_cards_dict[card]["Type"] == "Asset":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unused
                "",  # Unsed
                int(small_deal_cards_dict[card]["Cost"]),
                int(small_deal_cards_dict[card]["Cost"]),  # Down Payment
                int(small_deal_cards_dict[card]["Cash Flow"]),
                0,  # 8-Unused
                int(small_deal_cards_dict[card]["Price Range Low"]),
                int(small_deal_cards_dict[card]["Price Range High"])))
        elif small_deal_cards_dict[card]["Type"] == "Land":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unused
                "",  # Unsed
                int(small_deal_cards_dict[card]["Cost"]),
                int(small_deal_cards_dict[card]["Down Payment"]),
                int(small_deal_cards_dict[card]["Acres"]),
                0,  # 8-Unused
                0,  # 9-Unused
                0,  # 10-Unused
                0))  # 11-Unused
        elif small_deal_cards_dict[card]["Type"] == "LoanNotToBeRepaid":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unused
                "",  # Unsed
                int(small_deal_cards_dict[card]["Cost"]),
                0,  # 6-Unused
                0,  # 7-Unused
                0,  # 8-Unused
                0,  # 9-Unused
                0,  # 10-Unused
                0))  # 11-Unused
        elif small_deal_cards_dict[card]["Type"] == "CostIfRentalProperty":
            small_deal_card_deck.add_card(SmallDealCard(
                small_deal_cards_dict[card]["Title"],
                small_deal_cards_dict[card]["Type"],
                "",  # Unused
                "",  # Unsed
                int(small_deal_cards_dict[card]["Cost"]),
                0,  # 6-Unused
                0,  # 7-Unused
                0,  # 8-Unused
                0,  # 9-Unused
                0,  # 10-Unused
                0))  # 11-Unused
        else:
            print("Small Deal Card known card not found in record: ",
                  small_deal_cards_dict[card])
    return small_deal_card_deck


def load_all_big_deal_cards(big_deal_cards_filename):
    """Load all Big Deal Cards for Game Simulations."""
    try:
        big_deal_cards_dict = json_read_write_file.load_json(
            big_deal_cards_filename)
    except OSError:
        print("No good Big Deal Cards json file found, file not found, " +
              "please fix")
        raise OSError
    except ValueError:
        print("No good Big Deal Cards json file found, ValueError, please fix")
        raise ValueError
#    else:
#        noBigDealCards = len(big_deal_cards_dict)
#        print(noBigDealCards, "Big Deal Cards loaded")

    big_deal_card_deck = Deck("Big Deal Cards")
    for card in big_deal_cards_dict:
        if big_deal_cards_dict[card]["Type"] in ["ApartmentHouseForSale",
                                                 "XPlex"]:
            big_deal_card_deck.add_card(BigDealCard(
                big_deal_cards_dict[card]["Title"],
                big_deal_cards_dict[card]["Type"],
                int(big_deal_cards_dict[card]["Cost"]),
                int(big_deal_cards_dict[card]["Down Payment"]),
                int(big_deal_cards_dict[card]["Cash Flow"]),
                int(big_deal_cards_dict[card]["Units"]),
                0,  # 7-Acres-unused
                int(big_deal_cards_dict[card]["Price Range Low"]),
                int(big_deal_cards_dict[card]["Price Range High"]),
                0,  # 10-unused-Cost if Have Real Estate
                0))  # 11-unused-Cost if Have 8-Plex
        elif big_deal_cards_dict[card]["Type"] in ["HouseForSale", "Business"]:
            big_deal_card_deck.add_card(BigDealCard(
                big_deal_cards_dict[card]["Title"],
                big_deal_cards_dict[card]["Type"],
                int(big_deal_cards_dict[card]["Cost"]),
                int(big_deal_cards_dict[card]["Down Payment"]),
                int(big_deal_cards_dict[card]["Cash Flow"]),
                0,  # 6-Units-unused
                0,  # 7-Acres-unused
                int(big_deal_cards_dict[card]["Price Range Low"]),
                int(big_deal_cards_dict[card]["Price Range High"]),
                0,  # 10-unused-Cost if Have Real Estate
                0))  # 11-unused-Cost if Have 8-Plex
        elif big_deal_cards_dict[card]["Type"] == "Land":
            big_deal_card_deck.add_card(BigDealCard(
                big_deal_cards_dict[card]["Title"],
                big_deal_cards_dict[card]["Type"],
                int(big_deal_cards_dict[card]["Cost"]),
                int(big_deal_cards_dict[card]["Down Payment"]),
                int(big_deal_cards_dict[card]["Cash Flow"]),
                0,  # 6-Units-unused
                int(big_deal_cards_dict[card]["Acres"]),
                0,  # 8-Price Range Low
                0,  # 9-Price Range High
                0,  # 10-unused-Cost if Have Real Estate
                0))  # 11-unused-Cost if Have 8-Plex
        elif big_deal_cards_dict[card]["Type"] == "Expense":
            big_deal_card_deck.add_card(BigDealCard(
                big_deal_cards_dict[card]["Title"],
                big_deal_cards_dict[card]["Type"],
                0,  # 3-Cost
                0,  # 4-Down Payment
                0,  # 5-Cash Flow
                0,  # 6-Units-unused
                0,  # 7-Acres-unused
                0,  # 8-Price Range Low
                0,  # 9-Price Range High
                int(big_deal_cards_dict[card]["Cost If Have Real Estate"]),
                int(big_deal_cards_dict[card]["Cost If Have 8-Plex"])))
        else:
            print("Big Deal Card known card not found in record: ",
                  big_deal_cards_dict[card])
    return big_deal_card_deck


class Deck(object):
    """Object to hod a Deck of Cards in Game Simulation."""

    def __init__(self, deckType):
        """Create a deck of cards for the Game Simulation."""
        self.deckType = deckType
        self.cards = []

    @property
    def no_cards(self):
        """Find the number of cards."""
        return len(self.cards)

    def add_card(self, card):
        """Add a card to the deck. This is how you create a deck."""
        self.cards.append(card)
        # return self.no_cards

    def take_random_card(self):
        """Take a random card from the deck. Wh? We don't know either."""
        import random
        try:
            return self.cards.pop(int(random.random()*self.no_cards))
        except IndexError:
            return None

    def take_top_card(self):
        """Take the top card of a deck. This is what to use."""
        try:
            return self.cards.pop()
        except IndexError:
            return None

    def shuffle(self):
        """Shuffle the deck."""
        import random
        random.shuffle(self.cards)

    def __copy__(self):
        """Copy a deck. Why?."""
        newDeck = Deck(self.deckType)
        for card in self.cards:
            newDeck.add_card(card)
        return newDeck

    def __str__(self):
        """Create string to be returned when str method is called."""
        card_string = ""
        for card in self.cards:
            card_string = card_string + str(card) + "\n"
        return card_string[:-1]


if __name__ == '__main__':  # test Card Objects
    small_deal_card_deck = load_all_small_deal_cards("SmallDealCards.json")
    big_deal_card_deck = load_all_big_deal_cards("BigDealCards.json")
    doodad_card_deck = load_all_doodad_cards("DoodadCards.json")
    market_card_deck = load_all_market_cards("MarketCards.json")

    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards)
#    print(small_deal_card_deck)
    print("No. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
#    print(big_deal_card_deck)
    print("No. of Doodad     Cards: ", doodad_card_deck.no_cards)
#    print(doodad_card_deck)
    print("No. of Market     Cards: ", market_card_deck.no_cards)
#    print(market_card_deck)

    bDCPR = []
    bDCPRError = []
    while True:
        big_deal_card = big_deal_card_deck.take_top_card()
        try:
            bDCPR.append((big_deal_card.price -
                          big_deal_card.price_range_low) /
                         (big_deal_card.price_range_high -
                          big_deal_card.price_range_low))
        except AttributeError:
            print("No Market Value, MAX or MIN on card:",
                  big_deal_card)
        except ZeroDivisionError:
            bDCPRError.append((big_deal_card.down_payment,
                               'No Price Range', "Card:" +
                               big_deal_card.title))
        if big_deal_card_deck.no_cards == 0:
            break

    bDCPR.sort()

    for aPR in bDCPR:
        print("{:.3f}".format(aPR))
    print("\n\n")
    for aPR in bDCPRError:
        print(aPR)

    print("\n\n\n")

    bDCROI = []
    big_deal_card_deck = load_all_big_deal_cards("BigDealCards.json")
    while True:
        big_deal_card = big_deal_card_deck.take_top_card()
        try:
            bDCROI.append(big_deal_card.cash_flow * 12 /
                          big_deal_card.down_payment)
        except AttributeError:
            print("No ROI on card:", big_deal_card.title)
        except ZeroDivisionError:
            print("Zero Down Payement:", big_deal_card.title)
        if big_deal_card_deck.no_cards == 0:
            break

    bDCROI.sort()

    for anROI in bDCROI:
        print("{:.3f}".format(anROI))


# TO DO - NEXT TO TRY - DECK METHODS - SHUFFLE, DEAL CARD, ETC. - COMPLETE
"""
    while True:
        card = small_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:",
            small_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    small_deal_card_deck = load_all_small_deal_cards("SmallDealCards.txt")
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = small_deal_card_deck.take_random_card()
        if card != None:
            print(card)
            print("Number of cards remaining:",
            small_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)

    while True:
        card = big_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:", big_deal_card_deck.no_cards)
        else:
            break

    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    big_deal_card_deck = load_all_big_deal_cards("big_deal_cards.txt")
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = big_deal_card_deck.take_random_card()
        if card != None:
            print(card)
            print("Number of cards remaining:", big_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)

    small_deal_card_deck = load_all_small_deal_cards("SmallDealCards.txt")
    big_deal_card_deck = load_all_big_deal_cards("big_deal_cards.txt")
    small_deal_card_deck.shuffle()
    big_deal_card_deck.shuffle()
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = small_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:",
            small_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    while True:
        card = big_deal_card_deck.take_top_card()
        if card != None:
            print(card)
            print("Number of cards remaining:", big_deal_card_deck.no_cards)
        else:
            break
    print("No. of Small Deal Cards: ", small_deal_card_deck.no_cards,
          "\nNo. of Big   Deal Cards: ", big_deal_card_deck.no_cards)
    print("Small Deck Type:", small_deal_card_deck.getDeckType(),
          "\nBig   Deck Type:", big_deal_card_deck.getDeckType())

"""

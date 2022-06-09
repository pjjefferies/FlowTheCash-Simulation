"""Simulate Game: This is where all the action is for simulating game."""
import cashflowsim.player_choice as player_choice
import cashflowsim.loans as loans
import cashflowsim.assets as assets


def board_space_action(player_on_board,
                       new_board_space,
                       verbose,
                       small_deal_card_deck,
                       big_deal_card_deck,
                       doodad_card_deck,
                       market_card_deck,
                       board):
    """Determine what action is needed for board space and make it so."""
    a_player = player_on_board[0]
    if a_player.strategy.manual:
        verbose = True
    #
    if verbose:
        print("Board Space:", new_board_space)
    space_type = new_board_space.board_space_type
    if space_type == "Opportunity":
        small_or_big_card = player_choice.choose_small_or_big_deal_card(
            a_player, verbose)
        if small_or_big_card == "small":
            picked_card = small_deal_card_deck.take_top_card()
            if verbose:
                print("Small Deal Picked Card:", picked_card,
                      "\nNo. Cards left:", small_deal_card_deck.no_cards)
            do_small_deal_action(a_player, picked_card, board, verbose)
        elif small_or_big_card == "big":
            picked_card = big_deal_card_deck.take_top_card()
            if verbose:
                print("Big Deal Picked Card:", picked_card,
                      "\nNo. Cards left:", big_deal_card_deck.no_cards)
            do_big_deal_action(a_player, picked_card, board, verbose)
    elif space_type == "Doodads":
        picked_card = doodad_card_deck.take_top_card()
        if verbose:
            print("Doodad Picked Card:", picked_card, "\nNo. Cards left:",
                  doodad_card_deck.no_cards)
        do_doodad_action(a_player, picked_card, verbose)
    elif space_type == "Charity":
        donate_to_charity_choice = player_choice.choose_to_donate_to_charity(
            a_player.strategy, verbose)
        if donate_to_charity_choice:
            if a_player.savings > 0.1 * a_player.salary:
                a_player.make_payment(int(0.1 * a_player.salary))
                a_player.start_charity_turns()
                if verbose:
                    print("Charity started")
            else:
                if verbose:
                    print("Sorry, you don't have enough money for charity")
    elif space_type == "Pay Check":
        return  # Paycheck handled if passed or landed-on in main routine
    elif space_type == "The Market":
        picked_card = market_card_deck.take_top_card()
        if verbose:
            print("Market Picked Card:", picked_card, "\nNo. Cards left:",
                  market_card_deck.no_cards)
        do_market_action(a_player, board, picked_card, verbose)
    elif space_type == "Baby":
        children = a_player.no_children
        a_player.have_child()
        if verbose:
            print("Children-Before: " + str(children) +
                  "\nChildren-After : " + str(a_player.no_children))
        return
    elif space_type == "Downsized":
        a_player.refresh()
        total_expenses = a_player.total_expenses
        if total_expenses > a_player.savings:
            new_loan_amount = int(((float(total_expenses) -
                                  float(a_player.savings))
                                 / 1000.0) + 1.0) * 1000
            if verbose:
                print("Not enough money, getting loan for",
                      str(new_loan_amount) + ".")
                new_loan = loans.Loan("Bank Loan", new_loan_amount,
                                     int(new_loan_amount/10), True)
                a_player.make_loan(new_loan)
        a_player.make_payment(total_expenses)
        a_player.start_layoff()
    else:
        print("Board Space Type unknown: " + space_type)
        assert ValueError


def do_market_action(this_player, board, picked_card, verbose):
    """Do action indicated on Market Card."""
    picked_card_type = picked_card.card_type
    if verbose:
        print("In do_market_action: Card:", picked_card)
    assert picked_card_type in [
        "Small Business Improves", "Condo Buyer - 2Br/1Ba",
        "Shopping Mall Wanted", "Buyer for 20 Acres", "Price of Gold Soars",
        "Car Wash Buyer", "Software Company Buyer", "Apartment House Buyer",
        "House Buyer - 3Br/2Ba", "Plex Buyer", "Limited Partnership Sold",
        "Interest Rates Drop!", "Inflation Hits!"]
    if picked_card_type == "Small Business Improves":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.business_assets:
                if asset.asset_type == "StartCompany":
                    asset.increase_cash_flow(picked_card.increased_cash_flow)
                    if verbose:
                        print("\nPlayer " + a_player.name +
                              " increased cash flow on asset " +
                              asset.name + " by " +
                              picked_card.increased_cash_flow + " to " +
                              asset.cash_flow + ".")
    elif picked_card_type == "Condo Buyer - 2Br/1Ba":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.real_estate_assets:
                if asset.house_or_condo == "Condo":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_real_estate(asset, picked_card.price,
                                                verbose)
    elif picked_card_type == "Shopping Mall Wanted":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.business_assets:
                if asset.name == "Small Shopping Mall for Sale":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_business(asset, picked_card.price,
                                              verbose)
    elif picked_card_type == "Buyer for 20 Acres":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.real_estate_assets:
                if asset.name == "Land":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_real_estate(asset, picked_card.price,
                                                verbose)
    elif picked_card_type == "Price of Gold Soars":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.business_assets:
                if asset.name == "Rare Gold Coin":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_business(asset, picked_card.price,
                                              verbose)
    elif picked_card_type == "Car Wash Buyer":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.business_assets:
                if asset.name == "Car Wash for Sale":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_business(asset, picked_card.price,
                                              verbose)
    elif picked_card_type == "Software Company Buyer":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.business_assets:
                if asset.name == "Start a Company Part Time-Software":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_business(asset, picked_card.price,
                                              verbose)
    elif picked_card_type == "Apartment House Buyer":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.real_estate_assets:
                if asset.asset_type == "ApartmentHouseForSale":
                    if player_choice.choose_to_sell_asset(
                            a_player, asset,
                            picked_card.price*asset.units, 0,
                            verbose):
                        a_player.sell_real_estate(
                            asset, picked_card.price*asset.units,
                            verbose)
    elif picked_card_type == "House Buyer - 3Br/2Ba":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.real_estate_assets:
                if asset.name == "House for Sale - 3Br/2Ba":
                    if player_choice.choose_to_sell_asset(a_player, asset,
                                                       picked_card.price,
                                                       0, verbose):
                        a_player.sell_real_estate(asset, picked_card.price,
                                                verbose)
    elif picked_card_type == "Plex Buyer":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.real_estate_assets:
                if asset.asset_type == "XPlex":
                    if player_choice.choose_to_sell_asset(
                            a_player, asset,
                            picked_card.price*asset.units, 0,
                            verbose):
                        a_player.sell_real_estate(
                            asset,
                            picked_card.price*asset.units, verbose)
    elif picked_card_type == "Limited Partnership Sold":
        for a_player_on_board in board.players:
            a_player = a_player_on_board[0]
            for asset in a_player.business_assets:
                if asset.name == "Limited Partner Wanted":
                    if player_choice.choose_to_sell_asset(
                            a_player, asset, picked_card.price,
                            0, verbose):
                        a_player.sell_business(asset, picked_card.price,
                                              verbose)
    elif picked_card_type == "Interest Rates Drop!":
        for real_estate_asset in this_player.real_estate_assets:
            if real_estate_asset.house_or_condo == "House":
                if player_choice.choose_to_sell_asset(
                        this_player, real_estate_asset, 0, 50000, verbose):
                    this_player.sell_real_estate(real_estate_asset,
                                               real_estate_asset.cost +
                                               50000,
                                               verbose)
    elif picked_card_type == "Inflation Hits!":
        for real_estate_asset in this_player.real_estate_assets:
            if real_estate_asset.house_or_condo == "House":
                this_player.sell_real_estate(real_estate_asset, 0, verbose)
    else:
        assert ValueError


def do_big_deal_action(this_player, picked_card, board, verbose):
    """Do a Big Deal Action indicated on Big Deal Cards."""
    picked_card_type = picked_card.card_type
    if verbose:
        print("In do_big_deal_action, Savings:", this_player.savings,
              "\nCard:", picked_card)
    assert picked_card_type in ["ApartmentHouseForSale", "XPlex", "Business",
                                "HouseForSale", "Land", "Expense"]
    #
    if picked_card_type in ["ApartmentHouseForSale", "XPlex"]:
        new_real_estate_asset = assets.RealEstate(
            picked_card.title,
            picked_card_type,
            None,
            picked_card.price,
            picked_card.down_payment,
            picked_card.cash_flow,
            picked_card.price_range_low,
            picked_card.price_range_high,
            picked_card.units,
            acres=0)
        if player_choice.choose_to_buy_asset(this_player, new_real_estate_asset,
                                          verbose):
            this_player.buy_real_estate(new_real_estate_asset, verbose)
        else:
            del new_real_estate_asset
    elif picked_card_type == "Business":
        new_business_asset = assets.Business(picked_card.title,
                                             picked_card_type,
                                             picked_card.price,
                                             picked_card.down_payment,
                                             picked_card.cash_flow,
                                             picked_card.price_range_low,
                                             picked_card.price_range_high)
        if player_choice.choose_to_buy_asset(this_player, new_business_asset,
                                          verbose):
            this_player.buy_business(new_business_asset, verbose)
        else:
            del new_business_asset
    elif picked_card_type == "HouseForSale":
        new_house_asset = assets.RealEstate(picked_card.title,
                                            picked_card_type,
                                            "House",
                                            picked_card.price,
                                            picked_card.down_payment,
                                            picked_card.cash_flow,
                                            picked_card.price_range_low,
                                            picked_card.price_range_high,
                                            units=0,
                                            acres=0)
        if player_choice.choose_to_buy_asset(this_player, new_house_asset,
                                          verbose):
            this_player.buy_real_estate(new_house_asset, verbose)
        else:
            del new_house_asset
    elif picked_card_type == "Land":
        new_land_asset = assets.RealEstate(picked_card.title,
                                           picked_card_type,
                                           "None",
                                           picked_card.price,
                                           picked_card.down_payment,
                                           0,  # cashFlow
                                           picked_card.price_range_low,
                                           picked_card.price_range_high,
                                           0,  # units
                                           picked_card.acres)
        if player_choice.choose_to_buy_asset(this_player,
                                          new_land_asset, verbose):
            this_player.buy_real_estate(new_land_asset, verbose)
        else:
            del new_land_asset
    elif picked_card_type == "Expense":
        if picked_card.cost_if_have_real_estate > 0:
            for real_estate_asset in this_player.real_estate_assets:
                if real_estate_asset.asset_type in ["HouseForSale",
                                                   "ApartmentHouseForSale",
                                                   "XPlex"]:
                    # havePropertyCost = picked_card.cost_if_have_real_estate
                    break
        elif picked_card.cost_if_have8_plex > 0:
            for real_estate_asset in this_player.real_estate_assets:
                if real_estate_asset.asset_type == "XPlex":
                    if real_estate_asset.units == 8:
                        # havePropertyCost = picked_card.cost_if_have8_plex
                        break


def do_small_deal_action(this_player, picked_card, board, verbose):
    """Do action indicated on Small Deal Card."""
    picked_card_type = picked_card.card_type
    if verbose:
        print("In do_small_deal_action, Savings:", this_player.savings,
              "Card:", picked_card)
    assert picked_card_type in ["Stock", "StockSplit", "HouseForSale",
                                "StartCompany", "Asset", "Land",
                                "LoanNotToBeRepaid", "CostIfRentalProperty"]

    if picked_card_type == "Stock":
        new_stock = assets.Stock(picked_card.symbol,
                                0,
                                picked_card.price,
                                picked_card.dividend,
                                picked_card.price_range_low,
                                picked_card.price_range_high)
        if not player_choice.choose_to_buy_stock_asset(this_player, new_stock,
                                                   verbose):
            del new_stock
            return
        this_player.buy_stock(new_stock, picked_card.price, verbose)
    #
    elif picked_card_type == "StockSplit":
        stock_symbol = picked_card.symbol
        stock_split_ratio = picked_card.split_ratio
        the_players = board.players
        for each_player_on_board in the_players:
            each_player = each_player_on_board[0]
            list_of_stocks = each_player.stock_assets
            for each_stock in list_of_stocks:
                if each_stock.name == stock_symbol:
                    each_stock.stock_split(stock_split_ratio)
    #
    elif picked_card_type == "HouseForSale":
        new_house_asset = assets.RealEstate(picked_card.title,
                                            picked_card_type,
                                            "House",
                                            picked_card.price,
                                            picked_card.down_payment,
                                            picked_card.cash_flow,
                                            picked_card.price_range_low,
                                            picked_card.price_range_high,
                                            units=0,
                                            acres=0)
        if player_choice.choose_to_buy_asset(this_player, new_house_asset,
                                          verbose):
            this_player.buy_real_estate(new_house_asset, verbose)
        else:
            del new_house_asset
    elif picked_card_type in ["StartCompany", "Asset"]:
        new_business_asset = assets.Business(picked_card.title,
                                             picked_card_type,
                                             picked_card.price,
                                             picked_card.down_payment,
                                             picked_card.cash_flow,
                                             picked_card.price_range_low,
                                             picked_card.price_range_high)
        if player_choice.choose_to_buy_asset(this_player, new_business_asset,
                                          verbose):
            this_player.buy_business(new_business_asset, verbose)
        else:
            del new_business_asset
    elif picked_card_type == "Land":
        new_land_asset = assets.RealEstate(picked_card.title,
                                           picked_card_type,
                                           "None",
                                           picked_card.price,
                                           picked_card.down_payment,
                                           0,  # cashFlow
                                           picked_card.price_range_low,
                                           picked_card.price_range_high,
                                           0,  # units
                                           picked_card.acres)
        if player_choice.choose_to_buy_asset(this_player, new_land_asset,
                                          verbose):
            this_player.buy_real_estate(new_land_asset, verbose)
        else:
            del new_land_asset
    elif picked_card_type == "LoanNotToBeRepaid":
        loan_not_to_be_repaid_amount = picked_card.price
        if this_player.savings < loan_not_to_be_repaid_amount:
            new_loan_amount = (int(((float(loan_not_to_be_repaid_amount) -
                                   float(this_player.savings)) /
                                  1000) + 1) * 1000)
            if verbose:
                print("Not enough money, getting loan for",
                      str(new_loan_amount) + ".")
            new_loan = loans.Loan("Bank Loan", new_loan_amount,
                                 int(new_loan_amount/10), True)
            this_player.make_loan(new_loan)
        this_player.make_payment(loan_not_to_be_repaid_amount)
    elif picked_card_type == "CostIfRentalProperty":
        cost_if_rental_property_amount = picked_card.price
        the_players = board.players
        for each_player_on_board in the_players:
            each_player = each_player_on_board[0]
            if len(each_player.real_estate_assets) > 0:
                if each_player.savings < cost_if_rental_property_amount:
                    new_loan_amount = (int(((float(cost_if_rental_property_amount) -
                                          float(each_player.savings)) /
                                          1000) + 1) * 1000)
                    if verbose:
                        print("Not enough money, getting loan for",
                              str(new_loan_amount) + ".")
                    new_loan = loans.Loan("Bank Loan", new_loan_amount,
                                         int(new_loan_amount / 10), True)
                    each_player.make_loan(new_loan)
                each_player.make_payment(cost_if_rental_property_amount)
    else:
        assert ValueError


def do_doodad_action(a_player, picked_card, verbose):
    """Do action on Doodad Card."""
    picked_card_type = picked_card.card_type
    if verbose:
        print("In do_doodad_action, Savings:", a_player.savings,
              "Card:", picked_card)
    assert picked_card_type in ["OneTimeExpense", "ChildCost", "NewLoan"]
    if picked_card_type == "OneTimeExpense":
        payment = picked_card.one_time_payment
        if a_player.savings < payment:
            new_loan_amount = (int(((float(payment) -
                                   float(a_player.savings)) /
                                  1000) + 1) * 1000)
            new_loan = loans.Loan("Bank Loan", new_loan_amount,
                                 int(new_loan_amount/10), True)
            a_player.make_loan(new_loan)
        if verbose:
            print("Making payment of", payment)
            print("Savings before:", a_player.savings)
        a_player.make_payment(payment)
        if verbose:
            print("Savings  after:", a_player.savings)
    elif picked_card_type == "ChildCost":
        any_cost_per_child = picked_card.any_child_payment
        per_cost_per_child = picked_card.each_child_payment
        no_children = a_player.no_children
        if no_children > 0:
            if verbose:
                print("You have kids, you must pay")
            payment = any_cost_per_child + no_children * per_cost_per_child
            if a_player.savings < payment:
                new_loan_amount = (int(((float(payment) -
                                       float(a_player.savings)) /
                                      1000) + 1) * 1000)
                new_loan = loans.Loan("Bank Loan", new_loan_amount,
                                     int(new_loan_amount / 10), True)
                a_player.make_loan(new_loan)
            a_player.make_payment(payment)
        else:
            if verbose:
                print("No kids, no payment required")
    elif picked_card_type == "NewLoan":
        new_loan_amount = picked_card.loan_amount
        new_loan = loans.Loan(picked_card.loan_title, new_loan_amount,
                             picked_card.loan_payment, False)
        a_player.make_loan(new_loan)
        a_player.make_payment(new_loan_amount + picked_card.one_time_payment)
    else:
        assert ValueError

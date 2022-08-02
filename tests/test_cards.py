# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import logging

# import pytest

from cashflowsim.cards import (
    CardDeck,
    EmptyDeckError,
    Card,
    load_all_doodad_cards,
    load_all_market_cards,
    load_all_small_deal_cards,
    load_all_big_deal_cards,
)

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
TESTS_DIR: str = "tests"
LOG_DIR: str = "game_logs"

SMALLDEALCARDS_FN: str = "SmallDealCards.json"
BIGDEALCARDS_FN: str = "BigDealCards.json"
DOODADCARDS_FN: str = "DoodadCards.json"
MARKETCARDS_FN: str = "MarketCards.json"
LOGFILE_FN: str = "log_file_test_cards.txt"
BAD_DOODAD_FILENAME_FN: str = "bad_doodad_filename"
BAD_JSON_FILE_NO_DATA_FN: str = "dummy_file_for_test.json"
BAD_DOODAD_JSON_FILE_ONE_BAD_DATUM_FN: str = "DoodadCards_One_Bad_Entry.json"
BAD_MARKET_JSON_FILE_ONE_BAD_DATUM_FN: str = "MarketCards_One_Bad_Entry.json"
BAD_SMALL_DEAL_JSON_FILE_ONE_BAD_DATUM_FN: str = "SmallDealCards_One_Bad_Entry.json"
BAD_BIG_DEAL_JSON_FILE_ONE_BAD_DATUM_FN: str = "BigDealCards_One_Bad_Entry.json"


base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)

small_deal_cards_path_fn: str = join(game_data_path, SMALLDEALCARDS_FN)
big_deal_cards_path_fn: str = join(game_data_path, BIGDEALCARDS_FN)
market_cards_path_fn: str = join(game_data_path, MARKETCARDS_FN)
doodad_cards_path_fn: str = join(game_data_path, DOODADCARDS_FN)
bad_doodad_cards_path_fn: str = join(game_data_path, BAD_DOODAD_FILENAME_FN)
bad_json_file_no_data_path_fn: str = join(
    base_path, TESTS_DIR, BAD_JSON_FILE_NO_DATA_FN
)
bad_doodad_json_file_one_bad_datum_path_fn: str = join(
    base_path, TESTS_DIR, BAD_DOODAD_JSON_FILE_ONE_BAD_DATUM_FN
)
bad_market_json_file_one_bad_datum_path_fn: str = join(
    base_path, TESTS_DIR, BAD_MARKET_JSON_FILE_ONE_BAD_DATUM_FN
)
bad_small_deal_json_file_one_bad_datum_path_fn: str = join(
    base_path, TESTS_DIR, BAD_SMALL_DEAL_JSON_FILE_ONE_BAD_DATUM_FN
)
bad_big_deal_json_file_one_bad_datum_path_fn: str = join(
    base_path, TESTS_DIR, BAD_BIG_DEAL_JSON_FILE_ONE_BAD_DATUM_FN
)

this_fn: str = __file__.split("\\")[-1].split(".")[0]
logfile_fn: str = "".join([this_fn, "_log.txt"])

logfile_path_fn: str = join(base_path, APP_DIR, LOG_DIR, logfile_fn)

logging.basicConfig(
    filename=logfile_path_fn,
    # level=logging.DEBUG,
    level=logging.ERROR,
    filemode="a",
    format="%(asctime)s - (%(levelname)s) %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    force=True,
)
logging.info(
    f"\n\n\nStart of new test run: {dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
)


def test_load_card_decks() -> None:
    logging.info("test_load_card_decks")
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_cards_path_fn
    )
    big_deal_card_deck: CardDeck = load_all_big_deal_cards(
        big_deal_cards_filename=big_deal_cards_path_fn
    )
    doodad_card_deck: CardDeck = load_all_doodad_cards(
        doodad_cards_filename=doodad_cards_path_fn
    )
    market_card_deck: CardDeck = load_all_market_cards(
        market_cards_filename=market_cards_path_fn
    )

    logging.info(f"No. of Small Deal Cards: {small_deal_card_deck.no_cards}")
    logging.info(f"No. of Big   Deal Cards: {big_deal_card_deck.no_cards}")
    logging.info(f"No. of Doodad     Cards: {doodad_card_deck.no_cards}")
    logging.info(f"No. of Market     Cards: {market_card_deck.no_cards}")
    logging.info(f"end test_load_card_decks")


def test_deal_all_big_deal_cards() -> None:
    logging.info("test_deal_all_big_deal_cards")
    big_deal_card_deck = load_all_big_deal_cards(
        big_deal_cards_filename=big_deal_cards_path_fn
    )
    big_deal_card_deck.shuffle()
    while True:
        try:
            card: Card = big_deal_card_deck.take_top_card()
        except EmptyDeckError:
            break
        logging.info(
            f"{card}\nNumber of cards remaining: {big_deal_card_deck.no_cards}"
        )


def test_big_deal_card_deck_values() -> None:
    big_deal_card_deck = load_all_big_deal_cards(
        big_deal_cards_filename=big_deal_cards_path_fn
    )
    big_deck_card_price_range_ratio: list[float] = []
    big_deal_card_roi: list[float] = []
    while True:
        try:
            big_deal_card = big_deal_card_deck.take_top_card()
        except EmptyDeckError:
            break
        print(big_deal_card)
        print(big_deal_card.price_range_high, " : ", big_deal_card.price_range_low)
        try:
            big_deck_card_price_range_ratio.append(
                (big_deal_card.price - big_deal_card.price_range_low)
                / (big_deal_card.price_range_high - big_deal_card.price_range_low)
            )
            if (
                big_deck_card_price_range_ratio[-1] < -1.0
                or big_deck_card_price_range_ratio[-1] > 1
            ):
                raise ValueError(
                    f"Big Deal Card Price Range Ratio out of range: {big_deck_card_price_range_ratio[-1]}."
                    f" Card: {big_deal_card}"
                )
        except AttributeError:
            raise AttributeError(
                f"No Market Value, MAX or MIN on card: {big_deal_card}"
            )
        except ZeroDivisionError:
            big_deck_card_price_range_ratio.append(0.0)
        try:
            big_deal_card_roi.append(
                big_deal_card.cash_flow * 12 / big_deal_card.down_payment
            )
        except AttributeError:
            raise AttributeError(f"No ROI on card: {big_deal_card.title}")
        except ZeroDivisionError:
            big_deal_card_roi.append(0.0)


def test_deal_all_small_deal_cards() -> None:
    logging.info("test_deal_all_small_deal_cards")
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_cards_path_fn
    )
    small_deal_card_deck.shuffle()
    while True:
        try:
            card: Card = small_deal_card_deck.take_top_card()
        except EmptyDeckError:
            break
        logging.info(
            f"{card}\nNumber of cards remaining: {small_deal_card_deck.no_cards}"
        )


def test_small_deal_card_deck_values() -> None:
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_cards_path_fn
    )
    small_deck_card_price_range_ratio: list[float] = []
    small_deal_card_roi: list[float] = []
    while True:
        try:
            small_deal_card = small_deal_card_deck.take_top_card()
        except EmptyDeckError:
            break
        print(small_deal_card.price_range_high, " : ", small_deal_card.price_range_low)
        try:
            small_deck_card_price_range_ratio.append(
                (small_deal_card.price - small_deal_card.price_range_low)
                / (small_deal_card.price_range_high - small_deal_card.price_range_low)
            )
            if (
                small_deck_card_price_range_ratio[-1] < -1.0
                or small_deck_card_price_range_ratio[-1] > 1.5
            ):
                raise ValueError(
                    f"small Deal Card Price Range Ratio out of range: {small_deck_card_price_range_ratio[-1]}."
                    f" Card: {small_deal_card}"
                )
        except AttributeError:
            raise AttributeError(
                f"No Market Value, MAX or MIN on card: {small_deal_card}"
            )
        except ZeroDivisionError:
            small_deck_card_price_range_ratio.append(0.0)
        try:
            small_deal_card_roi.append(
                small_deal_card.cash_flow * 12 / small_deal_card.down_payment
            )
        except AttributeError:
            raise AttributeError(f"No ROI on card: {small_deal_card.title}")
        except ZeroDivisionError:
            small_deal_card_roi.append(0.0)


def test_deal_all_market_deal_cards() -> None:
    logging.info("test_deal_all_market_deal_cards")
    market_card_deck: CardDeck = load_all_market_cards(
        market_cards_filename=join(game_data_path, MARKETCARDS_FN)
    )
    market_card_deck.shuffle()
    while True:
        try:
            card: Card = market_card_deck.take_top_card()
        except EmptyDeckError:
            break
        logging.info(f"{card}\nNumber of cards remaining: {market_card_deck.no_cards}")


def test_deal_all_doodad_deal_cards() -> None:
    logging.info("test_deal_all_doodad_deal_cards")
    doodad_card_deck: CardDeck = load_all_doodad_cards(
        doodad_cards_filename=join(game_data_path, DOODADCARDS_FN)
    )
    doodad_card_deck.shuffle()
    while True:
        try:
            card: Card = doodad_card_deck.take_top_card()
        except EmptyDeckError:
            break
        logging.info(f"{card}\nNumber of cards remaining: {doodad_card_deck.no_cards}")


def test_print_doodad_card_with_unknown_card_type() -> None:
    logging.info("test_print_doodad_card_with_unknown_card_type")
    doodad_card_deck: CardDeck = load_all_doodad_cards(
        doodad_cards_filename=join(game_data_path, DOODADCARDS_FN)
    )
    a_card: Card = doodad_card_deck.take_top_card()

    a_card.card_type = "Unicorn Ride"  # Don't try this at home

    try:
        logging.info(f"Card: {a_card}")
    except ValueError:
        logging.info(f"Correctly caught that doodad card card_type is unknown")
        return
    err_msg = f"Did not correctly catch that doodad card card_type is unknown"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_print_market_card_with_unknown_title() -> None:
    logging.info("test_print_market_card_with_unknown_title")
    market_card_deck: CardDeck = load_all_market_cards(
        market_cards_filename=join(game_data_path, MARKETCARDS_FN)
    )
    a_card: Card = market_card_deck.take_top_card()

    a_card.title = "Unicorn Ride"  # Don't try this at home

    try:
        logging.info(f"Card: {a_card}")
    except ValueError:
        logging.info(f"Correctly caught that market card title is unknown")
        return
    err_msg = f"Did not correctly catch that market card title is unknown"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_print_big_deal_card_with_unknown_card_type() -> None:
    logging.info("test_print_big_deal_card_with_unknown_card_type")
    big_deal_card_deck: CardDeck = load_all_big_deal_cards(
        big_deal_cards_filename=big_deal_cards_path_fn
    )
    a_card: Card = big_deal_card_deck.take_top_card()

    a_card.card_type = "Unicorn Ride"  # Don't try this at home

    try:
        logging.info(f"Card: {a_card}")
    except ValueError:
        logging.info(f"Correctly caught that big deal card card_type is unknown")
        return
    err_msg = f"Did not correctly catch that big deal card card_type is unknown"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_print_small_deal_card_with_unknown_card_type() -> None:
    logging.info("test_print_small_deal_card_with_unknown_card_type")
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_cards_path_fn
    )
    a_card: Card = small_deal_card_deck.take_top_card()

    a_card.card_type = "Unicorn Ride"  # Don't try this at home

    try:
        logging.info(f"Card: {a_card}")
    except ValueError:
        logging.info(f"Correctly caught that small deal card card_type is unknown")
        return
    err_msg = f"Did not correctly catch that small deal card card_type is unknown"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_print_card_with_unknown_category() -> None:
    logging.info("test_print_card_with_unknown_category")
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_cards_path_fn
    )
    a_card: Card = small_deal_card_deck.take_top_card()

    a_card.category = "Unicorn Card"  # Don't try this at home

    try:
        logging.info(f"Card: {a_card}")
    except ValueError:
        logging.info(f"Correctly caught that card category is unknown")
        return
    err_msg = f"Did not correctly catch that card category is unknown"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_print_small_deal_card_deck() -> None:
    logging.info("test_print_small_deal_card__deck")
    small_deal_card_deck: CardDeck = load_all_small_deal_cards(
        small_deal_cards_filename=small_deal_cards_path_fn
    )

    logging.info(f"Card Deck:\n{small_deal_card_deck}")
    logging.info(f"Printed Card Deck without errors")


def test_load_doodad_cards_bad_filename() -> None:
    bad_doodad_cards_path_fn = join(game_data_path, "on_the_moon.json")
    try:
        load_all_doodad_cards(doodad_cards_filename=bad_doodad_cards_path_fn)
    except OSError as e:
        logging.info(
            f"Doodad Cards filename: {bad_doodad_cards_path_fn} correctly not found "
            f"with message: {e}"
        )
        return
    err_msg = (
        f"Bad Doodad Cards filename: {bad_doodad_cards_path_fn} not reported as unfound"
    )
    logging.error(err_msg)
    raise OSError(err_msg)


def test_load_doodad_cards_bad_json_data() -> None:
    try:
        load_all_doodad_cards(doodad_cards_filename=bad_json_file_no_data_path_fn)
    except ValueError as e:
        logging.info(
            f"Doodad Cards filename: {bad_json_file_no_data_path_fn} correctly identified as bad json data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad Doodad Cards filename: {bad_json_file_no_data_path_fn} not reported as having bad json data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_doodad_cards_one_bad_card() -> None:
    try:
        load_all_doodad_cards(
            doodad_cards_filename=bad_doodad_json_file_one_bad_datum_path_fn
        )
    except ValueError as e:
        logging.info(
            f"Doodad Cards filename: {bad_doodad_json_file_one_bad_datum_path_fn} correctly"
            f" identified as having unreconised card data with message: {e}"
        )
        return
    err_msg = f"Bad Doodad Cards filename: {bad_doodad_json_file_one_bad_datum_path_fn} not reported as having unreconised card data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_market_cards_bad_filename() -> None:
    bad_market_cards_path_fn = join(game_data_path, "on_the_moon.json")
    try:
        load_all_market_cards(market_cards_filename=bad_market_cards_path_fn)
    except OSError as e:
        logging.info(
            f"Market Cards filename: {bad_market_cards_path_fn} correctly not found "
            f"with message: {e}"
        )
        return
    err_msg = (
        f"Bad Market Cards filename: {bad_market_cards_path_fn} not reported as unfound"
    )
    logging.error(err_msg)
    raise OSError(err_msg)


def test_load_market_cards_bad_json_data() -> None:
    try:
        load_all_market_cards(market_cards_filename=bad_json_file_no_data_path_fn)
    except ValueError as e:
        logging.info(
            f"Market Cards filename: {bad_json_file_no_data_path_fn} correctly identified as bad json data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad Market Cards filename: {bad_json_file_no_data_path_fn} not reported as having bad json data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_market_cards_one_bad_card() -> None:
    try:
        load_all_market_cards(
            market_cards_filename=bad_market_json_file_one_bad_datum_path_fn
        )
    except ValueError as e:
        logging.info(
            f"Market Cards filename: {bad_market_json_file_one_bad_datum_path_fn} correctly identified as having unreconised card data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad Market Cards filename: {bad_market_json_file_one_bad_datum_path_fn} not reported as having unreconised card data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_small_deal_cards_bad_filename() -> None:
    bad_small_deal_cards_path_fn = join(game_data_path, "on_the_moon.json")
    try:
        load_all_small_deal_cards(
            small_deal_cards_filename=bad_small_deal_cards_path_fn
        )
    except OSError as e:
        logging.info(
            f"Small_deal Cards filename: {bad_small_deal_cards_path_fn} correctly not found "
            f"with message: {e}"
        )
        return
    err_msg = f"Bad small_deal Cards filename: {bad_small_deal_cards_path_fn} not reported as unfound"
    logging.error(err_msg)
    raise OSError(err_msg)


def test_load_small_deal_cards_bad_json_data() -> None:
    try:
        load_all_small_deal_cards(
            small_deal_cards_filename=bad_json_file_no_data_path_fn
        )
    except ValueError as e:
        logging.info(
            f"Small_deal Cards filename: {bad_json_file_no_data_path_fn} correctly identified as bad json data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad small_deal Cards filename: {bad_json_file_no_data_path_fn} not reported as having bad json data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_small_deal_cards_one_bad_card() -> None:
    try:
        load_all_small_deal_cards(
            small_deal_cards_filename=bad_small_deal_json_file_one_bad_datum_path_fn
        )
    except ValueError as e:
        logging.info(
            f"Small_deal Cards filename: {bad_small_deal_json_file_one_bad_datum_path_fn} correctly identified as having unreconised card data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad small_deal Cards filename: {bad_small_deal_json_file_one_bad_datum_path_fn} not reported as having unreconised card data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_big_deal_cards_bad_filename() -> None:
    bad_big_deal_cards_path_fn = join(game_data_path, "on_the_moon.json")
    try:
        load_all_big_deal_cards(big_deal_cards_filename=bad_big_deal_cards_path_fn)
    except OSError as e:
        logging.info(
            f"Big_deal Cards filename: {bad_big_deal_cards_path_fn} correctly not found "
            f"with message: {e}"
        )
        return
    err_msg = f"Bad big_deal Cards filename: {bad_big_deal_cards_path_fn} not reported as unfound"
    logging.error(err_msg)
    raise OSError(err_msg)


def test_load_big_deal_cards_bad_json_data() -> None:
    try:
        load_all_big_deal_cards(big_deal_cards_filename=bad_json_file_no_data_path_fn)
    except ValueError as e:
        logging.info(
            f"Big_deal Cards filename: {bad_json_file_no_data_path_fn} correctly identified as bad json data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad big_deal Cards filename: {bad_json_file_no_data_path_fn} not reported as having bad json data"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_load_big_deal_cards_one_bad_card() -> None:
    try:
        load_all_big_deal_cards(
            big_deal_cards_filename=bad_big_deal_json_file_one_bad_datum_path_fn
        )
    except ValueError as e:
        logging.info(
            f"Big_deal Cards filename: {bad_big_deal_json_file_one_bad_datum_path_fn} correctly identified as having unreconised card data"
            f"with message: {e}"
        )
        return
    err_msg = f"Bad big_deal Cards filename: {bad_big_deal_json_file_one_bad_datum_path_fn} not reported as having unreconised card data"
    logging.error(err_msg)
    raise ValueError(err_msg)

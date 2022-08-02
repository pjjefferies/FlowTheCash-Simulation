# -*- coding: utf-8 -*-
"""
Created on Sat May  7 23:48:49 2022

@author: PaulJ
"""
from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import logging

from cashflowsim.profession import Profession, get_profession_defs

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
TESTS_DIR: str = "tests"
LOG_DIR: str = "game_logs"

PROFESSIONS_FN = "ProfessionsList.json"
BAD_PROFESSIONS_FN = "BadProfessionsList.json"
BAD_PROFESSIONS_CONTENT_FN = "dummy_file_for_test.json"
PROFESSIONS_LIST = (
    "Lawyer",
    "Engineer",
    "Doctor",
    "Secretary",
    "Nurse",
    "Business Manager",
    "Airline Pilot",
    "Mechanic",
    "Teacher (K-12)",
    "Truck Driver",
    "Police Officer",
    "Janitor",
)

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)
profession_data_path_fn: str = join(game_data_path, PROFESSIONS_FN)
bad_profession_data_path_fn: str = join(game_data_path, BAD_PROFESSIONS_FN)
bad_profession_content_data_path_fn: str = join(
    base_path, TESTS_DIR, BAD_PROFESSIONS_CONTENT_FN
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


def test_load_all_professions() -> None:
    """Test Class to test Profession objects in profession module."""

    professions: dict[str, Profession] = get_profession_defs(profession_data_path_fn)
    logging.info(f"{len(professions)} professions successfully loaded")
    for a_profession in PROFESSIONS_LIST:
        logging.info(f"Checking in list for {professions[a_profession]}...")
        professions.pop(a_profession)
        logging.info(f"Confirmed that {a_profession} was loaded")
    assert not professions
    logging.info(f"All professions loaded and there are none extra")


def test_bad_file_name_load_professions() -> None:
    """Test Class to test detecting bad profeesions file."""

    try:
        get_profession_defs(bad_profession_data_path_fn)
    except OSError as e:
        logging.info(
            f"Detecting non-existent professions file successfully detected with message {e}"
        )
        return
    err_msg = (
        f"Bad Professions file {bad_profession_data_path_fn} not reported as unfound"
    )
    logging.error(err_msg)
    raise OSError(err_msg)


def test_bad_file_name_contents_load_professions() -> None:
    """Test Class to test detecting bad profeesions file contents"""

    try:
        get_profession_defs(bad_profession_content_data_path_fn)
    except ValueError as e:
        logging.info(
            f"Detecting bad professions file successfully detected with message {e}"
        )
        return
    err_msg = (
        f"Bad Professions file {bad_profession_data_path_fn} not reported no good data"
    )
    logging.error(err_msg)
    raise ValueError(err_msg)

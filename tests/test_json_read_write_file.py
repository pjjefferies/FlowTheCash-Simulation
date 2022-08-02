# -*- coding: utf-8 -*-

from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import logging
from re import T

from cashflowsim.json_read_write_file import load_json, write_json

APP_DIR: str = "cashflowsim"
TESTS_DIR = "tests"
LOG_DIR: str = "game_logs"

TEST_JSON_FN: str = "test_json_file_for_write_read.json"

TEST_DATA: dict[str, dict[str, str | int]] = {
    "Player1": {
        "name": "Player1 Name",
        "Profession": "Engineer",
        "Strategy": "Manual",
        "Salary": 1_000_000,
    },
    "Player2": {
        "name": "Players Name",
        "Profession": "Doctor",
        "Strategy": "Dave Ramsey",
        "Salary": 150_000,
    },
    "Player1": {
        "name": "Player3 Name",
        "Profession": "Program Manager",
        "Strategy": "Manual",
        "Salary": 70_000,
    },
}

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
test_json_file_path_fn: str = join(base_path, APP_DIR, LOG_DIR, TEST_JSON_FN)

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


def test_write_json() -> None:
    logging.info(f"Writting test data to json file {test_json_file_path_fn}")
    write_json(file_name=test_json_file_path_fn, data_to_write=TEST_DATA)
    logging.info(f"Wrote test data to json file {test_json_file_path_fn}")


def test_read_json() -> None:
    logging.info(f"Writting test data to json file {test_json_file_path_fn}")
    write_json(file_name=test_json_file_path_fn, data_to_write=TEST_DATA)
    logging.info(f"Wrote test data to json file {test_json_file_path_fn}")

    logging.info(f"Loading test data from json file {test_json_file_path_fn}")
    NEW_TEST_DATA: dict[str, dict[str, str | int]] = load_json(
        file_name=test_json_file_path_fn
    )
    logging.info(f"Read test data from json file {test_json_file_path_fn}")
    assert TEST_DATA == NEW_TEST_DATA
    logging.info(
        f"Read test data from json file {test_json_file_path_fn} matches original test data"
    )

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

from os import listdir
from os.path import join, abspath
from inspect import getsourcefile
import datetime as dt
import logging
import pytest

from cashflowsim.board import Board, load_board_spaces, PlayerNotOnBoardError
from cashflowsim.roll_die import roll_die
from cashflowsim.player import Player
from cashflowsim.profession import Profession, get_profession_defs
from cashflowsim.strategy import Strategy, get_strategy_defs

APP_DIR: str = "cashflowsim"
GAME_DATA_DIR: str = "game_data"
STRATEGIES_DIR = "simulation_strategies"
TESTS_DIR = "tests"
LOG_DIR: str = "game_logs"

BOARDSPACES_FN = "RatRaceBoardSpaces.json"
BAD_BOARDSPACES_FN = "BadRatRaceBoardSpaces.json"
BAD_BOARDSPACES_CONTENT_FN = "dummy_file_for_test.json"
PROFESSIONS_FN = "ProfessionsList.json"
PLAYER1_NAME = "Player1"
PLAYER1_PROF = "Engineer"
PLAYER2_NAME = "Player2"
PLAYER2_PROF = "Business Manager"

base_path: str = "\\".join(abspath(str(getsourcefile(lambda: 0))).split("\\")[:-2])
game_data_path: str = join(base_path, APP_DIR, GAME_DATA_DIR)
boardspace_path_fn: str = join(game_data_path, BOARDSPACES_FN)
bad_boardspace_path_fn: str = join(game_data_path, BAD_BOARDSPACES_FN)
bad_boardspace_content_path_fn = join(base_path, TESTS_DIR, BAD_BOARDSPACES_CONTENT_FN)
profession_data_path_fn: str = join(game_data_path, PROFESSIONS_FN)
strategies_data_path: str = join(base_path, APP_DIR, STRATEGIES_DIR)

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

strategies_fn_list: list[str] = [
    f for f in listdir(strategies_data_path) if f.endswith(".json")
]
all_strategies: dict[str, Strategy] = {}
for a_strategy_fn in strategies_fn_list:
    strategy_defs_fn: str = join(base_path, APP_DIR, STRATEGIES_DIR, a_strategy_fn)
    some_strategies: dict[str, Strategy] = get_strategy_defs(
        strategy_defs_fn=strategy_defs_fn
    )
    all_strategies.update(some_strategies)


def test_load_board_bad_filename() -> None:
    try:
        load_board_spaces(board_spaces_filename=bad_boardspace_path_fn)
    except OSError as e:
        logging.info(
            f"RatRaceBoard Filename: {bad_boardspace_path_fn} correctly not found "
            f"with message: {e}"
        )
        return
    err_msg = (
        f"Bad RatRaceBoard Filename: {bad_boardspace_path_fn} not reported as unfound"
    )
    logging.error(err_msg)
    raise OSError(err_msg)


def test_load_board_bad_file_contents() -> None:
    try:
        load_board_spaces(board_spaces_filename=bad_boardspace_content_path_fn)
    except ValueError as e:
        logging.info(
            f"RatRaceBoard Filename: {bad_boardspace_content_path_fn} correctly flagged as invalid "
            f"with message: {e}"
        )
        return
    err_msg = f"Bad RatRaceBoard Filename: {bad_boardspace_content_path_fn} not reported as invalid"
    logging.error(err_msg)
    raise ValueError(err_msg)


def test_create_board_non_verbose() -> None:
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)
    logging.info(f"RatRaceBoard Type: {rat_race_board.board_type}")
    logging.info(rat_race_board)
    logging.info(f"End of Board\n\n")


def test_create_board_verbose() -> None:
    rat_race_board: Board = load_board_spaces(
        board_spaces_filename=boardspace_path_fn, verbose=True
    )
    logging.info(f"RatRaceBoard Type: {rat_race_board.board_type}")
    logging.info(rat_race_board)
    logging.info(f"End of Board\n\n")


def test_adding_player_to_board_default_space() -> None:
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(a_player=player1)  # Add player1 to board at space 0

    assert player1.board_space_no == 0


def test_adding_player_to_board_0_space() -> None:
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(
        a_player=player1, board_space=0
    )  # Add player1 to board at space 0

    assert player1.board_space_no == 0


def test_adding_player_to_board_10_space() -> None:
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(
        a_player=player1, board_space=10
    )  # Add player1 to board at space 0

    assert player1.board_space_no == 10


def test_adding_player_to_board_neg_5_space() -> None:  # should ignore out of bounds space and put on space 0
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(
        a_player=player1, board_space=-5
    )  # Add player1 to board at space 0

    assert player1.board_space_no == 0


def test_adding_player_to_board_105_space() -> None:  # should ignore out of bounds space and put on space 0
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(
        a_player=player1, board_space=105
    )  # Add player1 to board at space 0

    assert player1.board_space_no == 0


def test_players_moving_on_board() -> None:
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    player2: Player = Player(
        name=PLAYER2_NAME,
        profession=profession_defs[PLAYER2_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(
        a_player=player1, board_space=0
    )  # Add player1 to board at space 0
    rat_race_board.add_player(
        a_player=player2, board_space=0
    )  # Add player1 to board at space 0
    for turn in range(1, 101):  # Simulate 100 turns
        currentboard_player = rat_race_board.next_player
        main_move_spaces: int = roll_die(strategy="Automatic", no_of_dice=1)
        (
            new_position,
            main_passed_pay_check,
            newBoardSpace,
        ) = rat_race_board.move_player_board_spaces(
            a_player=currentboard_player, move_spaces=main_move_spaces
        )
        assert new_position is not None, "Player is not on the board"
        logging.info(
            f"Turn: {turn:3}, Player: {currentboard_player.name}, "
            f"Roll: {str(main_move_spaces)}, "
            f"Current Space: {new_position:2}, "
            f"Type: {newBoardSpace.board_space_type}. "
            f"Pay Check Passed: {str(main_passed_pay_check)}"
        )


def test_moving_a_player_not_on_board() -> None:
    rat_race_board: Board = load_board_spaces(board_spaces_filename=boardspace_path_fn)

    profession_defs: dict[str, Profession] = get_profession_defs(
        profession_data_path_fn
    )
    player1: Player = Player(
        name=PLAYER1_NAME,
        profession=profession_defs[PLAYER1_PROF],
        strategy=all_strategies["Manual"],
    )
    player2: Player = Player(
        name=PLAYER2_NAME,
        profession=profession_defs[PLAYER2_PROF],
        strategy=all_strategies["Manual"],
    )
    rat_race_board.add_player(
        a_player=player1, board_space=0
    )  # Add player1 to board at space 0

    new_position: int = 0
    with pytest.raises(PlayerNotOnBoardError):
        (
            new_position,
            _,
            _,
        ) = rat_race_board.move_player_board_spaces(a_player=player2, move_spaces=1)

    assert new_position is not None, "Player is not on the board"
    logging.info(f"Player not on the board detected")

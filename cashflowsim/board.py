"""Manage Board for Game Simulation."""
import logging

from dataclasses import dataclass, field
from cashflowsim.json_read_write_file import load_json
from cashflowsim.player import Player

log = logging.getLogger(__name__)


class PlayerNotOnBoardError(Exception):
    """Raise error if no players are loaded and something is tried on players on-board."""

    def __init__(self, message: str):
        self.message = message


@dataclass(kw_only=True)
class BoardSpace:
    """Create a Space to be put on a Board."""

    board_space_type: str
    description: str = ""

    def __post_init__(self):
        """Post-initialization."""
        pass

    def __str__(self):
        """Create string to be returned when str method is called."""
        return (
            f"\nType:        {self.board_space_type}"
            f"\nDescription: {self.description}"
        )


@dataclass(kw_only=True)
class Board:
    """Object to represent Game Board."""

    board_type: str
    board_spaces: list[BoardSpace] = field(default_factory=list)
    players: list[Player] = field(
        default_factory=list
    )  # List of lists containing [player obj., space #]
    current_player_no: int = 0

    def add_board_space(self, *, board_space: BoardSpace) -> None:
        """Add a board space to a board. This is how you build a board."""
        self.board_spaces.append(board_space)

    def move_player_board_spaces(
        self, *, a_player: Player, move_spaces: int
    ) -> tuple[int, bool, BoardSpace]:
        """Move a player on a board by specified number of spaces."""
        moves_remaining = move_spaces
        passed_pay_check = False
        try:
            player_list_index = self.players.index(a_player)
        except ValueError:
            raise PlayerNotOnBoardError(f"player {a_player} is not on board to move")
        old_board_index: int = self.players[player_list_index].board_space_no
        new_board_index = old_board_index
        while moves_remaining > 0:
            new_board_index += 1
            moves_remaining -= 1
            if new_board_index > (len(self.board_spaces) - 1):
                new_board_index = 0
            if self.board_spaces[new_board_index].board_space_type == "Pay Check":
                passed_pay_check = True
        self.players[player_list_index].board_space_no = new_board_index
        return (new_board_index, passed_pay_check, self.board_spaces[new_board_index])

    def add_player(self, *, a_player: Player, board_space: int = 0):
        """Add a player to the board as a list of [player, space number]."""
        if board_space < 0 or board_space > (len(self.board_spaces) - 1):
            board_space = 0  # if starting space is not on board, start at 0
        a_player.board_space_no = board_space
        self.players.append(a_player)
        if len(self.players) == 1:
            # initiate current_player for get_next_player method
            self.current_player_no = -1

    @property
    def next_player(self) -> Player:
        """Return the next player to play."""
        self.current_player_no += 1
        if self.current_player_no > (len(self.players) - 1):
            self.current_player_no = 0
        return self.players[self.current_player_no]

    def __str__(self):
        """Create string to be returned when str method is called."""
        board_string = ""
        for board_space in self.board_spaces:
            board_string = board_string + str(board_space) + "\n"
        return board_string[:-1]


def load_board_spaces(*, board_spaces_filename: str, verbose: bool = False):
    """Load Board Spaces from JSON file."""
    try:
        board_space_defs = load_json(file_name=board_spaces_filename)
    except OSError:
        raise OSError(
            f"{board_spaces_filename} file not found to load board splaces, please fix"
        )
    except ValueError:
        raise ValueError(
            f"No good json file found in {board_spaces_filename}, ValueError, please fix"
        )
    else:
        no_board_spaces = len(board_space_defs)
        if verbose:
            print(no_board_spaces, "boad spaces loaded")
    board = Board(board_type="Rat Race")
    for board_space_no in range(1, no_board_spaces + 1):
        space_name = "boardSpaceNo" + "{:03d}".format(board_space_no)
        board.add_board_space(
            board_space=BoardSpace(
                board_space_type=board_space_defs[space_name]["Board Space Title"],
                description=board_space_defs[space_name]["Board Space Detail"],
            )
        )
    return board

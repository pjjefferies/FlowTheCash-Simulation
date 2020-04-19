"""Manage Board for Game Simulation."""
from json_read_write_file import load_json


class BoardSpace(object):
    """Create a Space to be put on a Board."""

    def __init__(self, board_space_type, description=""):
        """Create a Space to be put on a Board."""
        self.board_space_type = board_space_type
        self.description = description

    def __str__(self):
        """Create string to be returned when str method is called."""
        return("\nType:        " + self.board_space_type + "\nDescription: " +
               self.description)


class Board(object):
    """Object to represent Game Board."""

    def __init__(self, board_type):
        """Create the Game Board Object."""
        self.board_type = board_type
        self.board_spaces = []
        self.players = []  # List of lists containing [player obj., space #]

    def add_board_space(self, board_space):
        self.board_spaces.append(board_space)

    def move_player_board_spaces(self, board_player, move_spaces):
        moves_remaining = move_spaces
        passed_pay_check = False
        player_list_index = self.players.index(board_player)
        if player_list_index == None:
            print("Player: " + player.name + " is not on the board")
            return None, None, None
        new_board_index = self.players[player_list_index][1]
        while moves_remaining > 0:
            new_board_index += 1
            moves_remaining -= 1
            if new_board_index > (len(self.board_spaces) - 1):
                new_board_index = 0
            if self.board_spaces[new_board_index].board_space_type == "Pay Check":
                passed_pay_check = True
        self.players[player_list_index][1] = new_board_index
        return new_board_index, passed_pay_check, self.board_spaces[new_board_index]

    def add_player(self, player, starting_space=0):
        """Add a player to the board as a list of [player, space number]."""
        if starting_space > (len(self.board_spaces) - 1):
            starting_space = 0  # if starting space is not on board, start at 0
        self.players.append([player, starting_space])
        if len(self.players) == 1:
            # initiate current_player for get_next_player method
            self.current_player = -1

    @property
    def players_on_board(self):
        """Return true list of players objects without their locations."""
        return [player for player, _ in self.players]

    def get_next_player(self):
        """Return the next player to play."""
        self.current_player += 1
        if self.current_player > (len(self.players) - 1):
            self.current_player = 0
        return self.players[self.current_player]

    def __str__(self):
        """Create string to be returned when str method is called."""
        board_string = ""
        for boardSpace in self.board_spaces:
            board_string = board_string + str(boardSpace) + "\n"
        return board_string[:-1]


def getboard_spaces(board_spaces_file_name, verbose=False):
    """Load Board Spaces from JSON file."""
    try:
        board_space_defs = load_json(board_spaces_file_name)
    except OSError:
        print("No good json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good json file found, ValueError, please fix")
        raise ValueError
    else:
        no_board_spaces = len(board_space_defs)
        if verbose:
            print(no_board_spaces, "boad spaces loaded")
    board = Board("Rat Race")
    for board_space_no in range(1, no_board_spaces + 1):
        space_name = "boardSpaceNo" + "{:03d}".format(board_space_no)
        board.add_board_space(BoardSpace(
            board_space_defs[space_name]["Board Space Title"],
            board_space_defs[space_name]["Board Space Detail"]))
    return board


if __name__ == '__main__':  # test board objects
    from die_roll import roll_die
    from player import Player, get_profession_defs
    ratRaceBoard = getboard_spaces("RatRaceBoardSpaces.json")
    print("ratRaceBoard Type: " + ratRaceBoard.board_type)

    print(ratRaceBoard)
    print("End of Board\n\n")

    # Import list of professions
    profession_defs = get_profession_defs("ProfessionsList.json")
    me = Player("PaulCool", profession_defs["Engineer"], "Manual")  # Create me
    she = Player("LynnHot", profession_defs["Doctor"], "Manual")  # Create she
    ratRaceBoard.add_player(me, 0)  # Add me to board at space 0
    ratRaceBoard.add_player(she, 0)  # Add she to board at space 0
    for turn in range(1, 101):  # Simulate 100 turns
        currentboard_player = ratRaceBoard.get_next_player()
        print("\ncurrentboard_player:", currentboard_player[0].name)
        move_spaces = roll_die("Automatic", 1, False)
        print("Die roll", move_spaces)
        newPosition, passed_pay_check, newBoardSpace = (
            ratRaceBoard.move_player_board_spaces(currentboard_player, move_spaces))
        if newPosition is None:
            print("Player is not on the board")
            break
        else:
            print("Turn: {:>3}".format(turn) +
                  ", Player: " + currentboard_player[0].name +
                  ", Roll: " + str(move_spaces) +
                  ", Current Space: {:>2}".format(newPosition) +
                  ", Type: " + newBoardSpace.board_space_type +
                  ", Pay Check Passed: " + str(passed_pay_check))

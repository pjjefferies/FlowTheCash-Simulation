# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

import unittest

class TestBoard(unittest.TestCase):
    """Test Class to test Board objects in board module."""
    from board import Board, BoardSpace, load_board_spaces
    from die_roll import roll_die
    from player import Player
    from profession import get_profession_defs
    rat_race_board = load_board_spaces("RatRaceBoardSpaces.json")
    print("ratRaceBoard Type: " + rat_race_board.board_type)

    print(rat_race_board)
    print("End of Board\n\n")

    # Import list of professions
    profession_defs = get_profession_defs("ProfessionsList.json")
    me = Player("PaulCool", profession_defs["Engineer"], "Manual")  # Create me
    she = Player("LynnHot", profession_defs["Doctor"], "Manual")  # Create she
    rat_race_board.add_player(me, 0)  # Add me to board at space 0
    rat_race_board.add_player(she, 0)  # Add she to board at space 0
    for turn in range(1, 101):  # Simulate 100 turns
        currentboard_player = rat_race_board.next_player
        print("\ncurrentboard_player:", currentboard_player[0].name)
        main_move_spaces = roll_die("Automatic", 1, False)
        print("Die roll", main_move_spaces)
        new_position, main_passed_pay_check, newBoardSpace = (
            rat_race_board.move_player_board_spaces(currentboard_player,
                                                    main_move_spaces))
        if new_position is None:
            print("Player is not on the board")
            break
        print("Turn: {:>3}".format(turn) +
              ", Player: " + currentboard_player[0].name +
              ", Roll: " + str(main_move_spaces) +
              ", Current Space: {:>2}".format(new_position) +
              ", Type: " + newBoardSpace.board_space_type +
              ", Pay Check Passed: " + str(main_passed_pay_check))


if __name__ == '__main__':
    unittest.main(verbosity=2)

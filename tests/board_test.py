# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 22:33:00 2022

@author: PaulJ
"""

BOARDSPACES_FN = '../game_data/RatRaceBoardSpaces.json'
PROFESSIONS_FN = '../game_data/ProfessionsList.json'
PLAYER1_NAME = 'PaulCool'
PLAYER1_PROF = 'Engineer'
PLAYER2_NAME = 'YohanAmI'
PLAYER2_PROF = 'Business Manager'

import unittest

class TestBoard(unittest.TestCase):
    """Test Class to test Board objects in board module."""
    from cashflowsim.board import Board, BoardSpace, load_board_spaces
    from cashflowsim.die_roll import roll_die
    from cashflowsim.player import Player
    from cashflowsim.profession import get_profession_defs

    def test_create_board(self):
        rat_race_board = TestBoard.load_board_spaces(BOARDSPACES_FN)
        print("ratRaceBoard Type: " + rat_race_board.board_type)

        print(rat_race_board)
        print("End of Board\n\n")


    def test_players_moving_on_board(self):
        rat_race_board = TestBoard.load_board_spaces(BOARDSPACES_FN)

        profession_defs = TestBoard.get_profession_defs(PROFESSIONS_FN)
        me = TestBoard.Player(PLAYER1_NAME, profession_defs[PLAYER1_PROF], "Manual")  # Create me
        she = TestBoard.Player(PLAYER2_NAME, profession_defs[PLAYER2_PROF], "Manual")  # Create she
        rat_race_board.add_player(me, 0)  # Add me to board at space 0
        rat_race_board.add_player(she, 0)  # Add she to board at space 0
        for turn in range(1, 101):  # Simulate 100 turns
            with self.subTest(i=turn):
                currentboard_player = rat_race_board.next_player
                main_move_spaces = TestBoard.roll_die("Automatic", 1, False)
                new_position, main_passed_pay_check, newBoardSpace = (
                    rat_race_board.move_player_board_spaces(currentboard_player,
                                                            main_move_spaces))
                self.assertIsNotNone(new_position,
                                     msg='Player is not on the board')
                print("Turn: {:>3}".format(turn) +
                      ", Player: " + currentboard_player[0].name +
                      ", Roll: " + str(main_move_spaces) +
                      ", Current Space: {:>2}".format(new_position) +
                      ", Type: " + newBoardSpace.board_space_type +
                      ", Pay Check Passed: " + str(main_passed_pay_check))


if __name__ == '__main__':
    unittest.main(verbosity=2)

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:57:35 2020

@author: PaulJ
"""

import unittest
import player
import profession
import strategy


class TestPlayer(unittest.TestCase):
    """Test Class to test Player objects in player module."""

    PROFESSION_DEFS = profession.get_profession_defs("ProfessionsList.json")
    STRATEGY_DEFS = strategy.get_strategy_defs("Strategies.json")

    # Make Available Strategies to Test
    # tests = [{'

    def test_player(self):
        """General test using list of tests above."""
        list_of_player = []
        for a_profession in self.PROFESSION_DEFS:  # create player example for
            name = a_profession + " Player"
            list_of_player.append(player.Player(
                name,
                self.PROFESSION_DEFS[a_profession],
                self.STRATEGY_DEFS["Standard Auto"]))
        # print(len(LIST_OF_PLAYERS), "players created")
        for a_player in list_of_player:
            self.assertIsInstance(a_player, player.Player)
            # print(A_PLAYER)
        # print("End")


if __name__ == '__main__':
    unittest.main(verbosity=2)

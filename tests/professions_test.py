# -*- coding: utf-8 -*-
"""
Created on Sat May  7 23:48:49 2022

@author: PaulJ
"""

PROFESSIONS_FN = '../game_data/ProfessionsList.json'
PROFESSIONS_LIST = ('Lawyer', 'Engineer', 'Doctor', 'Secretary', 'Nurse',
                    'Business Manager', 'Airline Pilot', 'Mechanic',
                    'Teacher (K-12)', 'Truck Driver', 'Police Officer',
                    'Janitor')


import unittest

class TestProfessions(unittest.TestCase):
    """Test Class to test Profession objects in profession module."""

    from cashflowsim.profession import Profession, get_profession_defs

    def test_check_all_professions_returned(self):
        professions = TestProfessions.get_profession_defs(PROFESSIONS_FN)
        for a_profession in PROFESSIONS_LIST:
            professions.pop(a_profession)
        self.assertDictEqual(professions, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)


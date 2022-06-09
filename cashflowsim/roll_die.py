"""Functions related to rolling a die."""

import random

def roll_die(strategy="Manual", no_of_dice=1, verbose=False):
    """Roll a die."""
    if strategy == "Manual":
        verbose = True
        if no_of_dice == 1:
            input("Hit 'Enter' to roll die ")
        else:
            input("Hit 'Enter' to roll " + str(no_of_dice) + " dice")
    total_die_roll = 0
    for _ in range(no_of_dice):
        total_die_roll += random.choice([1, 2, 3, 4, 5, 6])
    if verbose:
        print("Total Dice: ", str(total_die_roll))
    return total_die_roll

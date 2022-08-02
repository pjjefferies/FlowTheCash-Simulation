"""Functions related to rolling a die."""

import logging
import random

log = logging.getLogger(__name__)


def roll_die(*, strategy: str = "Manual", no_of_dice: int = 1) -> int:
    """Roll a die."""
    if strategy == "Manual":
        if no_of_dice == 1:
            input(f"Hit 'Enter' to roll die")
        else:
            input(f"Hit 'Enter' to roll {no_of_dice} dice")
    total_die_roll: int = 0
    for _ in range(no_of_dice):
        total_die_roll += random.choice([1, 2, 3, 4, 5, 6])
    if strategy == "Manual":
        print(f"Total of Dice: {total_die_roll}")
    log.info(f"Total of Dice: {total_die_roll}")
    return total_die_roll

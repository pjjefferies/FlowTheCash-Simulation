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


if __name__ == '__main__':  # test die rolling
    import statistics
    print("\n100 Automatic Rolls in verbose mode")
    for roll in range(100):  # Try 100 automatic rolls in verbose
        die_result = roll_die("Automatic", 1, True)

    print("\n100 Automatic Rolls in non-verbose mode")
    die_rolls = []
    for roll in range(100):  # Try 100 automatic rolls in quiet
        die_result = roll_die("Automatic", 1, False)
        die_rolls.append(die_result)
    mean_die_roll = statistics.mean(die_rolls)
    std_dev_die_roll = statistics.stdev(die_rolls)
    print("For 100 Automatic Die Rolls: Mean =", str(mean_die_roll),
          "Std. Dev. =", str(std_dev_die_roll))

    print("\n10 Manual Rolls in verbose mode")
    for roll in range(10):
        die_result = roll_die("Manual", 1, True)

    print("\n10 Manual Rolls of two dice in non-verbose mode")
    die_rolls = []
    for roll in range(10):
        die_result = roll_die("Manual", 2, False)
        die_rolls.append(die_result)
    mean_die_roll = statistics.mean(die_rolls)
    std_dev_die_roll = statistics.stdev(die_rolls)
    print("For 10 Manual Rolls of 2 Dice: Mean =", str(mean_die_roll),
          "Std. Dev. =", str(std_dev_die_roll
                             ))

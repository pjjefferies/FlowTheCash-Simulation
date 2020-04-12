"""Functions related to rolling a die."""


def rollDie(strategy="Manual", noOfDice=1, verbose=False):
    """Roll a die."""
    import random
    if strategy == "Manual":
        verbose = True
        if noOfDice == 1:
            input("Hit 'Enter' to roll die ")
        else:
            input("Hit 'Enter' to roll " + str(noOfDice) + " dice")
    totalDieRoll = 0
    for dieNo in range(noOfDice):
        totalDieRoll += random.choice([1, 2, 3, 4, 5, 6])
    if verbose:
        print("Total Dice: ", str(totalDieRoll))
    return totalDieRoll


if __name__ == '__main__':  # test die rolling
    import statistics
    print("\n100 Automatic Rolls in verbose mode")
    for roll in range(100):  # Try 100 automatic rolls in verbose
        dieResult = rollDie("Automatic", 1, True)

    print("\n100 Automatic Rolls in non-verbose mode")
    dieRolls = []
    for roll in range(100):  # Try 100 automatic rolls in quiet
        dieResult = rollDie("Automatic", 1, False)
        dieRolls.append(dieResult)
    meanDieRoll = statistics.mean(dieRolls)
    stdevDieRoll = statistics.stdev(dieRolls)
    print("For 100 Automatic Die Rolls: Mean =", str(meanDieRoll),
          "Std. Dev. =", str(stdevDieRoll))

    print("\n10 Manual Rolls in verbose mode")
    for roll in range(10):
        dieResult = rollDie("Manual", 1, True)

    print("\n10 Manual Rolls of two dice in non-verbose mode")
    dieRolls = []
    for roll in range(10):
        dieResult = rollDie("Manual", 2, False)
        dieRolls.append(dieResult)
    meanDieRoll = statistics.mean(dieRolls)
    stdevDieRoll = statistics.stdev(dieRolls)
    print("For 10 Manual Rolls of 2 Dice: Mean =", str(meanDieRoll),
          "Std. Dev. =", str(stdevDieRoll))

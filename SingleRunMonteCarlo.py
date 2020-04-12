# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:20:09 2015

@author: PaulJ
"""


def singleRunRepeat(professionObj, strategyObj, repetitions, verbose):
    """Run Cash Flow Simulations."""
    import random
    import CashFlowRatRaceSimulation as cfrrs

    oneResultsList = []

    for test in range(0, repetitions):
        random.seed(test)

        if test % (max(repetitions/5.0, 100)) == 0:
            print("Profession:", professionObj.getProfession(), "Strategy:",
                  strategyObj.getName(), "Running Test:", test, "test of",
                  testsToRun)

        amIRich, amIBroke, turnCounter = cfrrs.CashFlowRatRaceGameSimulation(
            professionObj,
            strategyObj,
            verbose)
        oneResultsList.append([test, professionObj.getProfession(),
                               strategyObj.getName(), amIRich, amIBroke,
                               turnCounter])

    return oneResultsList


if __name__ == '__main__':
    import time
    import player
    import csv
    import datetime

    verbose = False
    testsToRun = 100
    professionDict = player.getProfessionDict("ProfessionsList.json")
    strategyDict = player.getStrategyDict("Strategies_3.json")
    noSims = len(professionDict) * len(strategyDict)
    timeSim = True

    resultsTitleList = ['test no.', 'professionName', 'strategyName',
                        'Am I Rich', 'Am I Poor', 'Turns']
    resultsListToSave = []

    gameFileLogFilename = "GameLog-" + datetime.datetime.now().strftime(
        '%Y%m%d-%H%M%S') + 'csv'
    with open(gameFileLogFilename, "w", newline='') as OutputFile:
        writer = csv.writer(OutputFile, delimiter=",")
        writer.writerow(resultsTitleList)
        startTime = time.time()
        if timeSim:
            singleStartTime = time.time()
        for professionToEval in iter(professionDict):
            for strategyToEval in iter(strategyDict):
                resultsListToSave = singleRunRepeat(
                    professionDict[professionToEval],
                    strategyDict[strategyToEval],
                    testsToRun, verbose)
                for gameResult in resultsListToSave:
                    writer.writerow(gameResult)
                if timeSim:
                    singleTime = time.time() - singleStartTime
                    print('Time per prof, strat combo:',
                          '{0:.1f}'.format(singleTime),
                          "seconds.\nTotal Expected Time:",
                          "{0:.1f}".format((singleTime*noSims)))
                    timeSim = False
        OutputFile.close()

    print("Time to run", testsToRun, "tests for each profession/strategy:",
          '{0:.2f}'.format(time.time() - startTime), "seconds.")

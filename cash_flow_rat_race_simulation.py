"""Main module for running Cash Flow Rat Race Simulation."""

# from importlib import reload
import board
# reload(board)
import cards
# reload(cards)
import player
# reload(player)
import player_choice
# reload(player_choice)
import dieRoll
# reload(dieRoll)
import boardSpaceAction
# reload(boardSpaceAction)
import random
import copy
import time


def CashFlowRatRaceGameSimulation(aProfession,
                                  aStrategy,
                                  verbose=False):
    """Initiate Cash Flow Rat Race Simulation."""
    # Create Rat Race Board
    ratRaceBoard = board.getBoardSpaces("RatRaceBoardSpaces.json")

    # Create 4 Card Decks - not used except as starting points
    smallDealCardDeckMaster = cards.loadAllSmallDealCards(
        "SmallDealCards.json")
    bigDealCardDeckMaster = cards.loadAllBigDealCards("BigDealCards.json")
    doodadCardDeckMaster = cards.loadAllDoodadCards("DoodadCards.json")
    marketCardDeckMaster = cards.loadAllMarketCards("MarketCards.json")

    # Start Main Loop, initiate decks to be used, shuffle and
    # create turn counter

    smallDealCardDeck = copy.copy(smallDealCardDeckMaster)
    bigDealCardDeck = copy.copy(bigDealCardDeckMaster)
    doodadCardDeck = copy.copy(doodadCardDeckMaster)
    marketCardDeck = copy.copy(marketCardDeckMaster)

    smallDealCardDeck.shuffle()
    bigDealCardDeck.shuffle()
    doodadCardDeck.shuffle()
    marketCardDeck.shuffle()

    # Create player and add to Board, starting at space 0
    player_name = aProfession.getProfession() + "_Player"
    aPlayer = player.Player(player_name, aProfession, aStrategy)
    ratRaceBoard.addPlayer(aPlayer, 0)

    turnCounter = 0
    while True:
        turnCounter += 1
        playerOnBoard = ratRaceBoard.getNextPlayer()
        amIRich, amIBroke = playerOnBoard[0].refresh()
        if verbose:
            print("After first refresh")
            print(aPlayer)
        if verbose:
            print(playerOnBoard[0].getName(), ", Turn:", turnCounter)

        # Offer to allow pay-off any loans pre-roll
        if player_choice.chooseToPayOffLoan(playerOnBoard[0]):
            amIRich, amIBroke = playerOnBoard[0].refresh()
            if amIRich:
                print("After", turnCounter, "turns, Player",
                      playerOnBoard[0].getName(), "is rich and wins")
                print("Passive income:", playerOnBoard[0].getPassiveIncome(),
                      "\nExpenses      :", playerOnBoard[0].getTotalExpenses())
                print(playerOnBoard[0])
                print("Sold Assets\n\n", playerOnBoard[0].getSoldAssets())
                break
            elif amIBroke:
                print("Player", playerOnBoard[0].getName(),
                      "is broke and looses")
                break  # Replace with remove player later for multiple player

        # If have charity, roll 1 or 2 dice, otherwise, roll 1
        if playerOnBoard[0].getCharityTurns() > 0:
            playerOnBoard[0].useCharityTurn()
            noOfDice = player_choice.chooseNoDie(
                [1, 2], playerOnBoard[0].getStrategy(), verbose)
        else:
            noOfDice = 1

        # If layed-off, skip turn
        if playerOnBoard[0].getSkippedTurnsRemaining() > 0:
            if verbose:
                print("Using a layoff day, " + str(
                    playerOnBoard[0].getSkippedTurnsRemaining()) +
                    " turns remaining")
            playerOnBoard[0].useLayoff()
            continue

        # Roll the die
        aDieRoll = dieRoll.rollDie(playerOnBoard[0].getStrategy(),
                                   noOfDice,
                                   verbose)

        # Move based on dice roll
        playerOnBoard[1], passedPaycheck, newBoardSpace = (
            ratRaceBoard.movePlayerBoardSpaces(playerOnBoard, aDieRoll))

        # If passed paycheck, show me the money
        if passedPaycheck:
            playerOnBoard[0].earnSalary()

        # Take action based on board space
        boardSpaceAction.boardSpaceAction(
            playerOnBoard, newBoardSpace, verbose,
            smallDealCardDeck, bigDealCardDeck, doodadCardDeck, marketCardDeck,
            ratRaceBoard)

        amIRich, amIBroke = playerOnBoard[0].refresh()
        if amIRich:
            if verbose:
                print("After", turnCounter, "turns, Player",
                      playerOnBoard[0].getName(), "is rich and wins")
                print("Passive income:", playerOnBoard[0].getPassiveIncome(),
                      "\nExpenses      :", playerOnBoard[0].getTotalExpenses())
                print(playerOnBoard[0])
                print("Sold Assets\n\n", playerOnBoard[0].getSoldAssets())
            break
        elif amIBroke:
            if verbose:
                print("After", turnCounter, "turns, Player",
                      playerOnBoard[0].getName(), "is broke and looses")
                print(playerOnBoard[0])
                print("Sold Assets\n\n", playerOnBoard[0].getSoldAssets())
            break

        # Offer to allow pay-off any loans post-roll
        if player_choice.chooseToPayOffLoan(playerOnBoard[0], verbose):
            amIRich, amIBroke = playerOnBoard[0].refresh()
            if amIRich:
                if verbose:
                    print("After", turnCounter, "turns, Player",
                          playerOnBoard[0].getName(), "is rich and wins")
                    print("Passive income:",
                          playerOnBoard[0].getPassiveIncome(),
                          "\nExpenses      :",
                          playerOnBoard[0].getTotalExpenses())
                    print(playerOnBoard[0])
                    print("Sold Assets\n\n", playerOnBoard[0].getSoldAssets())
                break
            elif amIBroke:
                if verbose:
                    print("Player", playerOnBoard[0].getName,
                          "is broke and looses")
                break  # Replace with remove player later for multiple player

        # Check if any card decks need to be shuffled
        if verbose:
            print("Entering check if any card decks need to be shuffled")
        if doodadCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Doodad Deck, shuffling...")
            doodadCardDeck = copy.copy(doodadCardDeckMaster)
            doodadCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Doodad Deck:",
                      doodadCardDeck.getNoCards())
        elif smallDealCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Small Deal Deck, shuffling...")
            smallDealCardDeck = copy.copy(smallDealCardDeckMaster)
            smallDealCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Small Deal Deck:",
                      smallDealCardDeck.getNoCards())
        elif bigDealCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Big Deal Deck, shuffling...")
            bigDealCardDeck = copy.copy(bigDealCardDeckMaster)
            bigDealCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Big Deal Deck:",
                      bigDealCardDeck.getNoCards())
        elif marketCardDeck.getNoCards() == 0:
            if verbose:
                print("At the bottom of Market Deck, shuffling...")
            marketCardDeck = copy.copy(marketCardDeckMaster)
            marketCardDeck.shuffle()
            if verbose:
                print("After shuffling, cards now in Market Deck:",
                      marketCardDeck.getNoCards())

        # End of Game Play Loop
    return amIRich, amIBroke, turnCounter


if __name__ == '__main__':
    for test in range(0, 500):
        startTime = time.time()
        random.seed(test)
    # Load list of professions and create empty list of players

        professionDict = player.getProfessionDict("ProfessionsList.json")

    # Create a player to test in manual mode/strategy, set verbose mode to true
        strategyDict = player.getStrategyDict("Strategies.json")

    # Example settings to test
        professionName = "Engineer"
        strategyName = "Standard Auto"
        verbose = False

        amIRich, amIBroke, turnCounter = CashFlowRatRaceGameSimulation(
            professionDict[professionName],
            strategyDict[strategyName],
            verbose)

        print("Test #:", test, "\n   Am I Rich:", amIRich, "\n   Am I Poor:",
              amIBroke, "\n   No of Turns:", turnCounter, "\n        Time:",
              (time.time()-startTime), "seconds\n\n\n")

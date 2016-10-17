from jsonReadWriteFile import *


class BoardSpace(object):
    def __init__(self, boardSpaceType, description=""):
        self.boardSpaceType = boardSpaceType
        self.description = description
    def getBoardSpaceType(self):
        return self.boardSpaceType
    def getBoardSpaceDescription(self):
        return self.boardSpaceDescription
    def __str__(self):
        return("\nType:        " + self.boardSpaceType + "\nDescription: " + self.description)


class Board(object):
    def __init__(self, boardType):
        self.boardType = boardType
        self.boardSpaces = []
        self.players = []
    def getBoardType(self):
        return self.boardType
    def getBoardSpaces(self):
        return self.boardSpaces
    def addBoardSpace(self, boardSpace):
        self.boardSpaces.append(boardSpace)
    def movePlayerBoardSpaces(self, boardPlayer, moveSpaces):
        movesRemaining = moveSpaces
        passedPayCheck = False
        playerListIndex = self.players.index(boardPlayer)
        if playerListIndex == None:
            print("Player: " + player.getName() + " is not on the board")
            return None, None, None
        newBoardIndex = self.players[playerListIndex][1]
        while movesRemaining > 0:
            newBoardIndex += 1
            movesRemaining -= 1
            if newBoardIndex > (len(self.boardSpaces) - 1):
                newBoardIndex = 0
            if self.boardSpaces[newBoardIndex].getBoardSpaceType() == "Pay Check":
                passedPayCheck = True
        self.players[playerListIndex][1] = newBoardIndex
        return newBoardIndex, passedPayCheck, self.boardSpaces[newBoardIndex]
    def addPlayer(self, player, startingSpace = 0):
        if startingSpace > (len(self.boardSpaces) - 1):
            startingSpace = 0   #if starting space is not on board, start at 0 space
        self.players.append([player, startingSpace]) #player on board is list of player object and location
        if len(self.players) == 1:
            self.currentPlayer = -1     #initiate currentPlayer for getNextPlayer method
    def getPlayerList(self):        #To use for actions potentially affecting multiple players
        playerList = []             #Return true list of players objects without their locations
        for playerOnBoard in self.players:
            playerList.append(playerOnBoard[0])
        return playerList
    def getNextPlayer(self):
        self.currentPlayer += 1
        if self.currentPlayer > (len(self.players) - 1):
            self.currentPlayer = 0
        return self.players[self.currentPlayer]
    def __str__(self):
        boardString = ""
        for boardSpace in self.boardSpaces:
            boardString = boardString + str(boardSpace) + "\n"
        return boardString[:-1]

"""   Old version using csv file for board spaces
def getBoardSpaces(boardSpacesFileName):
    import csv
    with open(boardSpacesFileName, "r") as boardSpacesFile:
        reader = csv.reader(boardSpacesFile)
        board = Board("Rat Race")
        for row in reader:
            if row[0] != [] and row[0][0] != "#":
                if len(row) > 1:
                    description = row[1]
                else:
                    description = ""
                board.addBoardSpace(BoardSpace(row[0],description))
                if len(row) > 2:
                    print("3rd members and beyond ignored in BoardSpaces")
        boardSpacesFile.close()
    return board
"""

def getBoardSpaces(boardSpacesFileName, verbose = False):
    try:
        boardSpaceDict = load_json(boardSpacesFileName)
    except OSError:
        print("No good json file found, file not found, please fix")
        raise OSError
    except ValueError:
        print("No good json file found, ValueError, please fix")
        raise ValueError
    else:
        noBoardSpaces = len(boardSpaceDict)
        if verbose:
            print(noBoardSpaces, "boad spaces loaded")
    board = Board("Rat Race")
    for boardSpaceNo in range(1,noBoardSpaces+1):
        spaceName = "boardSpaceNo" + "{:03d}".format(boardSpaceNo)
        board.addBoardSpace(BoardSpace(boardSpaceDict[spaceName]["Board Space Title"],
                                       boardSpaceDict[spaceName]["Board Space Detail"]))
    return board



if __name__ == '__main__':      #test board objects
    from dieRoll import *
    from player import *
    #ratRaceBoard = getBoardSpaces("RatRaceBoardSpaces.txt")
    ratRaceBoard = getBoardSpaces("RatRaceBoardSpaces.json")
    print("ratRaceBoard Type: " + ratRaceBoard.getBoardType())
    #print("ratRaceBoard Spaces: ", ratRaceBoard.getBoardSpaces())
    
    print(ratRaceBoard)
    print("End of Board\n\n")

    #professionDict = getProfessionDict("ProfessionsList.txt")      #Import list of professions
    professionDict = getProfessionDict("ProfessionsList.json")      #Import list of professions
    me  = Player("PaulCool", professionDict["Engineer"], "Manual")     #create me
    she = Player("LynnHot", professionDict["Doctor"], "Manual")     #create she
    ratRaceBoard.addPlayer(me, 0)   #add me to board at space 0
    ratRaceBoard.addPlayer(she, 0)   #add she to board at space 0
    for turn in range(1,101):     #simulate 100 turns
        currentBoardPlayer = ratRaceBoard.getNextPlayer()
        print("\ncurrentBoardPlayer:", currentBoardPlayer[0].getName())
        moveSpaces = rollDie("Automatic", 1, False)
        print("Die roll", moveSpaces)
        newPosition, passedPayCheck, newBoardSpace = ratRaceBoard.movePlayerBoardSpaces(currentBoardPlayer, moveSpaces)
        if newPosition == None:
            print("Player is not on the board")
            break
        else:
            print("Turn: {:>3}".format(turn) +
                  ", Player: " + currentBoardPlayer[0].getName() +
                  ", Roll: " + str(moveSpaces) +
                  ", Current Space: {:>2}".format(newPosition) +
                  ", Type: " + newBoardSpace.getBoardSpaceType() +
                  ", Pay Check Passed: " + str(passedPayCheck))


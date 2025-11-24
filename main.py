import game

def main():
    winReward = 10000
    maximumTurn = 3
    turnPenalty = [1000] * maximumTurn
    groupNumber = 4
    giveUpPenalty = 3000
    simpleVersion = True
    myGame = game.Game(winReward, maximumTurn, groupNumber, turnPenalty, giveUpPenalty, simpleVersion)
    shouldReadFromFile = True
    fileName = "simpleVersion.pkl" if simpleVersion else "complexVersion.pkl"
    if shouldReadFromFile:
        print(f"Reading from {fileName}")
        myGame.loadFromFile(fileName)
    else:
        print("Solving mdp")
        myGame.solve()
        print(f"Saving the optimal policy to {fileName}")
        myGame.saveToFile(fileName)
    continueGame = True
    while continueGame:
        myGame.startNewGame()
        userInput = ''
        while True:
            userInput = input("Do you want to start a new game (Y/n): ")
            if userInput == '':
                continue
            if userInput[0].lower() == 'n':
                continueGame = False
                break
            elif userInput[0].lower() == 'y':
                continueGame = True
                break
    print("Thanks for playing!")

if __name__ == "__main__":
    main()

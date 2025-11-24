import mahjongmdp
import util
import pickle

class Game:
    def __init__(self, winReward, maximumTurn, groupNumber, turnPenalty, giveUpPenalty, simpleVersion = False):
        self.winReward = winReward
        self.maximumTurn = maximumTurn
        self.groupNumber = groupNumber
        if len(turnPenalty) != maximumTurn:
            raise Exception('Wrong turnPenalty')
        self.turnPenalty = turnPenalty
        self.giveUpPenalty = giveUpPenalty
        self.target = 2 + groupNumber * 3
        self.hasCalculatedPi = False
        self.pi = {}
        self.mdp = mahjongmdp.MahjongMDP(winReward, maximumTurn, groupNumber, turnPenalty, giveUpPenalty, simpleVersion)

    def solve(self):
        alg = util.ValueIteration()
        alg.solve(self.mdp, 1)
        self.pi = alg.pi
        self.hasCalculatedPi = True

    def saveToFile(self, filename="data.pkl"):
        if not self.hasCalculatedPi:
            raise Exception("Need to caulcate Pi first")
        with open(filename, "wb") as f:
            pickle.dump(self.pi, f)

    def loadFromFile(self, filename="data.pkl"):
        with open(filename, "rb") as f:
            self.pi = pickle.load(f)
            self.hasCalculatedPi = True

    def convertToTiles(self, state):
        hand = state[0]

        res = ''
        for i in range(9):
            for j in range(hand[i]):
                res += str(i + 1)
        return res

    def startNewGame(self):
        if not self.hasCalculatedPi:
            raise Exception("Need to caulcate Pi first")

        startRandomHand = True
        while True:
            userInput = input('Do you want to specify your starting hand? (Y/N) ')
            if userInput == '':
                continue
            if userInput[0].lower() == 'y':
                startRandomHand = False
                break
            elif userInput[0].lower() == 'n':
                startRandomHand = True
                break

        if startRandomHand:
            state = self.mdp.startState()
        else:
            state = self.mdp.customState()
        totalReward = 0

        currentTurn = 1

        while state[1] is not None:
            actions = self.mdp.actions(state)

            # Automatically draw a tile if need to
            if "Draw" in actions:
                newTile = self.mdp.getRandomTile(state)
                print(f"You drawed {newTile + 1}")
                newHand = list(state[0])
                newRemaining = list(state[2])
                newHand[newTile] += 1
                newRemaining[newTile] -= 1
                newState = (tuple(newHand), state[1], tuple(newRemaining))
                state = newState
                continue

            tiles = self.convertToTiles(state)
            print(f"Current hand: {tiles}, at turn {currentTurn}, link: https://tenhou.net/2/?p={tiles}p")
            print(f"Available actions: {actions}")

            if state not in self.pi:
                raise Exception("Pi does not contain this state!")
            optimalAction = self.pi[state]
            print(f'Optimal action: {optimalAction}')

            yourAction = ''
            if "Win" in actions:
                yourAction = "Win"
            elif len(actions) == 1:
                yourAction = actions[0]
            while yourAction not in actions:
                yourAction = input('Please choose your action [Enter for optimal]: ')
                if yourAction == '':
                    yourAction = optimalAction

            if yourAction.startswith('Discard'):
                discardTile = int(yourAction[-1])
                print(f"You discarded {discardTile}")
                newState = self.mdp.getDiscardState(state, discardTile)
                totalReward += newState[2]
                state = newState[0]
                currentTurn += 1
            elif yourAction == 'Giveup':
                print(f"You gave up!")
                newState = (None, None, None)
                state = newState
                totalReward -= self.giveUpPenalty
            elif yourAction == 'Win':
                print(f"You win!")
                newState = (None, None, None)
                state = newState
                totalReward += self.winReward

        print(f"Your final score: {totalReward}")

import util, math, random
from collections import defaultdict
from util import ValueIteration

class MahjongMDP(util.MDP):
    def __init__(self, winReward, maximumTurn, groupNumber, turnPenalty, giveUpPenalty,
        simpleVersion = False):
        self.winReward = winReward
        self.maximumTurn = maximumTurn
        self.groupNumber = groupNumber
        self.turnPenalty = turnPenalty
        if not turnPenalty:
            raise Exception("Should have at least one turn penalty")
        self.giveUpPenalty = giveUpPenalty
        self.target = 2 + groupNumber * 3
        self.simpleVersion = simpleVersion

    def hasWonWithoutPair(self, hand, i):
        if i == 9:
            return True
        if hand[i] == 0:
            return self.hasWonWithoutPair(hand, i + 1)
        if i <= 6 and hand[i + 1] > 0 and hand[i + 2] > 0:
            hand[i] -= 1
            hand[i + 1] -= 1
            hand[i + 2] -= 1
            if self.hasWonWithoutPair(hand, i):
                return True
            hand[i] += 1
            hand[i + 1] += 1
            hand[i + 2] += 1
        if hand[i] >= 3:
            hand[i] -= 3
            if self.hasWonWithoutPair(hand, i):
                return True
            hand[i] += 3
        return False

    def hasWon(self, hand):
        newHand = list(hand)
        for i in range(9):
            if newHand[i] < 2:
                continue
            newHand[i] -= 2
            if self.hasWonWithoutPair(newHand, 0):
                return True
            newHand[i] += 2
        return False

    def startState(self):
        hand = tuple([0] * 9)
        remaining = tuple([4] * 9)
        return (hand, 0, remaining)

    def customState(self):
        customHand = ''
        while True:
            customHand = input("Please provide your random hand: ")
            print(customHand)
            customHand = customHand.strip()
            if len(customHand) != self.target:
                continue
            hand = [0] * 9
            remaining = [4] * 9
            ok = True
            for c in customHand:
                if '1' <= c <= '9':
                    tileIndex = int(c) - 1
                    hand[tileIndex] += 1
                    remaining[tileIndex] -= 1
                    if hand[int(c) - 1] > 4:
                        ok = False
                else:
                    ok = False
            if not ok:
                continue
            return (tuple(hand), 0, tuple(remaining))
        return None


    def getRandomTile(self, state):
        tiles = []
        for i in range(9):
            for j in range(state[2][i]):
                tiles.append(i)
        return random.choice(tiles)

    def actions(self, state):
        hand, turnNumber, remaining = state
        if turnNumber is None:
            return ['Giveup']
        totalCount = sum(hand)
        if totalCount < self.target:
            totalRemaining = sum(remaining)
            if totalRemaining == 0:
                return ['Giveup']
            else:
                return ['Draw']
        if self.hasWon(hand):
            return ['Win']
        actions = ['Giveup']
        if turnNumber < self.maximumTurn:
            for i in range(9):
                if hand[i] > 0:
                    actions.append(f'Discard{i + 1}')
        return actions

    def getDiscardState(self, state, discardTile):
        hand, turnNumber, remaining = state
        newHand = list(hand)
        newHand[discardTile - 1] -= 1
        newRemaining = list(remaining)
        newTurn = turnNumber + 1
        if self.simpleVersion:
            newRemaining[discardTile - 1] += 1
            newTurn = turnNumber

        newState = (tuple(newHand), newTurn, tuple(newRemaining))
        actualPenalty = -self.turnPenalty[-1]
        if turnNumber < len(self.turnPenalty):
            actualPenalty = -self.turnPenalty[turnNumber]
        return (newState, 1, actualPenalty)


    def succAndProbReward(self, state, action):
        newStates = []
        hand, turnNumber, remaining = state
        if turnNumber is None:
            return []
        if action == 'Draw':
            totalRemaining = sum(remaining)
            for i in range(9):
                if remaining[i] > 0:
                    p = remaining[i] / totalRemaining
                    newRemaining = list(remaining)
                    newRemaining[i] -= 1
                    newHand = list(hand)
                    newHand[i] += 1
                    newState = (tuple(newHand), turnNumber, tuple(newRemaining))
                    newStates.append((newState, p, 0))
            return newStates
        elif action == 'Giveup':
            return [((None, None, None), 1, -self.giveUpPenalty)]
        elif action == 'Win':
            return [((None, None, None), 1, self.winReward)]
        discardTile = int(action[7])
        newState = self.getDiscardState(state, discardTile)
        
        return [newState]

    def discount(self):
        return 1

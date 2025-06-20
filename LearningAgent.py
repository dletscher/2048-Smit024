import pickle
import random
import time
from Game2048 import *

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)
        # Initialize value table
        self._valueTable = {}
        for a in range(16):
            for b in range(16):
                for c in range(16):
                    for d in range(16):
                        self._valueTable[(a, b, c, d)] = random.uniform(0, 1)

        self._learningRate = 0.001
        self._discountFactor = 0.99

    def loadData(self, filename):
        print('Loading data')
        with open(filename, 'rb') as dataFile:
            self._valueTable = pickle.load(dataFile)

    def saveData(self, filename):
        print('Saving data...')
        with open(filename, 'wb') as dataFile:
            pickle.dump(self._valueTable, dataFile)

    def value(self, board):
        # Sum values of all 4 rotations
        v = 0.0
        for turns in range(4):
            g = board.rotate(turns)
            key = tuple(g._board[:4])
            v += self._valueTable.get(key, 0.0)
        return v

    def findMove(self, board):
        bestValue = float('-inf')
        bestMove = None
        for a in board.actions():
            v = 0.0
            for (g, p) in board.possibleResults(a):
                v += p * self.value(g)
            if v > bestValue:
                bestValue = v
                bestMove = a
        self.setMove(bestMove)

    def train(self, repetitions):
        for trial in range(repetitions):
            print(f'Simulating game number {trial + 1} of {repetitions}')
            state = Game2048()
            state.randomize()
            while not state.gameOver():
                self._startTime = time.time()
                self.findMove(state)
                move = self.getMove()
                oldState = state
                state, reward = state.result(move)

                # TD update
                update = self._learningRate * (
                    reward + self._discountFactor * self.value(state) - self.value(oldState)
                )

                for turns in range(4):
                    rotated = oldState.rotate(turns)
                    key = tuple(rotated._board[:4])
                    self._valueTable[key] = self._valueTable.get(key, 0.0) + update

# Only run training if this file is executed directly
if __name__ == '__main__':
    agent = Player(1)
    agent.loadData('MyData')
    agent.train(10000)
    agent.saveData('MyData')

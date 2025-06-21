
from Game2048 import *
import random
import math

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)

    def findMove(self, board):
        moves = board.actions()
        moveScores = {}
        for m in moves:
            sim, _ = board.result(m)
            score = self.eval(sim)
            moveScores[m] = score
        
        best = None
        highest = float('-inf')
        for m in moveScores:
            if moveScores[m] > highest:
                highest = moveScores[m]
                best = m

        self.setMove(best)

    def eval(self, b):
        # count empty spots
        empties = 0
        for i in b._board:
            if i == 0:
                empties += 1

        maxVal = max(b._board)

        # smoothness measure (just rough diff)
        smooth = 0
        for i in range(4):
            for j in range(3):
                smooth -= abs(b.getTile(i,j) - b.getTile(i,j+1))
        for j in range(4):
            for i in range(3):
                smooth -= abs(b.getTile(i,j) - b.getTile(i+1,j))

        # try to keep highest in a corner
        corners = [b.getTile(0,0), b.getTile(0,3), b.getTile(3,0), b.getTile(3,3)]
        cornerBonus = 0
        if maxVal in corners:
            cornerBonus = 1

        # simple directional flow bonus (monotonicity-ish)
        rowMono = 0
        colMono = 0
        for r in range(4):
            for c in range(3):
                if b.getTile(r,c) > b.getTile(r,c+1):
                    rowMono += 1
        for c in range(4):
            for r in range(3):
                if b.getTile(r,c) > b.getTile(r+1,c):
                    colMono += 1

        return 85 * empties + smooth + maxVal + (rowMono + colMono)*2 + cornerBonus * 1500

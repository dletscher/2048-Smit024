from Game2048 import *
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
        #for empty spots
        empties = sum(1 for i in b._board if i == 0)

        maxVal = max(b._board)

        smooth = 0
        for i in range(4):
            for j in range(3):
                smooth -= abs(b.getTile(i, j) - b.getTile(i, j + 1))
        for j in range(4):
            for i in range(3):
                smooth -= abs(b.getTile(i, j) - b.getTile(i + 1, j))

        #corner for max tile 
        corners = [b.getTile(0, 0), b.getTile(0, 3), b.getTile(3, 0), b.getTile(3, 3)]
        cornerBonus = 1 if maxVal in corners else 0

        #direction
        rowMono = sum(1 for r in range(4) for c in range(3) if b.getTile(r, c) > b.getTile(r, c + 1))
        colMono = sum(1 for c in range(4) for r in range(3) if b.getTile(r, c) > b.getTile(r + 1, c))

        #new weights
        return (
            100 * empties +            
            1.8 * smooth +             
            0.5 * maxVal +             
            3.0 * (rowMono + colMono) + 
            2000 * cornerBonus         
        )

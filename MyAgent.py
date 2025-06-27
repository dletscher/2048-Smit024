from Game2048 import *
import math

class Player(BasePlayer):
    def __init__(self, timeLimit):
        BasePlayer.__init__(self, timeLimit)
        self.maxDepth = 3

    #for best move
    def findMove(self, board):
        bestMove = None
        bestScore = float('-inf')
        depth = self.maxDepth

        for move in board.actions():
            nextBoard, _ = board.result(move)
            score = self.expectimax(nextBoard, depth - 1, isMax=False)
            if score is not None and score > bestScore:
                bestScore = score
                bestMove = move

        if bestMove is None:
            actions = board.actions()
            if actions:
                bestMove = actions[0]

        self.setMove(bestMove)

    #expectimax logic
    def expectimax(self, board, depth, isMax):
        if depth == 0 or board.gameOver():
            return self.eval(board)

        if isMax:
            best = float('-inf')
            for move in board.actions():
                nextBoard, _ = board.result(move)
                val = self.expectimax(nextBoard, depth - 1, isMax=False)
                if val is None:
                    continue
                best = max(best, val)
            return best
        else:
            total = 0
            count = 0
            for (tile, val) in board.possibleTiles():
                prob = 0.9 if val == 1 else 0.1
                nextBoard = board.addTile(tile, val)
                valScore = self.expectimax(nextBoard, depth - 1, isMax=True)
                if valScore is not None:
                    total += prob * valScore
                    count += 1
            return total if count > 0 else self.eval(board)

    def eval(self, b):
        tiles = b._board
        empties = tiles.count(0)
        maxVal = max(tiles)

        #weight logic 
        grad = [65536, 32768, 16384, 8192,
                512, 1024, 2048, 4096,
                256, 128, 64, 32,
                2, 4, 8, 16]
        gradScore = sum(tiles[i] * grad[i] for i in range(16))

        #Smoothnes
        smooth = 0
        for r in range(4):
            for c in range(3):
                a, b2 = b.getTile(r, c), b.getTile(r, c + 1)
                if a and b2:
                    smooth -= abs(math.log2(a) - math.log2(b2))
        for c in range(4):
            for r in range(3):
                a, b2 = b.getTile(r, c), b.getTile(r + 1, c)
                if a and b2:
                    smooth -= abs(math.log2(a) - math.log2(b2))

        #direction for merging more tiles
        mono = 0
        for r in range(4):
            for c in range(3):
                if b.getTile(r, c) >= b.getTile(r, c + 1):
                    mono += 1
        for c in range(4):
            for r in range(3):
                if b.getTile(r, c) >= b.getTile(r + 1, c):
                    mono += 1

        #center tiles 
        centerPenalty = -0.45 * sum(b.getTile(r, c) for r in (1, 2) for c in (1, 2))

        return (
            210 * empties +
            2.8 * smooth +
            6.5 * mono +
            0.025 * gradScore +
            centerPenalty
        )

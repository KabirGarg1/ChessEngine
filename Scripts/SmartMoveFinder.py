import random

pieceValue = {"K":1000, "Q":9, "B":3.1, "R":5, "N":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def findBestMove(gs,validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    bestPlayerMove = None
    oppMinMaxScore = CHECKMATE
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        oppMaxScore = -CHECKMATE
        for oppMove in oppMoves:
            gs.makeMove(oppMove)
            if gs.CheckMate:
                score = -turnMultiplier*CHECKMATE
            elif gs.StaleMate:
                score = 0
            else:
                score = -turnMultiplier*scoreAndMaterialCount(gs.board)
            if score>oppMaxScore: #Negative is best or black
                oppMaxScore = score
            gs.undoMove()

        if oppMaxScore<oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove

        gs.undoMove()
    return bestPlayerMove

def scoreAndMaterialCount(board):
    black_Material = 0
    white_Material = 0
    score=0
    for r in range(8):
        for c in range(8):
            if board[r][c][0] == "w":
                white_Material += pieceValue[board[r][c][1]]
            elif board[r][c][0] == "b":
                black_Material += pieceValue[board[r][c][1]]
    score = white_Material - black_Material
    return score
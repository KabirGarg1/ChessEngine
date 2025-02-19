import random

pieceValue = {"K":1000, "Q":9, "B":3.1, "R":5, "N":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
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

def bestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMinMax(gs,validMoves,DEPTH,gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs,validMoves,depth,whiteToMove):
    global nextMove
    if depth == 0:
        return scoreAndMaterialCount(gs)

    turnMultiplier = -1 if whiteToMove else 1
    isNextWhiteMove =  False if whiteToMove else True

    maxScore = turnMultiplier*CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextValidMoves = gs.getValidMoves()
        score = findMoveMinMax(gs,nextValidMoves,depth-1,isNextWhiteMove)
        if (whiteToMove and score>maxScore) or (not whiteToMove and score<maxScore):
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def scoreAndMaterialCount(gs):
    if gs.CheckMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.StaleMate:
        return STALEMATE
    
    black_Material = 0
    white_Material = 0
    score=0
    for r in range(8):
        for c in range(8):
            if gs.board[r][c][0] == "w":
                white_Material += pieceValue[gs.board[r][c][1]]
            elif gs.board[r][c][0] == "b":
                black_Material += pieceValue[gs.board[r][c][1]]
    score = white_Material - black_Material
    return score
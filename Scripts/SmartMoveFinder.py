import random

# Pawn table: Encourages advancement and central control.
WHITE_PAWN_TABLE = [
    [2, 3, 4, 5, 5, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [-1, 0, 1, 2, 2, 1, 0, -1],
    [-1, 0, 1, 2, 2, 1, 0, -1],
    [-1, -1, 0, 1, 1, 0, -1, -1],
    [-2, -1, -1, 0, 0, -1, -1, -2],
    [-2, -2, -2, -2, -2, -2, -2, -2]
]

BLACK_PAWN_TABLE = [
    [-2, -2, -2, -2, -2, -2, -2, -2],
    [-2, -1, -1, 0, 0, -1, -1, -2],
    [-1, -1, 0, 1, 1, 0, -1, -1],
    [-1, 0, 1, 2, 2, 1, 0, -1],
    [-1, 0, 1, 2, 2, 1, 0, -1],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 5, 5, 4, 3, 2]
]

# Knight table: Central squares are more attractive.
KNIGHT_TABLE = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1,  0,  1,  1,  1,  1,  0, -1],
    [-1,  1,  2,  3,  3,  2,  1, -1],
    [-1,  1,  3,  4,  4,  3,  1, -1],
    [-1,  1,  3,  4,  4,  3,  1, -1],
    [-1,  1,  2,  3,  3,  2,  1, -1],
    [-1,  0,  1,  1,  1,  1,  0, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

# Bishop table: Slightly lower values than knights.
BISHOP_TABLE = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1,  0,  1,  1,  1,  1,  0, -1],
    [-1,  1,  2,  2,  2,  2,  1, -1],
    [-1,  1,  2,  3,  3,  2,  1, -1],
    [-1,  1,  2,  3,  3,  2,  1, -1],
    [-1,  1,  2,  2,  2,  2,  1, -1],
    [-1,  0,  1,  1,  1,  1,  0, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

# Rook table: Encourages open file usage.
ROOK_TABLE = [
    [-2, -1, -1,  0,  0, -1, -1, -2],
    [-1,  0,  0,  1,  1,  0,  0, -1],
    [-1,  0,  0,  1,  1,  0,  0, -1],
    [ 0,  1,  1,  2,  2,  1,  1,  0],
    [ 0,  1,  1,  2,  2,  1,  1,  0],
    [-1,  0,  0,  1,  1,  0,  0, -1],
    [-1,  0,  0,  1,  1,  0,  0, -1],
    [-2, -1, -1,  0,  0, -1, -1, -2]
]

# Queen table: Combines elements of both rook and bishop.
QUEEN_TABLE = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1,  0,  0,  0,  0,  0,  0, -1],
    [-1,  0,  1,  1,  1,  1,  0, -1],
    [-1,  0,  1,  2,  2,  1,  0, -1],
    [-1,  0,  1,  2,  2,  1,  0, -1],
    [-1,  0,  1,  1,  1,  1,  0, -1],
    [-1,  0,  0,  0,  0,  0,  0, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

# King table: Favors safer, more centralized positions.
KING_TABLE = [
    [-2, -2, -2, -2, -2, -2, -2, -2],
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-2, -1,  0,  0,  0,  0, -1, -2],
    [-2, -1,  0,  1,  1,  0, -1, -2],
    [-2, -1,  0,  1,  1,  0, -1, -2],
    [-2, -1,  0,  0,  0,  0, -1, -2],
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-2, -2, -2, -2, -2, -2, -2, -2]
]



piecePositionScores = {"wp":WHITE_PAWN_TABLE,"bp":BLACK_PAWN_TABLE,"K":KING_TABLE,"Q":QUEEN_TABLE,"N":KNIGHT_TABLE,"B":BISHOP_TABLE,"R":ROOK_TABLE}
pieceValue = {"K":1000, "Q":9, "B":3.1, "R":5, "N":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
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
    turnMultiplier = 1 if gs.whiteToMove else -1
    findMoveMinMax(gs,validMoves,DEPTH,turnMultiplier,-CHECKMATE,CHECKMATE)
    return nextMove

def findMoveMinMax(gs,validMoves,depth,turnMultiplier,alpha,beta): #ALPHA IS CURRENT MAX AND BETA IS CURRENT MINIMUM SCORE
    global nextMove

    if depth == 0:
        return turnMultiplier*scoreAndMaterialCount(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextValidMoves = gs.getValidMoves() 
        score = -findMoveMinMax(gs,nextValidMoves,depth-1,-turnMultiplier,-beta,-alpha)
        if score>maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        alpha = max(alpha,maxScore)
        if alpha>=beta:
            break
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
            if gs.board[r][c] != "--":
                piece = gs.board[r][c]
                if piece[1] == "p":
                    piecePositionScore = piecePositionScores[piece][r][c]*0.1
                else:
                    piecePositionScore = piecePositionScores[piece[1]][r][c]*0.3
                if gs.inCheck:
                    piecePositionScore+=0.3
                if piece[0] == "w":
                    white_Material += pieceValue[piece[1]] + piecePositionScore
                elif piece[0] == "b":
                    black_Material += pieceValue[piece[1]] + piecePositionScore
    score = white_Material - black_Material
    return score
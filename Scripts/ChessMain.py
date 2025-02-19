import pygame as py
import ChessEngine
import SmartMoveFinder

WIDTH = HEIGHT = 512
DIMENSION= 8
SQ_SIZE = WIDTH//DIMENSION
IMAGES = {}
MAX_FPS = 15

def loadImages():
    pieces = ["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = py.transform.scale(py.image.load("pieces_images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))

def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = py.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)#transperency value
            s.fill(py.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(py.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(SQ_SIZE*move.endCol,SQ_SIZE*move.endRow))


def drawBoard_and_Pieces(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    global colors
    colors=[py.Color("white"),py.Color("Brown")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            py.draw.rect(screen,color,py.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c] != "--":
                screen.blit(IMAGES[board[r][c]],py.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def animateMove(move,screen,board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)

    # erase the piece moved from its ending square
    color = colors[(move.endCol + move.endRow)%2]
    endSquare = py.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
    py.draw.rect(screen,color,endSquare)
    #draw moving pieces
    if move.pieceCaptured != "--":
        screen.blit(IMAGES[move.pieceCaptured],endSquare)
    screen.blit(IMAGES[move.pieceMoved],py.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    py.display.flip()
    clock.tick(60)

def main():
    py.init
    screen = py.display.set_mode((WIDTH,HEIGHT))
    clock = py.time.Clock()
    gs = ChessEngine.GameState()
    loadImages()

    validMoves = gs.getValidMoves()
    moveMade = False

    sqSelected=()
    playerClicks=[]
    playerOne = True #Player White
    playerTwo = False #Playr Black
    running = True
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                if humanTurn:
                    location = py.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                

            elif event.type == py.MOUSEBUTTONUP:
                if humanTurn:
                    location = py.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE

                if playerClicks[0]==(row,col):
                    sqSelected=()
                    playerClicks=[]
                    continue

                sqSelected=(row,col)
                playerClicks.append(sqSelected)
                move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)

                for i in range(len(validMoves)):
                    if move == validMoves[i]:
                        gs.makeMove(validMoves[i])
                        moveMade = True
                sqSelected=()
                playerClicks=[]


            elif event.type == py.KEYDOWN:
                if event.key == py.K_z:
                  gs.undoMove()

        #AI move Finder Logic
        if not humanTurn:
            AImove = SmartMoveFinder.bestMoveMinMax(gs,validMoves) if not None else SmartMoveFinder.findRandomMove(validMoves)
            
            gs.makeMove(AImove)
            moveMade = True

        if moveMade:
            #animateMove(gs.moveLog[-1],screen,gs.board,clock)
            moveMade == False
            validMoves = gs.getValidMoves()
        drawBoard_and_Pieces(screen,gs,validMoves,sqSelected)
        clock.tick(MAX_FPS)
        py.display.flip()


if __name__ == "__main__":
    main()

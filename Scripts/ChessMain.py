import pygame as py
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION= 8
SQ_SIZE = WIDTH//DIMENSION
IMAGES = {}
MAX_FPS = 15

def loadImages():
    pieces = ["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = py.transform.scale(py.image.load("pieces_images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))

def drawBoard_and_Pieces(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
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
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                sqSelected=(row,col)
                playerClicks.append(sqSelected)
                

            elif event.type == py.MOUSEBUTTONUP:
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
        if moveMade:
            moveMade == False
            validMoves = gs.getValidMoves()
        drawBoard_and_Pieces(screen,gs)
        clock.tick(MAX_FPS)
        py.display.flip()

if __name__ == "__main__":
    main()

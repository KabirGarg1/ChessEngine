class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.getMoves = {"p":self.getPawnMove,"R":self.getRookMoves,"B":self.getBishopMoves,
                         "Q":self.getQueenMoves,"N":self.getKnightMoves,"K":self.getKingMoves}
        
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins=[]
        self.checks=[]


    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove
        self.moveLog.append(move)

    def undoMove(self):
        if len(self.moveLog)!=0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            sameColor = "w"
            startRow,startCol = self.whiteKingLocation[0],self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            sameColor = "b"
            startRow,startCol = self.blackKingLocation[0],self.blackKingLocation[1]
        
        directions = ((-1,0),(1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j  in range(len(directions)):
            direction = directions[j]
            possiblePin=()

            for distance in range(1,8):
                endRow = startRow + direction[0]*distance
                endCol = startCol + direction[1]*distance

                if 0<=endRow<=7 and 0<=endCol<=7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == sameColor:
                        if len(possiblePin)==0:
                            possiblePin = (endRow,endCol,direction[0],direction[1])
                        else:
                            possiblePin = ()
                            break
                    elif endPiece[0] == enemyColor:
                        piece_type = endPiece[1]

                        if((0<=j<=3 and piece_type=="R") or (4<=j<=7 and piece_type == "B") or (piece_type=="Q") or (distance == 1 and piece_type=="K") or 
                           (distance==1 and piece_type=="p" and ((enemyColor=="w" and 4<=j<=5) or (enemyColor=="b" and 6<=j<=7)))):
                            if len(possiblePin)==0:
                                inCheck=True
                                checks.append((endRow,endCol,direction[0],direction[1]))
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break

        #Checking checks seperatly for knight..knight cant apply pins cuz it jumps over pieces
        knight_directions = ((-2,-1),(-2,1)(-1,-2),(-1,2)(1,-2),(1,2),(2,-1),(2,1))
        for direction in knight_directions:
            endRow = startRow + direction[0]
            endCol = startCol + direction[1]

            piece = self.board[endRow][endCol]
            if piece[0] == enemyColor and piece[1] == "N":
                inCheck = True
                checks.append((endRow,endCol,direction[0],direction[1]))
        return inCheck,pins,checks

    def getValidMoves(self):
        moves=[]
        self.inCheck,self.pins,self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow,kingCol = self.whiteKingLocation[0],self.whiteKingLocation[1]
        else:
            kingRow,kingCol = self.blackKingLocation[0],self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.allPossibleMoves()
                check = self.checks[0]
                checkRow,checkCol = check[0],check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == "N":
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i,kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(moves) - 1,-1,-1):
                    if moves[i].pieceMoved[1] != "K" and not (moves[i].endRow,moves[i].endCol) in validSquares:
                        moves.remove(moves[i])
            else: #Double check can be escaped ONLY by moving king
                self.getKingMoves(kingRow,kingCol,moves)
        else:
            moves = self.allPossibleMoves

        return moves
    
    def allPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                if (color=="w" and self.whiteToMove) or (color=="b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.getMoves[piece](r,c,moves)
        return moves
    
    def getKingMoves(self,r,c,moves):
        sameColor = "w" if self.whiteToMove else "b"
        king_moves = [(1,-1),(1,0),(1,1),(0,-1),(0,1),(-1,-1),(-1,0),(-1,1)]
        
        for king_move in king_moves:
            endRow = r + king_move[0]
            endCol = c + king_move[1]
            if 0<=endRow<=7 and 0<=endCol<=7 and self.board[endRow][endCol][0] != sameColor:
                moves.append(Move((r,c),(endRow,endCol),self.board))

        return moves

    def getKnightMoves(self,r,c,moves):
        sameColor = "w" if self.whiteToMove else "b"
        knight_moves = [(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
        
        for knight_move in knight_moves:
            endRow = r + knight_move[0]
            endCol = c + knight_move[1]
            if 0<=endRow<=7 and 0<=endCol<=7 and self.board[endRow][endCol][0] != sameColor:
                moves.append(Move((r,c),(endRow,endCol),self.board))

        return moves
    
    def getQueenMoves(self,r,c,moves):
        return self.getBishopMoves(r,c,moves) + self.getRookMoves(r,c,moves)

    def getRookMoves(self,r,c,moves):
        enemyColor = "b" if self.whiteToMove else "w"

        for i in range(r+1,8):
            if self.board[i][c] == "--": moves.append(Move((r,c),(i,c),self.board))
            elif self.board[i][c][0] == enemyColor:
                moves.append(Move((r,c),(i,c),self.board))
                break
            else: break

        for i in range(r-1,-1,-1):
            if self.board[i][c] == "--": moves.append(Move((r,c),(i,c),self.board))
            elif self.board[i][c][0] == enemyColor:
                moves.append(Move((r,c),(i,c),self.board))
                break
            else: break

        for j in range(c+1,8):
            if self.board[r][j] == "--": moves.append(Move((r,c),(r,j),self.board))
            elif self.board[r][j][0] == enemyColor:
                moves.append(Move((r,c),(r,j),self.board))
                break
            else: break

        for j in range(c-1,-1,-1):
            if self.board[r][j] == "--": moves.append(Move((r,c),(r,j),self.board))
            elif self.board[r][j][0] == enemyColor:
                moves.append(Move((r,c),(r,j),self.board))
                break
            else: break

        return moves
    
    def getBishopMoves(self,r,c,moves):
        enemyColor = "b" if self.whiteToMove else "w"

        i,j = r+1,c+1
        while i<=7 and j<=7:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0] == enemyColor:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else: break
            i+=1
            j+=1

        i,j = r-1,c-1
        while i>=0 and j>=0:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0] == enemyColor:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else: break
            i-=1
            j-=1

        i,j = r+1,c-1
        while i<=7 and j>=0:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0] == enemyColor:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else: break
            i+=1
            j-=1

        i,j = r-1,c+1
        while i>=0 and j<=7:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0] == enemyColor:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else: break
            i-=1
            j+=1
        
        return moves

    def getPawnMove(self,r,c,moves):
        def getBlackPawnMove():
            if r<6:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r==1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c),self.board))

                if c>0 and self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))

                if c<7 and self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
            return moves
    
        def getWhitePawnMove():
            if r>1:
                if self.board[r-1][c] == "--":
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),self.board))

                if c>0 and self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1),self.board))

                if c<7 and self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
            return moves
        
        if self.whiteToMove:
            return getWhitePawnMove()
        return getBlackPawnMove()



class Move():
    rowToRank = {0:"8",1:"7",2:"6",3:"5",4:"4",5:"3",6:"2",7:"1"}
    colToFiles = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}

    #RankToRow = {v:k for k,v in rowToRank.items()}
    #FilesToCol = {v:k for k,v in colToFiles.items()}

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID =  self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    def __eq__(self, value):
        if isinstance(value,Move):
            return self.moveID == value.moveID
        return False

    def chessNotations(self):
        return self.colToFiles[self.startCol] + self.rowToRank[self.startRow] + self.colToFiles[self.endCol] + self.rowToRank[self.endRow]

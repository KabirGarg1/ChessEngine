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
        self.getMoves = {"p":self.getPawnMove,"R":self.getRookMoves,"B":self.getBishopMoves}

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

    def getValidMoves(self):
        return self.allPossibleMoves()
    
    def allPossibleMoves(self):
        moves=[]
        p = ["p","B","R"]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                if (color=="w" and self.whiteToMove) or (color=="b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece in p:
                      self.getMoves[piece](r,c,moves)
        return moves
    
    def getRookMoves(self,r,c,moves):
        for i in range(r+1,8):
            if self.board[i][c] == "--": moves.append(Move((r,c),(i,c),self.board))
            elif (self.whiteToMove and self.board[i][c][0] == "b") or (not self.whiteToMove and self.board[i][c][0] == "w"):
                moves.append(Move((r,c),(i,c),self.board))
                break
            else: break

        for i in range(r-1,-1,-1):
            if self.board[i][c] == "--": moves.append(Move((r,c),(i,c),self.board))
            elif (self.whiteToMove and self.board[i][c][0] == "b") or (not self.whiteToMove and self.board[i][c][0] == "w"):
                moves.append(Move((r,c),(i,c),self.board))
            else: break

        for j in range(c+1,8):
            if self.board[r][j] == "--": moves.append(Move((r,c),(r,j),self.board))
            elif (self.whiteToMove and self.board[r][j][0] == "b") or (not self.whiteToMove and self.board[r][j][0] == "w"):
                moves.append(Move((r,c),(r,j),self.board))
            else: break

        for j in range(c-1,-1,-1):
            if self.board[r][j] == "--": moves.append(Move((r,c),(r,j),self.board))
            elif (self.whiteToMove and self.board[r][j][0] == "b") or (not self.whiteToMove and self.board[r][j][0] == "w"):
                moves.append(Move((r,c),(r,j),self.board))
            else: break

        return moves
    
    def getBishopMoves(self,r,c,moves):
        i,j = r,c
        while i<=7 and j<=7:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif (self.whiteToMove and self.board[i][j][0] == "b") or (not self.whiteToMove and self.board[i][j][0] == "w"):
                moves.append(Move((r,c),(i,j),self.board))
            else: break
            i+=1
            j+=1

        i,j = r,c
        while i>=0 and j>=0:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif (self.whiteToMove and self.board[i][j][0] == "b") or (not self.whiteToMove and self.board[i][j][0] == "w"):
                moves.append(Move((r,c),(i,j),self.board))
            else: break
            i-=1
            j-=1

        i,j = r,c
        while i<=7 and j>=0:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif (self.whiteToMove and self.board[i][j][0] == "b") or (not self.whiteToMove and self.board[i][j][0] == "w"):
                moves.append(Move((r,c),(i,j),self.board))
            else: break
            i+=1
            j-=1

        i,j = r,c
        while i>=0 and j<=7:
            if self.board[i][j] == "--": moves.append(Move((r,c),(i,j),self.board))
            elif (self.whiteToMove and self.board[i][j][0] == "b") or (not self.whiteToMove and self.board[i][j][0] == "w"):
                moves.append(Move((r,c),(i,j),self.board))
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

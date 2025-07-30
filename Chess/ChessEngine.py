'''
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves at the current state. In addition, it will keep a move log.
'''

class GameState():
    def __init__(self):
        # 8x8 board, 2d list, 2 characters per square. Notation: crystal clear :)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self, move):
        '''Takes a move and execute it, rule's exceptions: castling, en passant, pawn promotion'''
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later if needed
        self.whiteToMove = not self.whiteToMove # switch turns

    def undoMove(self):
        '''Undo the last move made'''
        if len(self.moveLog) != 0:
            self.whiteToMove = not self.whiteToMove
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured

    def getValidMoves(self):
        '''All moves considering checks'''
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        '''All moves without considering checks'''
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == "w" and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    self.moveFunctions[piece](row, column, moves)
        return moves


    def getPawnMoves(self, row, column, moves):
        '''Get all the pawn moves for the pawn located at row, column and add this move to the list'''
        if self.whiteToMove: # white pawn move
            if self.board[row-1][column] == '--': # advancing 1 square
                moves.append(Move((row, column), (row-1, column), self.board))
                if row == 6 and self.board[row-2][column] == "--":
                    moves.append(Move((row, column), (row-2, column), self.board))

            if column - 1 >= 0: # left captures
                if self.board[row-1][column-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, column), (row-1, column-1), self.board))
            if column + 1 <= 7: # right captures
                if self.board[row-1][column+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, column), (row-1, column+1), self.board))

        else:
            if self.board[row+1][column] == '--': # advancing 1 square
                moves.append(Move((row, column), (row+1, column), self.board))
                if row == 1 and self.board[row+2][column] == "--":
                    moves.append(Move((row, column), (row+2, column), self.board))

            if column - 1 >= 0: # left captures
                if self.board[row+1][column-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, column), (row+1, column-1), self.board))
            if column + 1 <= 7: # right captures
                if self.board[row+1][column+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, column), (row+1, column+1), self.board))
            

    def getRookMoves(self, row, column, moves):
        '''Get all the rook moves for the rook located at row, column and add this move to the list'''
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: 
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:
                        break

    
    def getKnightMoves(self, row, column, moves):
        '''Get all the rook moves for the knight located at row, column and add this move to the list'''
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:   
            enemyColor = "w"
        for m in knightMoves:
            endRow = row + m[0]
            endCol = column + m[1]
            print(endRow, endCol)
            if 0 <= endRow < 8 and 0 <= endCol < 8: 
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == '-' or endPiece[0] == enemyColor:
                    print("Hola")
                    moves.append(Move((row, column), (endRow, endCol), self.board))



    def getBishopMoves(self, row, column, moves):
        '''Get all the rook moves for the bishop located at row, column and add this move to the list'''
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:   
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: 
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:
                        break

    def getQueenMoves(self, row, column, moves):
        '''Get all the rook moves for the queen located at row, column and add this move to the list'''
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        '''Get all the rook moves for the king located at row, column and add this move to the list'''
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:   
            enemyColor = "w"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = column + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: 
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == '-' or endPiece[0] == enemyColor:
                    moves.append(Move((row, column), (endRow, endCol), self.board))

class Move():
    # maps keys to values
    # key: value
    ranks2Rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows2Ranks = {v: k for k, v in ranks2Rows.items()}
    files2Cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols2Files = {v: k for k, v in files2Cols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startColumn = startSq[1]

        self.endRow = endSq[0]
        self.endColumn = endSq[1]

        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]

        self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn 

    def __eq__(self, other):
        '''Overriding the equals method'''
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        # TODO: Adding real chess notation
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    def getRankFile(self, r, c):
        return self.cols2Files[c] + self.rows2Ranks[r]

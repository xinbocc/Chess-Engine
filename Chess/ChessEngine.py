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

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.check = False
        self.pins = []
        self.checks = []

        self.enPassantPossible = () # square where en passant capture can happen
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

        

    def makeMove(self, move):
        '''Takes a move and execute it, rule's exceptions: castling, en passant, pawn promotion'''
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later if needed
        self.whiteToMove = not self.whiteToMove # switch turns
        
        # Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endColumn)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endColumn)

        # if pawn promotion change piece
        if move.pawnPromotion:
            """ promotedPiece = input("Promote to Q, R, B, or N:")
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + promotedPiece """
            # just promote to queen:
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + "Q"
        
        # enpassant move
        if move.enPassant:
            self.board[move.startRow][move.endColumn] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:  # only on 2 square pawn advance
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startColumn)
        else:
            self.enPassantPossible = ()

        #castle moves
        if move.castle:
            if move.endColumn - move.startColumn == 2: # kingside
                self.board[move.endRow][move.endColumn - 1] = self.board[move.endRow][move.endColumn + 1] # moving R
                self.board[move.endRow][move.endColumn + 1] = '--' # empty square where R was
            else: # queenside
                self.board[move.endRow][move.endColumn + 1] = self.board[move.endRow][move.endColumn + 1] # moving R
                self.board[move.endRow][move.endColumn - 2 ] = '--' # empty 
        
        self.enPassantPossibleLog.append(self.enPassantPossible)

        # update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    def undoMove(self):
        '''Undo the last move made'''
        if len(self.moveLog) != 0:
            self.whiteToMove = not self.whiteToMove
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            # Undo the king's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startColumn)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startColumn)
            # Undo enpassant
            if move.enPassant:
                self.board[move.endRow][move.endColumn] = '--' # removes the pawn that was added in the wrong squares
                self.baord[move.startRow][move.endColumn] = move.pieceCaptured # puts the pawn back on the correct square it was captured from
                self.enPassantPossible = (move.endRow, move.endColumn) # allow an en passant to happend on the next move
            # Undo a 2 aquare pawn advance should make enPassantPossible = () again
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            # give back castle rights if move took them away
            self.castleRightsLog.pop() # remove last moves updates
            castleRights = self.castleRightsLog[-1]
            self.whiteCastleKingside = castleRights.wks
            self.blackCastleKingside = castleRights.bks
            self.whiteCastleQueenside = castleRights.wqs
            self.blackCastleQueenside = castleRights.bqs
            # undo castle
        if move.castle:
            if move.endColumn - move.startColumn == 2: # kingside
                self.board[move.endRow][move.endColumn + 1] = self.board[move.endRow][move.endColumn - 1] # moving back R
                self.board[move.endRow][move.endColumn + 1] = '--' # empty square where R was
            else: # queenside
                self.board[move.endRow][move.endColumn - 2] = self.board[move.endRow][move.endColumn + 1] # moving back R
                self.board[move.endRow][move.endColumn + 1 ] = '--' # empty 

        self.checkmate = False
        self.stalemate = False

    def updateCastleRights(self, move):
        '''Update the castle rights given the move'''
        if move.pieceCaptured == "wR":
            if move.endColumn == 0:  # left rook
                self.currentCastlingRights.wqs = False
            elif move.endColumn == 7:  # right rook
                self.currentCastlingRights.wks = False
        elif move.pieceCaptured == "bR":
            if move.endColumn == 0:  # left rook
                self.currentCastlingRights.bqs = False
            elif move.endColumn == 7:  # right rook
                self.currentCastlingRights.bks = False

        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wqs = False
            self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bqs = False
            self.currentCastlingRights.bks = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startColumn == 0:  # left rook
                    self.currentCastlingRights.wqs = False
                elif move.startColumn == 7:  # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startColumn == 0:  # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startColumn == 7:  # right rook
                    self.currentCastlingRights.bks = False


    def getValidMoves(self):
        '''All moves considering checks'''

        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)

        moves = []
        self.check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.check:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endColumn) in validSquares:
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        if len(moves) == 0:
            if self.check:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.currentCastlingRights = tempCastleRights
        return moves
    
    
    def inCheck(self):
        '''Determine if the current player is in check'''
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, row, column):
        '''Determine if the enemy can attack the square row, column'''
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endColumn == column:
                self.whiteToMove = not self.whiteToMove
                return True
        return False
    
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

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False

        if self.board[row+moveAmount][column] == "--": # 1 square move
            if not piecePinned or pinDirection == (moveAmount, 0):
                if row + moveAmount == backRow:
                    pawnPromotion = True
                moves.append(Move((row, column), (row+moveAmount, column), self.board, pawnPromotion = pawnPromotion))
                if row == startRow and self.board[row+2*moveAmount][column] == "--": # 2 square moves
                    moves.append(Move((row, column), (row+2*moveAmount, column), self.board))
        if column-1 >=0: #capture to left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[row + moveAmount][column-1][0] == enemyColor:
                    if row + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((row, column), (row+moveAmount, column-1), self.board, pawnPromotion = pawnPromotion))
                if (row + moveAmount, column - 1) == self.enPassantPossible:
                    moves.append(Move((row, column), (row+moveAmount, column-1), self.board, enPassant=True))
        if column+1 <= 7:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[row + moveAmount][column+1][0] == enemyColor:
                    if row + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((row, column), (row+moveAmount, column+1), self.board, pawnPromotion = pawnPromotion))
                if (row + moveAmount, column + 1) == self.enPassantPossible:
                    moves.append(Move((row, column), (row+moveAmount, column+1), self.board, enPassant=True))


        """previous pawn function"""

        """ if self.whiteToMove: # white pawn move
            if self.board[row-1][column] == '--': # advancing 1 square
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((row, column), (row-1, column), self.board))
                    if row == 6 and self.board[row-2][column] == "--":
                        moves.append(Move((row, column), (row-2, column), self.board))

            if column - 1 >= 0: # left captures
                if self.board[row-1][column-1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((row, column), (row-1, column-1), self.board))
            if column + 1 <= 7: # right captures
                if self.board[row-1][column+1][0] == 'b': #enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row, column), (row-1, column+1), self.board))

        else:
            if self.board[row+1][column] == '--': # advancing 1 square
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((row, column), (row+1, column), self.board))
                    if row == 1 and self.board[row+2][column] == "--":
                        moves.append(Move((row, column), (row+2, column), self.board))

            if column - 1 >= 0: # left captures
                if self.board[row+1][column-1][0] == 'w': #enemy piece to capture
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row, column), (row+1, column-1), self.board))
            if column + 1 <= 7: # right captures
                if self.board[row+1][column+1][0] == 'w': #enemy piece to capture
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row, column), (row+1, column+1), self.board)) """

    def getRookMoves(self, row, column, moves):
        '''Get all the rook moves for the rook located at row, column and add this move to the list'''
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q': # can't remove Q from pin on R moves, only remove it on B moves
                    self.pins.remove(self.pins[i])
                break
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endColumn = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):    
                        endPiece = self.board[endRow][endColumn]
                        if endPiece == "--":
                            moves.append(Move((row, column), (endRow, endColumn), self.board))
                        elif endPiece[0] == enemyColor: 
                            moves.append(Move((row, column), (endRow, endColumn), self.board))
                            break
                        else:
                            break
                else:
                    break

    
    def getKnightMoves(self, row, column, moves):
        '''Get all the rook moves for the knight located at row, column and add this move to the list'''
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        
        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        if self.whiteToMove:
            allyColor = "w"
        else:   
            allyColor = "b"
        for m in knightMoves:
            endRow = row + m[0]
            endColumn = column + m[1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece[0] != allyColor:
                        moves.append(Move((row, column), (endRow, endColumn), self.board))

    def getBishopMoves(self, row, column, moves):
        '''Get all the rook moves for the bishop located at row, column and add this move to the list'''
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:   
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endColumn = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8: 
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):        
                        endPiece = self.board[endRow][endColumn]
                        if endPiece == "--":
                            moves.append(Move((row, column), (endRow, endColumn), self.board))
                        elif endPiece[0] == enemyColor: 
                            moves.append(Move((row, column), (endRow, endColumn), self.board))
                            break
                        else:
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
            allyColor = "w"
        else:   
            allyColor = "b"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endColumn = column + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8: 
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.blackKingLocation = (endRow, endColumn)
                    else:
                        self.whiteKingLocation = (endRow, endColumn)
                    check, pins, checks = self.checkForPinsAndChecks()
                    if not check:
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                    if allyColor == 'w':
                        self.blackKingLocation = (row, column)
                    else:
                        self.whiteKingLocation = (row, column)

    def getCastleMoves(self, row, column, moves):
        '''Generate all valid castle moves for the king at (row, column) and add them to the list of moves.'''
        if self.inCheck():
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(row, column, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(row, column, moves)

    def getKingsideCastleMoves(self, row, column, moves):
        if self.board[row][column + 1] == "--" and self.board[row][column + 2] == "--":
            if not self.squareUnderAttack(row, column + 1) and not self.squareUnderAttack(row, column + 2):
                moves.append(Move((row, column), (row, column + 2), self.board, castle=True))

    def getQueensideCastleMoves(self, row, column, moves):
        if self.board[row][column - 1] == "--" and self.board[row][column - 2] == "--" and self.board[row][column - 3] == "--":
            if not self.squareUnderAttack(row, column - 1) and not self.squareUnderAttack(row, column - 2):
                moves.append(Move((row, column), (row, column - 2), self.board, castle=True))



    def checkForPinsAndChecks(self):
        pins = [] # squares where the allied pinned piece is and dir pinned from
        checks = [] # squares where the enemy is applying a check
        check = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startColumn = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startColumn = self.blackKingLocation[1]
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endColumn = startColumn + d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endColumn, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities:
                        # 1. orthogonally away from K and piece is R
                        # 2. diagonally away from K and piece is a B
                        # 3. 1 square away diagonally from K and piece is p
                        # 4. any direction and piece is Q
                        # 5. any directions 1 square away and piece is K (case for preventing illegal kings moving towards each other)
                        if (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking, so check
                                check = True
                                checks.append((endRow, endColumn, d[0], d[1]))
                                break
                            else: # piece blocking, is pinned
                                pins.append(possiblePin)
                                break
                        else: # no checks
                            break
                else:
                    break
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for m in knightMoves:
            endRow = startRow + m[0]
            endColumn = startColumn + m[1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    check = True
                    checks.append((endRow, endColumn, m[0], m[1]))
            else:
                break
        return check, pins, checks


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    # maps keys to values
    # key: value
    ranks2Rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows2Ranks = {v: k for k, v in ranks2Rows.items()}
    files2Cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols2Files = {v: k for k, v in files2Cols.items()}
    
    def __init__(self, startSq, endSq, board, enPassant = False, pawnPromotion = False, castle = False):
        self.startRow = startSq[0]
        self.startColumn = startSq[1]

        self.endRow = endSq[0]
        self.endColumn = endSq[1]

        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]

        self.enPassant = enPassant
        self.pawnPromotion = pawnPromotion
        self.castle = castle
        if enPassant:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp' # enpassant captures opposite colored pawn
        self.isCapture = self.pieceCaptured != "--"
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

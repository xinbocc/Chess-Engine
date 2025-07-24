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
        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later if needed
        self.whiteToMove = not self.whiteToMove # switch turns

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

    def getChessNotation(self):
        # TODO: Adding real chess notation
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    def getRankFile(self, r, c):
        return self.cols2Files[c] + self.rows2Ranks[r]

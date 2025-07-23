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
        
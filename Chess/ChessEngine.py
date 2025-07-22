'''
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves at the current state. In addition, it will keep a move log.
'''

class GameState():
    def __init__(self):
        self.board = []
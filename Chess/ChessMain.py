'''
This is a driver file -> It will be responsible for handling user input and displaying the current GameState object.
'''

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    ''' Loading images just one time -> global dictionary of images.'''
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    ''' The main driver for our code. This will handle user input and updating the graphics '''
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    loadImages()
    running = True
    sqSelected = () # no square is selected, keeps tracks of the last click of the user (row, column)
    playerClicks = [] # keeps tracks of player clicks [(5, 4), (6, 4)]
    while running:
        # The game
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                column = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if sqSelected == (row, column): # user clicked in same position twice -> unselect?
                    sqSelected = ()
                    playerClicks = [] 
                else:
                    sqSelected = (row, column)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    # we move
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    
                    if move in validMoves:                
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo w/ 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    '''Draws the game state'''
    drawBoard(screen) # Drawing board's squares
    # TODO: Adding piece highlighting or move suggestions 
    drawPieces(screen, gs.board) # Drawing the pieces


def drawBoard(screen):
    '''Draws the squares on the board'''
    colors = [p.Color(237, 214, 176), p.Color(184, 135, 98)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = (colors[(column+row) % 2])
            p.draw.rect(screen, color, p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    '''Draws the pieces on the board using current GameState.board'''
    for row in range (DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--': # not empty square
                screen.blit(IMAGES[piece], p.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()



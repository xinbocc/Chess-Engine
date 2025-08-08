'''
This is a driver file -> It will be responsible for handling user input and displaying the current GameState object.
'''

import pygame as p
from Chess import ChessEngine, ChessAI

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

    animate = False #flag variable for when we should animate a move

    loadImages()
    running = True
    sqSelected = () # no square is selected, keeps tracks of the last click of the user (row, column)
    playerClicks = [] # keeps tracks of player clicks [(5, 4), (6, 4)]
    gameOver = False
    playerOne = True # if a human is playing white, then this will be True. if ai is playing -> False
    playerTwo = False # same as playerOne but with black
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)


        # The game
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                        for i in range(len(validMoves)):
                            if move in validMoves:                
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo w/ 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: # reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        # ai move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')


        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    '''Highlight square selected and moves for piece selected'''
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('cyan'))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            #highlight moves from sq
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startColumn == c:
                    screen.blit(s, (move.endColumn*SQUARE_SIZE, move.endRow*SQUARE_SIZE))
                    

def drawGameState(screen, gs, validMoves, sqSelected):
    '''Draws the game state'''
    drawBoard(screen) # Drawing board's squares
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # Drawing the pieces


def drawBoard(screen):
    '''Draws the squares on the board'''
    global colors
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

def animateMove(move, screen, board, clock):
    '''Animating a move'''
    global colors
    dR = move.endRow - move.startRow
    dC = move.endColumn - move.startColumn
    framesPerSquare = 10 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startColumn + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending sq
        color = colors[(move.endRow + move.endColumn) % 2]
        endSquare = p.Rect(move.endColumn*SQUARE_SIZE, move.endRow*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece 
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Roboto", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Cyan'))
    screen.blit(textObject, textLocation.move(-2, -2))


if __name__ == "__main__":
    main()



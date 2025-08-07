import pygame
import sys
import numpy as np

# Constants
ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5

WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE  # extra row for user input
SIZE = (WIDTH, HEIGHT)

# RGB Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game Variables
board = np.zeros((ROWS, COLS))  # 0=empty, 1=Player1, 2=Player2
turn = 0
game_over = False

pygame.init()
screen = pygame.display.set_mode(SIZE)
font = pygame.font.SysFont("monospace", 75)

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE + SQUARESIZE//2, (r+1)*SQUARESIZE + SQUARESIZE//2), RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE + SQUARESIZE//2, HEIGHT - (r*SQUARESIZE + SQUARESIZE//2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE + SQUARESIZE//2, HEIGHT - (r*SQUARESIZE + SQUARESIZE//2)), RADIUS)
    pygame.display.update()

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Horizontal check
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive diagonal
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative diagonal
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False


# Main game loop
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            color = RED if turn == 0 else YELLOW
            pygame.draw.circle(screen, color, (posx, SQUARESIZE//2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

            col = event.pos[0] // SQUARESIZE

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn + 1)

                if winning_move(board, turn + 1):
                    label = font.render(f"Player {turn + 1} wins!", 1, RED if turn == 0 else YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)

                turn = (turn + 1) % 2

if game_over:
    pygame.time.wait(3000)

#!/usr/bin/env python3

import pygame
import time
from pygame.locals import *

'''
Initialize Pygame
'''
pygame.init()

'''
Set Up the Screen
'''
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Okay Chess But With a Twist😮')

'''
Define Colors
'''

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

'''
Define constants
'''
GRID_SIZE = 8
SQUARE_SIZE = min(WIDTH, HEIGHT) // GRID_SIZE

'''
Chess Board representation using 2D list
'''
board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         ['-', '-', '-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-', '-', '-'],
         ['-', '-', '-', '-', '-', '-', '-', '-'],
         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
         ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]

'''
Player turn variable definition
'''
current_player = 'WHITE'
last_move_time = time.time()

'''
Function to draw the chessboard
'''
def draw_board():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) 
            pygame.draw.rect(screen, WHITE if (x + y) & 2 == 0 else BLACK, rect)

'''
function to draw the chess pieces
'''

def draw_pieces():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            piece = board[y][x]
            if piece != '-':
                piece_image = pygame.image.load(f'pieces/black-chess-piece-pawn.png')
                piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

def switch_turns():
    global current_player
    if current_player == 'WHITE':
        current_player = 'BLACK'
    else:
        current_player = 'WHITE'

def is_legal_move(start_pos, end_pos):
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # Check if the end position is within the board bounds
    if end_x < 0 or end_x >= GRID_SIZE or end_y < 0 or end_y >= GRID_SIZE:
        return False

    # Get the piece being moved
    piece = board[start_y][start_x]

    # Check if the end position is occupied by a friendly piece
    if board[end_y][end_x] != '-' and board[end_y][end_x].isupper() == piece.isupper():
        return False

    # Implement piece-specific move validation
    if piece == 'P':  # Pawn
        # Pawn moves forward one square
        if start_x == end_x and ((start_y == 1 and end_y == 3) or (start_y == 6 and end_y == 4)):
            return True
        # Pawn captures diagonally
        if abs(start_x - end_x) == 1 and end_y - start_y == 1 and board[end_y][end_x] != '-':
            return True
    elif piece == 'R':  # Rook
        # Rook moves horizontally or vertically
        if start_x == end_x or start_y == end_y:
            # Check if there are any pieces blocking the path
            if start_x == end_x:
                step = 1 if start_y < end_y else -1
                for y in range(start_y + step, end_y, step):
                    if board[y][start_x] != '-':
                        return False
            else:  # start_y == end_y
                step = 1 if start_x < end_x else -1
                for x in range(start_x + step, end_x, step):
                    if board[start_y][x] != '-':
                        return False
            return True
    elif piece == 'N':  # Knight
        # Knight moves in an L-shape (2 squares in one direction and 1 square perpendicular)
        if (abs(start_x - end_x) == 1 and abs(start_y - end_y) == 2) or (abs(start_x - end_x) == 2 and abs(start_y - end_y) == 1):
            return True
    elif piece == 'B':  # Bishop
        # Bishop moves diagonally
        if abs(start_x - end_x) == abs(start_y - end_y):
            # Check if there are any pieces blocking the path
            step_x = 1 if start_x < end_x else -1
            step_y = 1 if start_y < end_y else -1
            x, y = start_x + step_x, start_y + step_y
            while x != end_x and y != end_y:
                if board[y][x] != '-':
                    return False
                x += step_x
                y += step_y
            return True
    elif piece == 'Q':  # Queen
        # Queen moves horizontally, vertically, or diagonally
        if start_x == end_x or start_y == end_y or abs(start_x - end_x) == abs(start_y - end_y):
            # Check if there are any pieces blocking the path
            if start_x == end_x:  # vertical move
                step = 1 if start_y < end_y else -1
                for y in range(start_y + step, end_y, step):
                    if board[y][start_x] != '-':
                        return False
            elif start_y == end_y:  # horizontal move
                step = 1 if start_x < end_x else -1
                for x in range(start_x + step, end_x, step):
                    if board[start_y][x] != '-':
                        return False
            else:  # diagonal move
                step_x = 1 if start_x < end_x else -1
                step_y = 1 if start_y < end_y else -1
                x, y = start_x + step_x, start_y + step_y
                while x != end_x and y != end_y:
                    if board[y][x] != '-':
                        return False
                    x += step_x
                    y += step_y
            return True
    elif piece == 'K':  # King
        # King moves one square in any direction
        if abs(start_x - end_x) <= 1 and abs(start_y - end_y) <= 1:
            return True
        # Check for castling (not implemented in this example)
    return False  # If no specific move validation is found, consider the move illegal


def handle_player_movement():
    global current_player, last_move_time
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN and current_player == 'WHITE':
            # Get the position of the mouse click
            x, y = pygame.mouse.get_pos()

            # Convert mouse position to board coordinates
            board_x = x // SQUARE_SIZE
            board_y = y // SQUARE_SIZE

            # Check if a piece is selected
            if board[board_y][board_x] != '-':
                selected_piece = (board_x, board_y)
            elif selected_piece:
                # Move the selected piece to the clicked position
                dest_x, dest_y = board_x, board_y
                if is_legal_move(selected_piece, (dest_x, dest_y)):
                    move_piece(selected_piece, (dest_x, dest_y))
                    switch_turns()
                    last_move_time = time.time()
                    return


running = True
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Handle player movement
    handle_player_movement()

    # Update the display
    draw_board()
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()

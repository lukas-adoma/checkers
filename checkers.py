# Will need an end turn button if the person does not want to do more than one attack.

import numpy as np
import pygame
import sys
import random

COLUMN_COUNT = 8
ROW_COUNT = 8

PLAYER_ONE = 1
PLAYER_TWO = 2

TURN_ONE = 0
TURN_TWO = 1

KING_PIECE_ONE = 3
KING_PIECE_TWO = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    count = 0
    for row in range(ROW_COUNT - 3, ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if (count % 2 == 0) and (row % 2 == 0):
                board[row][col] = 1
            if (count % 2 == 1) and (row % 2 == 1):
                board[row][col] = 1
            count = count + 1
    for row in range(ROW_COUNT - 8, ROW_COUNT - 5):
        for col in range(COLUMN_COUNT):
            if (count % 2 == 1) and (row % 2 == 1):
                board[row][col] = 2
            if (count % 2 == 0) and (row % 2 == 0):
                board[row][col] = 2
            count = count + 1
    return board


board = create_board()


def get_piece(board, row, col):
    if (int(board[row][col]) == KING_PIECE_ONE):
        return KING_PIECE_ONE
    if (int(board[row][col]) == KING_PIECE_TWO):
        return KING_PIECE_TWO
    if (int(board[row][col]) == PLAYER_ONE):
        return PLAYER_ONE
    if (int(board[row][col]) == PLAYER_TWO):
        return PLAYER_TWO
    else:
        return 0


def valid_locations(board, row, col, player):
    piece = get_piece(board, row, col)
    # might have to cast as an int because the return is different. This is why the == is not working.
    valid_locations_list = []
    try:
        # this is not working, not finding if value at position is ==0.
        if (board[row - 1][col - 1] == 0):
            valid_locations_list.append([row - 1, col - 1])
    except IndexError:
        pass
    try:
        if (board[row - 1][col + 1] == 0):
            valid_locations_list.append([row - 1, col + 1])
    except IndexError:
        pass

    # Additional Diag for King
    if piece == KING_PIECE_ONE or piece == KING_PIECE_TWO:
        try:
            if (board[row + 1][col - 1] == 0):
                valid_locations_list.append([row + 1, col - 1])
        except IndexError:
            pass
        try:
            if (board[row + 1][col + 1] == 0):
                valid_locations_list.append([row + 1, col + 1])
        except IndexError:
            pass

    return valid_locations_list


# Change depending on the player because the board does not flip. Ideally find a way for the board to flip.
def valid_kills(board, row, col, player):
    piece = get_piece(board, row, col)
# This kill list elements will be iterated into this method and then more posiitions will be appended until all potential kills positions are added. for each element in array add into valid kill one method.
    valid_kill_list = []
    try:
        if (board[row + 1][col + 1] == other_player(player) and board[row + 2][col + 2] == 0):
            valid_kill_list.append([row + 2, col + 2])
    except IndexError:
        pass
    try:
        if (board[row - 1][col + 1] == other_player(player) and board[row - 2][col + 2] == 0):
            valid_kill_list.append([row - 2, col + 2])
    except IndexError:
        pass
    if piece == KING_PIECE_ONE or piece == KING_PIECE_TWO:
        try:
            if (board[row + 1][col - 1] == other_player(player) and board[row + 2][col - 2] == 0):
                valid_kill_list.append([row + 1, col - 1])
        except IndexError:
            pass
        try:
            if (board[row - 1][col - 1] == other_player(player) and board[row - 2][col - 2] == 0):
                valid_kill_list.append([row - 1, col - 1])
        except IndexError:
            pass

    return valid_kill_list


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def other_player(player):
    if ((player + 1) % 2) == 0:
        return PLAYER_TWO
    else:
        return PLAYER_ONE


def winning_move(board, piece):
    count = 0
    if piece == PLAYER_ONE:
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if (board[row][col] == 2):
                    count = count + 1
    if piece == PLAYER_TWO:
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if (board[row][col] == 1):
                    count = count + 1
    if (count == 0):
        return True
    return False


def player_move_valid_locations(player):
    player_king = player + 2
    askposition = True
    while askposition:
        # Add difference for different players, and make sure selected checker is not 0.
        row = input("Choose checker row to move")
        col = input("Choose checker col to move")
        try:
            # Taking column input as index format so it is subtracted by one.
            col = int(col)
            row = int(row)
            if col <= 7 or col >= 0:
                if (get_piece(board, row, col) is player) or (get_piece(board, row, col) is player_king):
                    valid_kill_list = valid_kills(board, row, col, PLAYER_ONE)
                    valid_locations_list = valid_locations(
                        board, row, col, PLAYER_ONE)
                    if len(valid_kill_list) is not 0:
                        print(valid_kill_list)
                        print("This is valid_kill_list")
                        askposition = False
                    else:
                        if len(valid_locations_list) is not 0:
                            print(valid_locations_list)
                            print("This is the valid_locations_list")
                            askposition = False
                        else:
                            print("No valid moves, please choose another piece")
                else:
                    print("Please select one of your checkers.")
            else:
                print("Enter a number 1-8")
        except:
            print("Please enter a valid number!")


def player_execute_move(player):
    askposition = True
    while askposition:
        row = input("Choose final checker row position")
        col = input("Choose final checker column position")


game_over = False
# Chooses which player will go first.
# turn = random.randint(TURN_ONE, TURN_TWO)
turn = TURN_ONE
pygame.init()
print('Welcome to checkers!')
print(board)
while not game_over:
    # Need a board.flip class for each time turn changes.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if turn == TURN_ONE and not game_over:
        print("Player One")
        player_move_valid_locations(PLAYER_ONE)
        print("Player One")
        player_execute_move(PLAYER_ONE)

    if turn == TURN_TWO and not game_over:
        col = int(input("Player 2 make your column selection")) - 1
        row = int(input("Player 2 make your row selection")) - 1
        if valid_locations(board, row, col, PLAYER_TWO):
            pass
    turn += 1  # Changes turns from one person to another.
    turn = turn % 2

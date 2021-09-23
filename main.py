import random
import numpy as np

flag_code = 13
not_checked_code = 12

"""
Initializes a size x size matrix with 10. In this matrix, a 10 means that the
player doesn't know what value is in that box, otherwise it will show the number
of adjacent bombs.
"""
def init_game_board (size):
    game_board = [[not_checked_code for i in range(size)] for j in range(size)]
    return game_board

# Initializes a matrix that indicates the board that the player will see
def init_player_board (size):
    player_board = [[2 for i in range(2 * size + 1)] for j in range(2 * size + 1)]

    for i in range(2 * size + 1):
        for j in range(2 * size + 1):
            if i % 2 == 0:
                player_board [i][j] = 10
            elif j % 2 == 0:
                player_board [i][j] = 11
            else:
                player_board [i][j] = 12

    return  player_board

def move_game_board_on_player_board (size, game_board, player_board):
    for i in range(size):
        for j in range(size):
            player_board[2 * i + 1][2 * j + 1] = game_board[i][j]

    return player_board

"""
Codes for the signs used when showing the board.
'*' = -1
' ' = 0
'-' = 10
'|' = 11
'0' = 12
'P' = 13
"""
def print_player_board (size, player_board):
    for i in player_board:
        for j in i:
            if j == -1:
                print('*', end = "")
            elif j == 0:
                print(' ', end = "")
            elif j < 10:
                print(str (j), end = "")
            elif j == 10:
                print('-', end = "")
            elif j == 11:
                print('|', end = "")
            elif j == 12:
                print('0', end = "")
            elif j == 13:
                print('P', end = "")
        print()


"""
The function initializes a size x size minesweeper board and will put
bombs in random places of the matrix. The bombs will have the -1 value.
"""
def generate_random_minesweeper_board (size, num_of_bombs):
    board = [[0 for i in range (size)] for j in range (size)]

    num_of_bombs_added = 0
    while num_of_bombs_added < num_of_bombs:
        rand = random.randint (1, size * size) - 1
        row = int (rand / size)
        col = rand % size

        if board [row][col] == 0:
            board [row][col] = -1
            num_of_bombs_added += 1

    return board


"""
The function calculates the values of the non-mine squares.
"""
def calculate_board_values (size, board):
    for i in range (size):
        for j in range (size):
            if board [i][j] == -1:
                if i - 1 >= 0:
                    if j - 1 >= 0:
                        if board [i - 1][j - 1] != -1:
                            board [i - 1][j - 1] += 1
                    if board [i - 1][j] != -1:
                        board [i - 1][j] += 1
                    if j + 1 < size:
                        if board [i - 1][j + 1] != -1:
                            board [i - 1][j + 1] += 1
                if j - 1 >= 0:
                    if board [i][j - 1] != -1:
                        board [i][j - 1] += 1
                if j + 1 < size:
                    if board [i][j + 1] != -1:
                        board [i][j + 1] += 1
                if i + 1 < size:
                    if j - 1 >= 0:
                        if board [i + 1][j - 1] != -1:
                            board [i + 1][j - 1] += 1
                    if board [i + 1][j] != -1:
                        board [i + 1][j] += 1
                    if j + 1 < size:
                        if board [i + 1][j + 1] != -1:
                            board [i + 1][j + 1] += 1
    return board

"""
This function makes sure that if you press on a cell that is not a number, all
the adjacent non-bomb cells will reveal themselves
"""
def game_simplification (size, board, game_board, player_board):
    modify = True

    # While we make a modification in the game_board, we loop back to verify
    # if there are any cells that need to be shown to the player and weren't
    # shown previously
    while modify:
        modify = False
        for i in range(size):
            for j in range(size):
                if game_board[i][j] == not_checked_code:
                    if i - 1 >= 0:
                        if j - 1 >= 0:
                            if game_board[i - 1][j - 1] == 0:
                                game_board[i][j] = board[i][j]
                                modify = True
                                continue
                        if game_board[i - 1][j] == 0:
                            game_board[i][j] = board[i][j]
                            modify = True
                            continue
                        if j + 1 < size:
                            if game_board[i - 1][j + 1] == 0:
                                game_board[i][j] = board[i][j]
                                modify = True
                                continue
                    if j - 1 >= 0:
                        if game_board[i][j - 1] == 0:
                            game_board[i][j] = board[i][j]
                            modify = True
                            continue
                    if j + 1 < size:
                        if game_board[i][j + 1] == 0:
                            game_board[i][j] = board[i][j]
                            modify = True
                            continue
                    if i + 1 < size:
                        if j - 1 >= 0:
                            if game_board[i + 1][j - 1] == 0:
                                game_board[i][j] = board[i][j]
                                modify = True
                                continue
                        if game_board[i + 1][j] == 0:
                            game_board[i][j] = board[i][j]
                            modify = True
                            continue
                        if j + 1 < size:
                            if game_board[i + 1][j + 1] == 0:
                                game_board[i][j] = board[i][j]
                                modify = True
                                continue

    player_board = move_game_board_on_player_board(size, game_board, player_board)
    print_player_board(size, player_board)
    return game_board



# Code runs when you lose the game
def game_loss (size, board, player_board):
    for i in range(size):
        for j in range(size):
            if board[i][j] == -1:
                player_board[2 * i + 1][2 * j + 1] = -1

    print_player_board(size, player_board)
    print("You lost!")
    return player_board

def game_turn (size, board, game_board, player_board):
    end = 0

    while end == 0:
        action = int (input("What action do you choose to do? "))
        if action == 1:
            flag = False
        else:
            flag = True

        row = int (input("Introduce the row number: ")) - 1
        col = int (input("Introduce the column number: ")) - 1

        if game_board[row][col] != not_checked_code:
            print("The box was already checked, please try again")

        # We verify if it checked a bomb, in which case the game is lost.
        if board[row][col] == -1 and not flag:
            player_board = game_loss(size, board, player_board)
            end = -1
        elif board[row][col] == 0 and not flag:
            game_board[row][col] = 0
            game_board = game_simplification(size, board, game_board, player_board)
        else:
            if flag == False:
                game_board[row][col] = board[row][col]
            else:
                game_board[row][col] = flag_code

            move_game_board_on_player_board(size, game_board, player_board)
            print_player_board(size, player_board)

        # We check if the game ended.
        if end != -1:
            end = 1
            for i in game_board:
                for j in i:
                    if j == not_checked_code:
                        end = 0

        if end == 1:
            print("You won!")

def main():
    print("(1) EASY: 8x8 with 10 bombs")
    print("(2) MEDIUM: 16x16 with 40 bombs")
    print("(3) HARD: 24x24 with 100 bombs")
    choice = input("Choose the number of the game option you want: ")

    while choice != "1" and choice != "2" and choice != "3":
        print("You didn't choose a valid mode, please try again.")
        choice = input("Choose the number of the game option you want: ")

    if choice == "1":
        size = 8
        num_of_bombs = 10
    elif choice == "2":
        size = 16
        num_of_bombs = 40
    else:
        size = 24
        num_of_bombs = 100

    print("Each turn you have 2 options and you should press 1 or 2 depending" +
          " on your decision:")
    print("(1) Check a box")
    print("(2) Flag a box")

    board = generate_random_minesweeper_board(size, num_of_bombs)
    board = calculate_board_values(size, board)
    game_board = init_game_board(size)

    player_board = init_player_board(size)
    move_game_board_on_player_board(size, game_board, player_board)
    print_player_board(size, player_board)
    game_turn(size, board, game_board, player_board)

if __name__ == '__main__':
    main ()

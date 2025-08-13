import math
import random
import matplotlib.pyplot as plt
import numpy as np

# Tic Tac Toe Board Visualization
def draw_board(board):
    fig, ax = plt.subplots()
    ax.set_xticks([0.5, 1.5], minor=True)
    ax.set_yticks([0.5, 1.5], minor=True)
    ax.grid(which="minor", color="black", linewidth=2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ':
                ax.text(j + 0.5, 2.5 - i, board[i][j], fontsize=40, ha='center', va='center')
    plt.show(block=False)
    plt.pause(1)
    plt.close()

# Check for winner
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

# Check if moves are left
def moves_left(board):
    for row in board:
        if ' ' in row:
            return True
    return False

# Minimax Algorithm
def minimax(board, depth, is_max):
    winner = check_winner(board)
    if winner == 'O':
        return 10 - depth
    elif winner == 'X':
        return depth - 10
    elif not moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = ' '
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = ' '
        return best

# Find best move for AI
def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

# Main game loop
def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    human_turn = True if random.choice([True, False]) else False
    print("You are X, AI is O")

    while True:
        draw_board(board)
        if check_winner(board) or not moves_left(board):
            break

        if human_turn:
            row, col = random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ' '])
            board[row][col] = 'X'
        else:
            move = find_best_move(board)
            board[move[0]][move[1]] = 'O'
        human_turn = not human_turn

    draw_board(board)
    winner = check_winner(board)
    if winner:
        print(f"Winner: {winner}")
    else:
        print("It's a tie!")

play_game()

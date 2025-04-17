# ----- system ----- #
from copy import deepcopy
from random import choice


from random import choice


def get_random_move(board: list[list[str]]) -> tuple[int, int]:
    if choice([True, False]):
        empty = [(i, j) for i in range(3)
                 for j in range(3) if board[i][j] == " "]
        return choice(empty) if empty else (-1, -1)

    for mark in ["X", "O"]:
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = mark
                    if check_winner(board) == mark:
                        board[i][j] = " "
                        return i, j
                    board[i][j] = " "

    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return choice(empty) if empty else (-1, -1)


def get_optimal_move(board: list[list[str]]) -> tuple[int, int]:
    best_score = float("-inf")
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                temp = deepcopy(board)
                temp[i][j] = "X"
                score = minimax(temp, False)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move


def minimax(board: list[list[str]], is_maximizing: bool):
    winner = check_winner(board)

    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    elif all(cell != " " for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    temp = deepcopy(board)
                    temp[i][j] = "X"
                    score = minimax(temp, False)
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    temp = deepcopy(board)
                    temp[i][j] = "O"
                    score = minimax(temp, True)
                    best_score = min(score, best_score)
        return best_score


def check_winner(board: list[list[str]]) -> str | None:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None

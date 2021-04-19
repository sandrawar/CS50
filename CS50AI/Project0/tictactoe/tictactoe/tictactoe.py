"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xys = 0
    zeros = 0
    for row in board:
        for cell in row:
            if cell == X:
                xys += 1
            if cell == O:
                zeros += 1
    if xys > zeros:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                action = (i, j)
                actions.add(action)
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    if board[i][j] != None:
        raise ValueError
    newBoard = copy.deepcopy(board)
    newBoard[i][j] = player(board)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        symbol = board[i][0]
        if symbol != None:
            winner = True
            for j in range(3):
                if board[i][j] != symbol:
                    winner = False
                    break
            if winner:
                return symbol
    
    symbol = board[1][1]
    if symbol != None:
        if ((board[0][0] == symbol and board[2][2] == symbol)  or (board[0][2] == symbol and board[2][0] == symbol)):
            return symbol
    
    for j in range(3):
        symbol = board[0][j]
        if symbol != None:
            winner = True
            for i in range(3):
                if board[i][j] != symbol:
                    winner = False
                    break
            if winner:
                return symbol
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != None or not bool(actions(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    whoWon = winner(board)
    if whoWon == X:
        return 1
    if whoWon == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    """
    if terminal(board):
        return None

    if player(board) == X:
        choice = -2
        for action in actions(board):
            nextBoard = result(board, action)
            while not terminal(nextBoard):
                nextBoard = result(nextBoard, minimax(nextBoard))
            points = utility(nextBoard)
            if points > choice:
                choice = points
                move = action
        return move
    else:
        choice = 2
        for action in actions(board):
            nextBoard = result(board, action)
            while not terminal(nextBoard):
                nextBoard = result(nextBoard, minimax(nextBoard))
            points = utility(nextBoard)
            if points < choice:
                move = action
                choice = points
        return move
    """
    
    # vol 2

    def maxValue(board, parentMinValue):
        if terminal(board):
            return (utility(board), None)
        maxValue = -2
        maxAction = None
        for action in actions(board):
            new = minValue(result(board, action), maxValue)
            if new[0] > maxValue:
                maxValue = new[0]
                maxAction = action
            if maxValue >= parentMinValue:
                break
        return (maxValue, maxAction)

    def minValue(board, parentMaxValue):
        if terminal(board):
            return (utility(board), None)
        minValue = 2
        minAction = None
        for action in actions(board):
            new = maxValue(result(board, action), minValue)
            if new[0] < minValue:
                minValue = new[0]
                minAction = action
            if minValue <= parentMaxValue:
                break
        return (minValue, minAction)
    
    
    if player(board) == X:
        return maxValue(board, 2)[1]
    return minValue(board, -2)[1]

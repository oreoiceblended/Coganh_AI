from Bot import RandomBot, AlphaBetaBot, Board, getBoardAfterMove
import time, copy
curBoard = [
    [ 1,  1,  1,  1,  1],
    [ 1,  0,  0,  0,  1],
    [ 1,  0,  0,  0, -1],
    [-1,  0,  0,  0, -1],
    [-1, -1, -1, -1, -1]
]
player1 =  RandomBot(1)
player2 = AlphaBetaBot(-1)
pre_board = None
board = Board(curBoard)

while True:
    move = player2.move(pre_board, board.mat, 0, 0)
    if move == None:
        print('Player2 fail to move')
        break
    print("Player 2 move ", move)
    pre_board = copy.deepcopy(board.mat)
    getBoardAfterMove(board, -1, move)
    board.print()
    move = player1.move(pre_board, board.mat, 0, 0)
    if move == None:
        print('Player1 fail to move')
        break
    print("Player 1 move ", move)
    pre_board = copy.deepcopy(board.mat)
    getBoardAfterMove(board, 1, move)
    board.print()



    
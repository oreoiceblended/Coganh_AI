from Bot import RandomBot, AlphaBetaBot, Board, getBoardAfterMove, QLearningBot
import time, copy
init_board = [
    [ 1,  1,  1,  1,  1],
    [ 1,  0,  0,  0,  1],
    [ 1,  0,  0,  0, -1],
    [-1,  0,  0,  0, -1],
    [-1, -1, -1, -1, -1]
]
bot = QLearningBot(-1)
def fight(turn):
    randomBot =  RandomBot(1)
    pre_board = None
    board = Board(copy.deepcopy(init_board))
    countX = 0
    countO = 0
    if turn == 1:
        countO = 1
        move = randomBot.move(pre_board, board.mat, 0, 0)
        prev_board = copy.deepcopy(board.mat)
        getBoardAfterMove(board, 1, move)
    while True:
        move = bot.move(pre_board, board.mat, 0, 0)
        if move == None:
            print('Bot fail to move')
            break
        countX += 1
        print("Bot move ", move)
        pre_board = copy.deepcopy(board.mat)
        getBoardAfterMove(board, -1, move)
        board.print()
        if countO == 50 and countX == 50:
            break
        move = randomBot.move(pre_board, board.mat, 0, 0)
        if move == None:
            print('RandomBot fail to move')
            break
        countO += 1
        print("Random Bot move ", move)
        pre_board = copy.deepcopy(board.mat)
        getBoardAfterMove(board, 1, move)
        board.print()
        if countO == 50 and countX == 50:
            break
    winner = board.getWinner()
    if winner == -1:
        print("---------QLearning Bot win:", countX)
    else:
        print("---------Random Bot win:", countO)
    board.print()

while True:
    print("------CHOOSE YOUR OPTION------")
    print("1. Random First")
    print("2. QLearning First")
    print("3. Quit")

    t = input()
    if t == '1':
        fight(1)
    elif t == '2':
        fight(-1)
    elif t == '3':
        break
    



    
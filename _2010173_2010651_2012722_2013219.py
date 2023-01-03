import time
import copy
import math
INF = math.inf
SIZE = 5
encodedBoardHelper = [
    [(0,0), (1,0), (2,0), (1,0), (0,1)],
    [(1,3), (4,0), (3,0), (4,0), (1,1)],
    [(2,3), (3,0), (4,0), (3,0), (2,1)],
    [(1,3), (4,0), (3,0), (4,0), (1,1)],
    [(0,3), (1,2), (2,2), (1,2), (0,2)]
]
directValue = [
    (-1,-1), (-1, 0), (-1, 1),
    ( 0,-1), ( 0, 0), ( 0, 1),
    ( 1,-1), ( 1, 0), ( 1, 1)
]
boardDirect = [
    [[5,8,7], [7,6,3], [3,0,1], [1,2,5]],
    [[5,7,3], [7,3,1], [3,1,5], [1,5,7]],
    [[5,7,3,8,6], [7,3,1,6,0], [3,1,5,0,2], [1,5,7,2,8]],
    [[1,3,5,7]],
    [[0,1,2,3,5,6,7,8]]
]
symmetricPoint = [
    [[], [], [], []],
    [[(5,3)], [(7,1)], [(3,5)], [(1,7)]],
    [[(5,3)], [(7,1)], [(3,5)], [(1,7)]],
    [[(3,5),(1,7)]],
    [[(0,8),(1,7),(3,5),(2,6)]]
]
boardHelper = []
symmetricHelper = []
for i in range(5):
    boardHelper.append([])
    symmetricHelper.append([])
    for j in range(5):
        helper = encodedBoardHelper[i][j]
        indexes = boardDirect[helper[0]][helper[1]]
        directs = [directValue[x] for x in indexes]
        xy = [(x[0]+i,x[1]+j) for x in directs] 
        symIndexes = symmetricPoint[helper[0]][helper[1]]
        symmetrics = [(directValue[x[0]], directValue[x[1]]) for x in symIndexes]
        symXy = [[(x[0]+i,x[1]+j) for x in y] for y in symmetrics] 
        boardHelper[i].append(xy)
        symmetricHelper[i].append(symXy)

class Board():
    def __init__(self,board):
        self.mat = board
        self.numO = 0
        self.numX = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] == 1:
                    self.numO += 1
                elif board[i][j] == -1:
                    self.numX += 1
    def staticEval(self, player):
        if player == 1:
            if self.numO == 0:
                return -INF
            if self.numX == 0:
                return INF
            return self.numO - self.numX
        else:
            if self.numO == 0:
                return INF
            if self.numX == 0:
                return -INF
            return self.numX - self.numO
    def updatequantity(self):
        self.numO = 0
        self.numX = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if self.mat[i][j] == 1:
                    self.numO += 1
                elif self.mat[i][j] == -1:
                    self.numX += 1
def get_prev_move(prev_board, cur_board):
    start = ()
    end = ()
    for i in range(5):
        for j in range(5):
            if start is None and end is None:
                break
            if prev_board[i][j] != 0 and cur_board[i][j] == 0:
                start = (i,j)
            if prev_board[i][j] == 0 and cur_board[i][j] != 0:
                end = (i,j)
    return (start, end)
def isTrapChess(board:Board, fromPos, toPos):
    (fx, fy) = fromPos
    (tx, ty) = toPos
    symmetries = symmetricHelper[fx][fy]
    for sym in symmetries:
        if toPos in sym:
            if toPos == sym[0]:
                (sx, sy) = sym[1]
            else:
                (sx, sy) = sym[0]
            if board.mat[sx][sy] == board.mat[tx][ty]:
                helper = boardHelper[fx][fy]
                for point in helper:
                    (px, py) = point
                    if board.mat[px][py] == -board.mat[tx][ty]:
                        return True
            break
    return False
def isMovableChess(board, chessPos):
    ends = []
    (x, y) = chessPos
    moveList = boardHelper[x][y]
    for point in moveList:
        (px, py) = point
        if board[px][py] == 0:
            end = (px, py)
            ends.append(end)
    return ends
def getMovableChessList(board:Board, player, trapPos):
    movableList = []
    # Get chess is trapped if exist
    if trapPos is not None:
        (trX, trY) = trapPos
        end = (trX, trY)
        helper = boardHelper[trX][trY]
        for point in helper:
            (px, py) = point
            chessPlayer = board.mat[px][py]
            if player == chessPlayer:
                start = (px, py)
                movableList.append((start, end))
        if len(movableList) > 0:
            return movableList
    # Get all player chess
    for i in range(5):
        for j in range(5):
            if board.mat[i][j] == player:
                start = (i, j)
                ends = isMovableChess(board.mat, start)
                if len(ends) > 0:
                    for end in ends:
                        movableList.append((start, end))
    return movableList
def eatBySymmetries(board, player, pos):
    (x, y) = pos
    symmetries = symmetricHelper[x][y]
    for sym in symmetries:
        (x1, y1) = sym[0]
        (x2, y2) = sym[1]
        chess1Player = board[x1][y1]
        chess2Player = board[x2][y2]
        if chess1Player == chess2Player:
            if player != chess1Player and chess1Player != 0:
                board[x1][y1] = player
                board[x2][y2] = player
def getUnmoveChessList(board, curChessPlayer, pos, visitted):
    if pos in visitted:
        return False
    visitted.add(pos)
    (x, y) = pos
    helper = boardHelper[x][y]
    rt = False
    i = 0
    n = len(helper)
    while i < n and not rt:
        (px, py) = helper[i]
        chessPlayer = board[px][py]
        if chessPlayer == 0:
            rt = rt or True
        elif chessPlayer == curChessPlayer:
            rt = rt or getUnmoveChessList(board, curChessPlayer,
                helper[i], visitted)
        i += 1
    return rt
def getBoardAfterMove(board:Board, player, move):
    (fx, fy) = move[0]
    (tx, ty) = move[1]
    board.mat[fx][fy] = 0
    board.mat[tx][ty] = player
    # Get "Gánh" chessmans
    eatBySymmetries(board.mat, player, move[1])
    # Get "Vây" chessmans
    for i in range(5):
        for j in range(5):
            visitted = set()
            chessPlayer = board.mat[i][j]
            if (chessPlayer != 0 and chessPlayer != player
                    and not getUnmoveChessList(board.mat, chessPlayer,
                    (i, j), visitted)):
                for changePos in visitted:
                    (px, py) = changePos
                    board.mat[px][py] = player
    board.updatequantity()
def move(prev_board, board, player, remain_time_x, remain_time_o):
    timestart = time.time()
    timepermove = 3
    prev_move = None
    if prev_board is not None:
        prev_move =  get_prev_move(prev_board, board)
    cur_board_obj = Board(board)
    ai = AI(player)
    res = ai.alpha_beta_search(cur_board_obj, player, prev_move, timepermove-(time.time() -timestart))
    return res
class AI:
    def __init__(self, player):
        self.PLAYERID = player
    def alpha_beta_search(self, board:Board, player:int, prev_move, timepermove):
        timestart = time.time()
        alpha = -INF
        beta = INF
        trapPos = None
        if prev_move is not None and isTrapChess(board, prev_move[0], prev_move[1]):
            trapPos = prev_move[0]
        else:
            trapPos = None
        movableList = getMovableChessList(board, player, trapPos)
        if len(movableList) == 0:
            return None
        if len(movableList) == 1:
            return movableList[0]
        n = len(movableList)
        nexttimepermove = (timepermove/n) - 0.0001 - (time.time() -timestart)
        best_move = ()
        for i in range(len(movableList)):
            next_board = Board(copy.deepcopy(board.mat))
            getBoardAfterMove(next_board, player, movableList[i])
            value = self.min_value(next_board, (-1)*player, alpha, beta , movableList[i], nexttimepermove)
            if value > alpha:
                alpha = value
                best_move = movableList[i]
            if alpha >= beta:
                break
        return best_move

    def min_value(self, board:Board, player, alpha, beta, prev_move, timepermove):
        if  timepermove <= 0:
            return board.staticEval(self.PLAYERID)
        timestart = time.time()
        value = beta
        if isTrapChess(board, prev_move[0], prev_move[1]):
            trapPos = prev_move[0]
        else:
            trapPos = None
        movableList = getMovableChessList(board, player, trapPos)
        n = len(movableList)
        if (n == 0):
            return value
        nexttimepermove = (timepermove/n) - 0.0001 - (time.time() -timestart)
        for i in range(len(movableList)):
            next_board = Board(copy.deepcopy(board.mat))
            getBoardAfterMove(next_board, player, movableList[i])
            value = min(value, self.max_value(next_board, (-1)*player, alpha, beta , movableList[i], nexttimepermove))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def max_value(self, board:Board, player, alpha, beta, prev_move, timepermove):
        if  timepermove <= 0:
            return board.staticEval(self.PLAYERID)
        timestart = time.time()
        value = alpha
        if isTrapChess(board, prev_move[0], prev_move[1]):
            trapPos = prev_move[0]
        else:
            trapPos = None
        movableList = getMovableChessList(board, player, trapPos)
        n = len(movableList)
        if (n == 0):
            return value
        nexttimepermove = (timepermove/n) - 0.0001 - (time.time() -timestart)
        for i in range(len(movableList)):
            next_board = Board(copy.deepcopy(board.mat))
            getBoardAfterMove(next_board, player, movableList[i])
            value = max(value, self.min_value(next_board, (-1)*player, alpha, beta , movableList[i],nexttimepermove))
            if value >= beta:
                return value
            beta = max(beta, value)
        return value
from cmath import inf
from turtle import st
from typing import List
import sys
from xmlrpc.client import Boolean
import copy
import pdb

if len(sys.argv) == 3:
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]

RegularRed = 'regularRed'
KingRed = 'kingRed'
RegularBlack = 'regularBlack'
KingBlack = 'kingBlack'

regularRedDirections = ((-1, -1), (-1, 1))
kingRedDirections = ((-1, -1), (-1, 1), (1, 1), (1, -1))
regularRedCapture = ((-2, -2), (-2, 2))
kingRedCapture = ((-2, -2), (-2, 2), (2, -2), (2, 2))

regularBlackDirections = ((1, -1), (1, 1))
kingBlackDirections = ((-1, -1), (-1, 1), (1, 1), (1, -1))
regularBlackCapture = ((2, -2), (2, 2))
kingBlackCapture = ((-2, -2), (-2, 2), (2, -2), (2, 2))


class Solver:

    def solveChecker(self):
        board = self.readInput('input0.txt')
        node = Node(board, None, 0, 'red')
        new_move = node.AlphaBeta(float('-inf'), float('inf'))
        move = new_move[0]
        nxt_node = node.makeAMove(move)
        res_board = nxt_node.board
        res = ''
        for row in res_board:
            for p in row:
                res += p
            res += '\n'
        print(res)
        f = open(OUTPUT, 'w')
        f.write(res)
        f.close()

    def readInput(self, inputFile: str) -> List[List[str]]:
        board = []
        f = open(inputFile, 'r')
        line = f.readline().rstrip()
        row = self._lineToList(line)
        board.append(row)
        while line:
            line = f.readline().rstrip()
            row = self._lineToList(line)
            board.append(row)
        return board

    def _lineToList(self, line: str) -> List[str]:
        res = []
        for s in line:
            res.append(s)
        return res


class Node:
    def __init__(self, board: List[List[str]], parent, depth: int, player: str) -> None:
        """

        Args:
            
            player (str): Only has value red or black; Red is max and black is min.
        """
        self.board = board
        self.parent = parent
        self.depth = depth
        self.player = player
        self.pieces = {'regularRed': [],
                       'kingRed': [],
                       'regularBlack': [],
                       'kingBlack': []
                       }
        self.piecesInfo = self.getPiecesInfo()

    def getPiecesInfo(self) -> List[int]:
        """ Return value is [red_pieces, red_kings, black_pieces, black_kings]
        """
        info = [0, 0, 0, 0]
        for row in range(8):
            for p in range(8):
                if self.board[row][p] == 'r':
                    self.pieces['regularRed'].append([row, p])
                    info[0] += 1
                if self.board[row][p] == 'R':
                    self.pieces['kingRed'].append([row, p])
                    info[1] += 1
                if self.board[row][p] == 'b':
                    self.pieces['regularBlack'].append([row, p])
                    info[2] += 1
                if self.board[row][p] == 'B':
                    self.pieces['kingBlack'].append([row, p])
                    info[3] += 1

        return info

    def getUtility(self):
        pieces = self.getPiecesInfo()
        uti = pieces[0] + 2 * pieces[1] - pieces[2] - 2 * pieces[3]
        return uti

    def endGame(self) -> Boolean:
        info = self.getPiecesInfo()
        if self.player == 'red':
            if info[0] + info[1] == 0:
                return True
        if self.player == 'black':
            if info[2] + info[3] == 0:
                return True
        # TODO: if a player has no legal moves left, then the game also ends.
        if not self.getValidMoves():
            return True
        return False

    def normalMove(self, pos: List[int], direction: List[int]) -> None:
        """A piece makes a normal move

        Args:
            move (List[List[int]]): move[0] is the old coordinate; move[1] is the new location for move[0]
        """
        if self.board[new[0]][new[1]] != '.':
            print("invalid move")
            exit()
        # Check validity

        new = [pos[0] + direction[0], pos[1] + direction[1]]
        if new[0] < 0 or new[0] > 7 or new[1] < 0 or new[1] > 7:
            return
        if self.board[new[0]][new[1]] != '.':
            return

        piece = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = '.'
        self.board[new[0]][new[1]] = piece

    def validCapture(self, pos, move) -> Boolean:
        if pos[0] + move[0] < 0 or pos[0] + move[0] > 7 or pos[1] + move[1] < 0 or pos[1] + move[1] > 7:
            return False

        if self.board[pos[0]][pos[1]] == '.':
            print("invalid piece location1.")
            exit()

        if self.player == 'red':
            if self.board[pos[0]][pos[1]] == 'r':
                if move not in regularRedCapture:
                    print("not a capture for regular red")
                    exit()
                # must be a capture
                if (self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'b' or \
                    self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'B') and \
                        self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                return False

            if self.board[pos[0]][pos[1]] == 'R':
                if move not in kingRedCapture:
                    print("not a capture for king red")
                    exit()
                # must be a capture
                if (self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'b' or \
                    self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'B') and \
                        self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                return False

        if self.player == 'black':
            if self.board[pos[0]][pos[1]] == 'b':
                if move not in regularBlackCapture:
                    print("not a capture for regular black")
                    exit()
                # must be a capture
                if (self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'r' or \
                    self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'R') and \
                        self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                return False

            if self.board[pos[0]][pos[1]] == 'B':
                if move not in kingRedCapture:
                    print("not a capture for king black")
                    exit()
                # must be a capture
                if (self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'r' or \
                    self.board[pos[0] + int(1 / 2 * move[0])][pos[1] + int(1 / 2 * move[1])] == 'R') and \
                        self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                return False
        print("shouldn't reach here.")
        exit()

    def validMove(self, pos: List[int], move) -> Boolean:
        """_summary_

        Args:
            pos (List[int]): pos[0] and pos[1] is the coordinate
            move (List[int]): move a direction

        Returns:
            Boolean: _description_
        """
        if pos[0] + move[0] < 0 or pos[0] + move[0] > 7 or pos[1] + move[1] < 0 or pos[1] + move[1] > 7:
            return False
        if self.board[pos[0]][pos[1]] == '.':
            print("invalid piece location2.")
            exit()

        if self.player == 'red':
            # check if the pos is valid
            if self.board[pos[0]][pos[1]] == 'r':  # a regular red pieces
                # TODO: delete after debugging
                if move not in regularRedDirections:
                    print("invalid move for regular red")
                    exit()
                if self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                else:
                    return False
            if self.board[pos[0]][pos[1]] == 'R':  # king red
                if move not in kingRedDirections:
                    print("invalid move for king red")
                    exit()
                if self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                else:
                    return False
            print("impossible to get here")
            exit()
        if self.player == 'black':
            # check if the pos is valid
            if self.board[pos[0]][pos[1]] == 'b':  # a regular red pieces
                # TODO: delete after debugging
                if move not in regularBlackDirections:
                    print("invalid move for regular black")
                    exit()
                if self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                else:
                    return False
            if self.board[pos[0]][pos[1]] == 'B':  # king red
                if move not in kingBlackDirections:
                    print("invalid move for king black")
                    exit()
                if self.board[pos[0] + move[0]][pos[1] + move[1]] == '.':
                    return True
                else:
                    return False
            print("impossible to get here")
            exit()
        print("impossible to get here")
        exit()

        if self.player == 'black':
            pass
        pass

    def getValidMoves(self) -> List:
        capture = []  # contains pairs of [position, move]
        move = []

        if self.player == 'red':

            # check red regular pieces
            # Check capture first
            for red in self.pieces[RegularRed]:
                for dir in regularRedCapture:
                    if self.validCapture(red, dir):
                        # there is a valid capture.
                        capture.append([red, dir])
                        # red king capture
            for redKing in self.pieces[KingRed]:
                for dir in kingRedCapture:
                    if self.validCapture(redKing, dir):
                        capture.append([redKing, dir])
            # No need to check for normal moves if there is a capture
            if len(capture) == 0:
                # Check regular moves
                for red in self.pieces[RegularRed]:
                    for dir in regularRedDirections:
                        if self.validMove(red, dir):
                            # there is a valid capture.
                            move.append([red, dir])
                            # red king moves
                for redKing in self.pieces[KingRed]:
                    for dir in kingRedDirections:
                        if self.validMove(redKing, dir):
                            move.append([redKing, dir])

        if self.player == 'black':
            # check red regular pieces
            # Check capture first
            for black in self.pieces[RegularBlack]:
                for dir in regularBlackCapture:
                    if self.validCapture(black, dir):
                        # there is a valid capture.
                        capture.append([black, dir])
                        # red king capture
            for blackKing in self.pieces[KingBlack]:
                for dir in kingBlackCapture:
                    if self.validCapture(blackKing, dir):
                        capture.append([blackKing, dir])
            # No need to check for normal moves if there is a capture
            if len(capture) == 0:
                # Check regular moves
                for black in self.pieces[RegularBlack]:
                    for dir in regularBlackDirections:
                        if self.validMove(black, dir):
                            # there is a valid capture.
                            move.append([black, dir])
                            # red king moves
                for blackKing in self.pieces[KingBlack]:
                    for dir in kingBlackDirections:
                        if self.validMove(blackKing, dir):
                            move.append([blackKing, dir])
        # One of the lists will be empty. return the none empty one.

        if not capture: return move
        return capture

    def makeAMove(self, move: List[List[int]]):
        """make an actual move on board

        Args:
            move (List[List[int]]): move[0] is the position of the piece, move[1] is the direction of move
        """
        pos = move[0]
        dir = move[1]
        newBoard = copy.deepcopy(self.board)
        oldPlayer = self.player
        if oldPlayer == 'red':
            newPlayer = 'black'
        else:
            newPlayer = 'red'

        # normal move
        if abs(dir[0]) == 1:
            piece = newBoard[pos[0]][pos[1]]
            newBoard[pos[0]][pos[1]] = '.'
            newBoard[pos[0] + dir[0]][pos[1] + dir[1]] = piece
            if piece == 'r':
                if pos[0] + dir[0] == 0:
                    newBoard[pos[0] + dir[0]][pos[1] + dir[1]] = 'R'
            if piece == 'b':
                if pos[0] + dir[0] == 7:
                    newBoard[pos[0] + dir[0]][pos[1] + dir[1]] = 'B'



        else:  # jump
            piece = newBoard[pos[0]][pos[1]]
            newBoard[pos[0]][pos[1]] = '.'
            newBoard[pos[0] + int(1 / 2 * dir[0])][pos[1] + int(1 / 2 * dir[1])] = '.'
            newBoard[pos[0] + dir[0]][pos[1] + dir[1]] = piece
            if piece == 'r':
                if pos[0] + dir[0] == 0:
                    newBoard[pos[0] + dir[0]][pos[1] + dir[1]] = 'R'
            if piece == 'b':
                if pos[0] + dir[0] == 7:
                    newBoard[pos[0] + dir[0]][pos[1] + dir[1]] = 'B'

        newState = Node(newBoard, self, self.depth + 1, newPlayer)

        return newState

        # multi jump

    def AlphaBeta(self, alpha, beta):
        best_move = None
        if self.endGame() or self.depth >= 10:
            return best_move, self.getUtility()
        if self.player == 'red': value = float('-inf')
        if self.player == 'black': value = float('inf')
        for move in self.getValidMoves():
            print(move)
            piece = move[0]
            dir = move[1]
            nxt_state = self.makeAMove(move)
            nxt_move, nxt_val = nxt_state.AlphaBeta(alpha, beta)
            print(nxt_val)
            if self.player == 'red':  # red is max
                if value < nxt_val: value, best_move = nxt_val, move
                if value >= beta: return best_move, value
                alpha = max(alpha, value)
            if self.player == 'black':
                if value > nxt_val: value, best_move = nxt_val, move
                if value <= alpha: return best_move, value
                beta = min(beta, value)
        return best_move, value


# main is here
checkers = Solver()
checkers.solveChecker()

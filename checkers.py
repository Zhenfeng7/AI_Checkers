

from turtle import st
from typing import List
import sys
from typing_extensions import Self
from xmlrpc.client import Boolean

if len(sys.argv) == 3:
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]

regularRedDirections = ((-1, -1), (-1, 1))
kingRedDirections = ((-1, -1), (-1, 1), (1, 1), (1, -1))
regularRedCapture = ((-2, -2), (-2, 2))
kingRedCapture = ((-2, -2), (-2, 2),(2, -2), (2, 2))

regularBlackDirections = ((1, -1), (1, 1))
kingBlackDirections = ((-1, -1), (-1, 1), (1, 1), (1, -1))
regularBlackCapture = ((2, -2), (2, 2))
kingBlackCapture = ((-2, -2), (-2, 2),(2, -2), (2, 2))

class Solver:
    def __init__(self, board: List[List[str]]) -> None:
        self.board = board



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
                       'kingRed':[],
                       'regularBlack':[],
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
            return info[0] + info[1] == 0
        if self.player == 'black':
            return info[2] + info[3] == 0
        # TODO: if a player has no legal moves left, then the game also ends.
        
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
        
    def capture(self):
        pass
    
    def validCapture(self, pos, move) -> Boolean:
        pass
    
    def getValidMoves(self, player: str):
        capture = [] # contains pairs of [position, move]
        move = []
        
        if player == 'red':
            
            # check red regular pieces
            # Check capture first
            for red in self.pieces['regularRed']:
                for dir in regularRedCapture:
                    if self.validCapture(red, dir):
                        # there is a valid capture.
                        capture.append([red, dir])   
            
                    
                    
            
        if player == 'black':
            
        
        







# main is here


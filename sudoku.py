#! /usr/bin/python3
#
# CodeGrade Example Assigment
# support@codegrade.com

from math import sqrt

import sys
import os
import copy

EPSILON = 0.000000001
#commenting to show this edit

def validList(sudoku):
    """Checks if every list in a sudoku is valid.

    Every list should contain only one of every digit of the sudoku. The digit
    may also be zero, in this case it is a blank spot.
    """

    # For each row in the sudoku
    for l in sudoku:
        rangeList = list(range(1, len(sudoku) + 1))

        # For each item in the row
        for item in l:
            if item not in rangeList and item != 0:
                return False
            if item != 0:
                rangeList.remove(item)
    return True


class Sudoku:
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.size = len(board)

    @classmethod
    def fromStdIn(cls):
        board = []

        for txt in sys.stdin:
            row = []

            for cell in txt.split():
                if cell == '_':
                    row.append(0)
                else:
                    row.append(int(cell))

            board.append(row)
        return cls(board)

    def __str__(self):
        sudoku = ''

        for row in self.board:
            for cell in row:
                if cell == 0:
                    sudoku += '_ '
                else:
                    sudoku += str(cell) + ' '
            sudoku += '\n'

        return sudoku

    def cols(self):
        """Return a sudoku where every list is a column."""
        return [[row[i] for row in self.board] for i in range(self.size)]


    def blanks(self):
        """Return the blank cells in a sudoku"""
        return [(colIndex, rowIndex)
                    for rowIndex, row  in enumerate(self.board)
                    for colIndex, cell in enumerate(row) if cell == 0]

    def blockIndex(self, row, col):
        """Return the row index of a block formatted sudoku list, given the
        sudoku, row index and column index of a row formatted sudoku list.
        """
        block = int(sqrt(self.size))
        return int(col / block) + int(row / block) * block


    def blocks(self):
        """Return a sudoku where every list is a block."""
        block = int(sqrt(self.size))
        return [[ self.board[block * a + i][block * b + j]
                  for i in range(block) for j in range(block)]
                      for a in range(block) for b in range(block)]

    def remainingNumbers(self, row, col):
        sequence = self.board[row] + self.cols()[col] +\
            self.blocks()[self.blockIndex(row, col)]


        return ( i for i in range(1, self.size + 1) if i not in sequence )


    def isFormatted(self):
        """Checks whether a given sudoku is correctly formatted.

        It checks whether the size of the sudoku a square is and whether every row
        and every colomn are the same size.
        """
        colLength = len(self.board)

        # Check if the sudoku size is a square, use EPSILON to compare floats.
        if abs(sqrt(colLength) - int(sqrt(colLength))) > EPSILON:
            return False

        # Check if every row in the sudoku is the same size as the column size.
        for row in self.board:
            if len(row) != colLength:
                return False

        return True

    def isValid(self):
        return not validList(self.board) or\
            validList(self.cols()) or\
            validList(self.blocks())

    def setCell(self, row, col, value):
        self.board[row][col] = value

    def getCell(self, row, col):
        return self.board[row][col]

def solve(sudoku):
    blanks = sudoku.blanks()

    if len(blanks) == 0:
        return True

    col, row = blanks[0]

    for i in sudoku.remainingNumbers(row, col):
        sudoku.setCell(row, col, i)

        if solve(sudoku):
            return True

        sudoku.setCell(row, col, 0)

    return False

if __name__ == "__main__":
    try:
        sudoku = Sudoku.fromStdIn()

        if not sudoku.isFormatted():
            raise ValueError("This is not a valid formatted sudoku")
        if not sudoku.isValid():
            raise ValueError("This sudoku may have duplicate digits.")

        solve(sudoku)
        print(sudoku)

    except ValueError as e:
        print(e)

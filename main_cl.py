'''
A simple command line 2048 game using W/S/A/D to move.

* Dependencies:
numpy, argparse

* Usage:
    python main_cl.py (default 4x4 board)
Or
    python mian_cl.py --width N --height M (NxM board)

* Written by Eason Chen
* 07/06/2017

$$TODO:
- GUI or web-based interface

'''

import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('--width', type=int, default=4)
parser.add_argument('--height', type=int, default=4)

args = parser.parse_args()

WIDTH = args.width
HEIGHT = args.height

class Board:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.is_finished = 0
        self.board = np.zeros((height, width), dtype=int)
        self.add_piece()

    # get the max piece of current board
    def max(self):
        return self.board.max()

    # randomly add a 2 or 4 piece to an empty spot
    def add_piece(self):
        x, y = np.where(self.board == 0) # find empty spot
        num = np.random.random_integers(0, 1)*2+2 # random add 2 or 4
        idx = np.random.choice(range(len(x)))
        xi, yi = x[idx], y[idx]
        self.board[xi][yi] += num

    # move the board by command up/down/left/right
    # return the new board
    def update(self, command):
        new_board = np.copy(self.board)
        if command == 'a':
            for i in range(self.height):
                line = new_board[i, :]
                merged_line = self.merge_line(line)
                new_board[i, :] = merged_line
        if command == 'd':
            for i in range(self.height):
                line = new_board[i, ::-1]
                merged_line = self.merge_line(line)
                new_board[i, :] = merged_line[::-1]
        if command == 'w':
            for i in range(self.height):
                line = new_board[:, i]
                merged_line = self.merge_line(line)
                new_board[:, i] = merged_line
        if command == 's':
            for i in range(self.height):
                line = new_board[::-1, i]
                merged_line = self.merge_line(line)
                new_board[:, i] = merged_line[::-1]
        return new_board

    # merge a line after a command
    def merge_line(self, line):
        N = len(line)
        line_nz = line[np.nonzero(line)]
        M = len(line_nz)
        for i in range(M-1):
            if line_nz[i] == line_nz[i+1]:
                line_nz[i] += line_nz[i+1]
                if i+2 < M:
                    line_nz[i+1:-1] = line_nz[i+2:]
                    line_nz[-1] = 0
                else:
                    line_nz[-1] = 0
        return np.lib.pad(line_nz, (0, N-M), 'constant', constant_values=0)

    # check if the current game is stuck (dead)
    def is_stuck(self):
        board_a, board_s, board_d, board_w = self.update('a'), self.update('s'),\
                                             self.update('d'), self.update('w')
        x, y = np.where(self.board == 0)
        return (np.array_equal(self.board, board_a) and
                np.array_equal(self.board, board_s) and
                np.array_equal(self.board, board_d) and
                np.array_equal(self.board, board_w) and
                len(x) == 0)

    # display the board in command line.
    # Note: the appearance is not optimized
    def draw(self):
        print('\n\n\n\n\n')
        print('-----------------')
        for i in range(self.height):
            line = '|'
            for j in range(self.width):
                line += ' {} |'.format(self.board[i, j])
            print(line)
            print('-----------------')

    # run the main game
    def run(self):
        self.draw()
        while True:
            command = input("Type W, S, A, D for up/down/left/right: ").lower()
            if command in ['w', 's', 'a', 'd']:
                new_board = self.update(command)
                if not np.array_equal(new_board, self.board):
                    self.board = new_board
                    self.add_piece()
                self.draw()
                if self.max() == 2048:
                    print('Congratulations! You get to 2048!')
                    break
                if self.is_stuck(): # stuck
                    print('Sorry, you failed.')
            else:
                print('Wrong command.')



if __name__ == '__main__':
    board = Board(WIDTH, HEIGHT)
    board.run()

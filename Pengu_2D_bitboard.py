#%% change log/update history
# -*- coding: utf-8 -*-
"""
CS 5400 Introduction to Artificial Intelligence
Jeremiah Rittenhouse
Graduate Student, Missouri University of Science and Technology
"""

"""
Began code 3/12/2022

Goal: Implement bitboard method to store Pengu game states, moves, etc.
"""

#%% imports

# custom imports

import sys 
# from 
# https://stackoverflow.com/questions/16179875/command-line-input-in-python
#arg1 = sys.argv[1]
#arg2 = sys.argv[2]

import time # for looking at how long things are taking
import numpy as np

#%% global/top variables

# this is num key format, the index will correspond to column and row effect in
# the below row_fx and col_fx "table" (suggested by Dr. Morales in class)
possible_moves = [1,2,3,4,6,7,8,9]

# table of movement effects based on row and column
# adding one to row goes DOWN a row
# adding one to a col goes RIGHT one col
row_fx = [1, 1, 1, 0, 0,-1,-1,-1] # e.g. a '1' move goes down and left, so
col_fx = [-1, 0, 1,-1, 1,-1, 0, 1] # add 1 to row, subtract 1 from column

def move_parse(move_key):
    """Given a move, map it into row_fx and col_fx indices."""
    move_idx = possible_moves.index(move_key)
    return(move_idx)
# end def move_parse

#%% class definitions

class PenguGame:
    """
    Holds all the information related to a state of the Pengu game. Do this
    using bitboards of [walls, ice, fish, snow, pengu, hazards].
    
    Init takes board, position tuple
    
    Consider future expansion to improve checking visited states capability.
    """
    
    def __init__(self,walls,ice,fish,snow,pengu,bears,sharks,score):
        self.walls = walls
        self.ice = ice
        self.fish = fish
        self.snow = snow
        self.pengu = pengu
        self.bears = bears
        self.sharks = sharks
        
        self.score = score
        
        self.rows = walls.shape[0]
        self.cols = walls.shape[1]
    # end def __init__
    
    def __repr__(self):
        # walls = self.walls.reshape(self.rows*self.cols)
        # ice = self.ice.reshape(self.rows*self.cols)
        # fish = self.fish.reshape(self.rows*self.cols)
        # snow = self.snow.reshape(self.rows*self.cols)
        # pengu = self.pengu.reshape(self.rows*self.cols)
        # hazards = self.hazards.reshape(self.rows*self.cols)
        
        state_string = ''
        
        for i in range(self.walls.shape[0]):
            for j in range(self.walls.shape[1]):
                if self.walls[i,j]:
                    state_string = state_string+'#'
                elif (self.pengu[i,j] and self.bears[i,j] 
                      or self.pengu[i,j] and self.sharks[i,j]
                      ):
                    state_string = state_string+'X'
                elif self.pengu[i,j]:
                    state_string = state_string+'P'
                elif self.fish[i,j]:
                    state_string = state_string+'*'
                elif self.snow[i,j]:
                    state_string = state_string+'0'
                elif self.ice[i,j]:
                    state_string = state_string+' '
                elif self.bears[i,j]:
                    state_string = state_string+'U'
                elif self.sharks[i,j]:
                    state_string = state_string+'S'
            # end j loop
            state_string = state_string+'\n'
        # end i loop
        state_string = state_string+'fish remaining = '+str(self.score)
        return(state_string)
    # end def __repr__
    
    def list_valid_moves(self):
        """
        Use masks to create the valid moves based on Pengu's position and
        the game state. 
        """
        # indices of list_of_moves
        # 0 = all false, 
        # 1 = true along lower right diagonal
        # 2 = true vertically down
        # 3 = true along lower right antidiagonal
        # 4 = true horizontally left
        # 5 = all false
        # 6 = true horizontally right
        # 7 = true along upper left antidiagonal
        # 8 = true vertically up
        # 9 = true upper right diagonal
        list_of_moves = [np.zeros((self.rows,self.cols),dtype=bool)]*10
        
        p_row = np.where(self.pengu == True)[0][0]
        p_col = np.where(self.pengu == True)[1][0]
        
        diag_mask = np.logical_xor(np.tri(self.rows,self.cols,p_col-p_row),
                                   np.tri(self.rows,self.cols,p_col-p_row-1)
                                   )
        adiag_mask = np.fliplr(
            np.logical_xor(np.tri(self.rows,self.cols,self.cols-p_col),
                           np.tri(self.rows,self.cols,self.cols-p_col-1))
            )
        
        #1_mask = np.fliplr
        return(diag_mask,adiag_mask)
    
    #def make_move(self,move_key)

#%% function definitions

def get_board_from_file(filename_in):
    """
    Given a filename, read the file and return a PenguGame object of the
    game and board states. 
    """
    data = open(filename_in,"r") # open the file in read mode 
    # I know the first line of the input file has the number of rows, space
    # number of columns in the game board.
    
    # Store the first line of the input file.
    input_file_header = data.readline() 
    # Now looking at the next line of the input file. (Board characters)
    
    board_rows = int(input_file_header.split()[0])
    board_cols = int(input_file_header.split()[1])
    
    # Initialize an empty bitboard to copy for making the game state.
    bitboard = np.zeros((board_rows,board_cols),
                        dtype=bool
                        )
    
    walls = np.copy(bitboard)
    ice = np.copy(bitboard)
    fish = np.copy(bitboard)
    snow = np.copy(bitboard)
    pengu = np.copy(bitboard)
    bears = np.copy(bitboard)
    sharks = np.copy(bitboard)
    
    # Populate the bitboards with the characters from the input file.
    # i is file line index, line is text line
    # j is character index, character is the board symbol
    for i,line in enumerate(data):
        for j,character in enumerate(line): 
            if character == '\n': # Ignore the newline characters.
                pass
            # end if newline
            else: # Happens if character is not a newline character.
                if character == '#': # indicates a wall
                    walls[i,j] = 1
                elif character == ' ': # indicates an ice cell
                    ice[i,j] = 1
                elif character == '*': # indicates an ice cell with a fish
                    fish[i,j] = 1
                    ice[i,j] = 1
                elif character == '0': # indicates a snow cell
                    snow[i,j] = 1
                elif character == 'P': # indicates pengu's initial location
                    pengu[i,j] = 1
                    ice[i,j] = 1 # because ice behind pengu's start location
                elif character == 'U': # indicates a bear cell
                    bears[i,j] = 1
                elif character == 'S': # indicates a shark cell
                    sharks[i,j] = 1
                # end if/elses populating board
            # end newline/else case handling
        # end j loop
    # end i loop
    return(PenguGame(walls,ice,fish,snow,pengu,bears,sharks,0))
# end def get_board_from_file

#%% import the board from file

sys_arg_testing = False
print_boards = True

if sys_arg_testing:
    # argv[0] = name of the program, PenguMain.py
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
else:
    input_filename='input_file_hw3.txt'
    output_filename='output_file.txt'
# end if else for arg testing or default input

game_start = get_board_from_file(input_filename)
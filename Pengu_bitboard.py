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
    
    #def __init__(self,size,dict_in,score):
    def __init__(self,size,list_in,score):
        #"""
        self.walls = list_in[0]
        self.ice = list_in[1]
        self.fish = list_in[2]
        self.snow = list_in[3]
        self.pengu = list_in[4]
        self.bears = list_in[5]
        self.sharks = list_in[6]
        """
        self.walls = dict_in['walls']
        self.ice = dict_in['ice']
        self.fish = dict_in['fish']
        self.snow = dict_in['snow']
        self.pengu = dict_in['pengu']
        self.bears = dict_in['bears']
        self.sharks = dict_in['sharks']
        """
        
        self.score = score
        
        self.rows = size[0]
        self.cols = size[1]
    # end def __init__
    
    def __repr__(self):
        # walls = self.walls.reshape(self.rows*self.cols)
        # ice = self.ice.reshape(self.rows*self.cols)
        # fish = self.fish.reshape(self.rows*self.cols)
        # snow = self.snow.reshape(self.rows*self.cols)
        # pengu = self.pengu.reshape(self.rows*self.cols)
        # hazards = self.hazards.reshape(self.rows*self.cols)
        
        state_string = ''
        index = 0
        
        for i in range(self.rows[0]):
            for j in range(self.cols[1]):
                if self.walls[index]:
                    state_string = state_string+'#'
                elif (self.pengu[index] and self.bears[index] 
                      or self.pengu[index] and self.sharks[index]
                      ):
                    state_string = state_string+'X'
                elif self.pengu[index]:
                    state_string = state_string+'P'
                elif self.fish[index]:
                    state_string = state_string+'*'
                elif self.snow[index]:
                    state_string = state_string+'0'
                elif self.ice[index]:
                    state_string = state_string+' '
                elif self.bears[index]:
                    state_string = state_string+'U'
                elif self.sharks[index]:
                    state_string = state_string+'S'
                # end if/elif handling characters
                index = index+1
            # end j loop
            state_string = state_string+'\n'
        # end i loop
        state_string = state_string+'fish remaining = '+str(self.score)
        return(state_string)
    # end def __repr__
    
    #def list_valid_moves(self)
    
    #def make_move(self,move_key)

#%% function definitions

def append_zero_char(string_in):
    """Given a string, append '0' to it and return it."""
    #string_out = string_in.append('0')
    string_out = string_in+'0'
    return(string_out)
# end def append_zero_char

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
    
    rows = int(input_file_header.split()[0])
    cols = int(input_file_header.split()[1])
    
    # walls = '0'*board_rows*board_cols
    # ice = '0'*board_rows*board_cols
    # fish = '0'*board_rows*board_cols
    # snow = '0'*board_rows*board_cols
    # pengu = '0'*board_rows*board_cols
    # bears = '0'*board_rows*board_cols
    # sharks ='0'*board_rows*board_cols
    
    # game_dict = {'walls':[],
    #              'ice':[],
    #              'fish':[],
    #              'snow':[],
    #              'pengu':[],
    #              'bears':[],
    #              'sharks':[]}
    
    walls = ''
    ice = ''
    fish = ''
    snow = ''
    pengu = ''
    bears = ''
    sharks =''
    
    game_list = [walls,ice,fish,snow,pengu,bears,sharks]
    
    index = 0
    # Populate the bitboards with the characters from the input file.
    # i is file line index, line is text line
    # j is character index, character is the board symbol
    for i,line in enumerate(data):
        for j,character in enumerate(line): 
            # walls=0,ice=1,fish=2,snow=3,pengu=4,bears=5,sharks=6
            append_zero_to = [1,1,1,1,1,1,1]
            
            if character == '\n': # Ignore the newline characters.
                pass
            # end if newline
            else: # Happens if character is not a newline character.
                if character == '#': # indicates a wall
                    #walls[index] = '1'
                    walls = walls+'1'
                    append_zero_to[0] = 0
                    #game_dict['walls'] = game_dict['walls'].append('1')
                    #append_zero_to.append(['ice','fish','snow',
                    #                       'pengu','bears','sharks'])
                elif character == ' ': # indicates an ice cell
                    #ice[index] = '1'
                    ice = ice+'1'
                    append_zero_to[1] = 0
                    #game_dict['ice'] = game_dict['ice'].append('1')
                    #append_zero_to.append(['walls','fish','snow',
                    #                       'pengu','bears','sharks'])
                elif character == '*': # indicates an ice cell with a fish
                    #fish[index] = '1'
                    #ice[index] = '1'
                    fish = fish+'1'
                    ice = ice+'1'
                    append_zero_to[1] = 0
                    append_zero_to[2] = 0
                    #game_dict['fish'] = game_dict['fish'].append('1')
                    #game_dict['ice'] = game_dict['ice'].append('1')
                    #append_zero_to.append(['walls','snow','pengu',
                    #                       'bears','sharks'])
                elif character == '0': # indicates a snow cell
                    #snow[index] = '1'
                    snow = snow+'1'
                    append_zero_to[3] = 0
                    #game_dict['snow'] = game_dict['snow'].append('1')
                    #append_zero_to.append(['walls','ice','fish',
                    #                       'pengu','bears','sharks'])
                elif character == 'P': # indicates pengu's initial location
                    #pengu[index] = '1'
                    #ice[index] = '1' # ice behind pengu's start location
                    pengu = pengu+'1'
                    ice = ice+'1'
                    append_zero_to[1] = 0
                    append_zero_to[4] = 0
                    #game_dict['pengu'] = game_dict['pengu'].append('1')
                    #game_dict['ice'] = game_dict['ice'].append('1')
                    #append_zero_to.append(['walls','fish','snow',
                    #                       'bears','sharks'])
                elif character == 'U': # indicates a bear cell
                    #bears[index] = '1'
                    bears = bears+'1'
                    append_zero_to[5] = 0
                    #game_dict['bears'] = game_dict['bears'].append('1')
                    #append_zero_to.append(['walls','ice','fish',
                    #                       'snow','pengu','sharks'])
                elif character == 'S': # indicates a shark cell
                    #sharks[index] = '1'
                    sharks = sharks+'1'
                    append_zero_to[6] = 0
                    #game_dict['sharks'] = game_dict['sharks'].append('1')
                    #append_zero_to.append(['walls','ice','fish',
                    #                       'snow','pengu','bears'])
                # end if/elses populating board
            # end newline/else case handling
            """index = index+1"""
            #print(append_zero_to)
            for index,key in enumerate(append_zero_to):
                if key:
                    game_list[index] = append_zero_char(game_list[index])
                #print(key)
                #game_dict[key] = append_zero_char(game_dict[key])
                #print(game_dict[key])
        # end j loop
    # end i loop
    #print(game_dict['walls'])
    #return(PenguGame((rows,cols),game_dict,0))
    return(PenguGame((rows,cols),game_list,0))
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
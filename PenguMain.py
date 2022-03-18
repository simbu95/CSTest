#%% imports

import sys 
import time

# custom imports
from Pengu_fcns import PenguGameBoard

from Pengu_fcns import board_from_string

from Pengu_fcns import pick_random_move
from Pengu_fcns import IDDFS_algorithm
from Pengu_fcns import goal_hw2, goal_hw3

#%% get board from input file

sys_arg_testing = False
print_boards = False
do_IDDFS_solution = True #If your going to do options like this, put them all at the top... I am not searching your file to find what options I can or can't do. 
end_game_printouts = True
print_to_output_file = True


if sys_arg_testing:
    # argv[0] = name of the program, PenguMain.py
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
else:
    input_filename='input_file_hw3.txt'
    output_filename='output_file.txt'

data = open(input_filename, "r")  # open infile in read mode

# the first line of the input file has the number of rows, 
# space, number of columns

#Honestly you should implement a read from file function in your game board class, and seperate game board from your AI stuff, but details... 
#When doing program control, its easier if the main function quickly shows you the direction, and the other files do the hardwork.
input_file_header = data.readline() # first get the entire line

split_header = input_file_header.split() # split the line

board_rows = int(split_header[0]) # convert first number character to # of rows
board_cols = int(split_header[1]) # second to # of columns

# initialize empty board
board_array = ([['']*board_cols for i in range(board_rows)]) 

# populate the board with the characters from the input file
for i,line in enumerate(data): # i is the file line index, line is text line
    # j is character index, character is the board symbol
    for j,character in enumerate(line): 
        if character == '\n': # ignore the newline character at the end of each
            pass              # line in the file
        # end if newline
        else: # this happens if character is not a newline character
            if character == 'P':    # if character is 'P' create tuple of his 
                pengu_pos = [i,j]   # row, column coordinates (from top left)
                character = ' ' # put ice on board behind pengu start position
            # end if handling Pengu position
            board_array[i][j] = character # put character on the board as long
                # as it is not a newline character or pengu's position
        # end newline/else case handling
    # end j loop
# end i loop

this_game_start = PenguGameBoard(board_array,pengu_pos,0)

#%% do IDDFS algorithm
if do_IDDFS_solution:
    
    # keep track of total time elapsed doing the algorithm
    time_before = time.time()
    
    # get the goal path using the IDDFS algorithm
    IDDFS_goal_path = IDDFS_algorithm(this_game_start,goal_hw3)
    
    move_history = IDDFS_goal_path
    
    if print_boards:
        # print the initialized board. It should match the input file board.
        pretty_print_board(this_game_start)
    # end if print_boards
    
    # carry out the solution moves to get Pengu's position and score
    end_game_state = this_game_start.make_list_of_moves(move_history)
    
    time_taken = time.time()-time_before
    print('IDDFS elapsed time was '+f'{time_taken:2f}')
# end if do_IDDFS_solution


pengu_pos = end_game_state.position
pengu_score = end_game_state.score
board_array = end_game_state.board

if end_game_printouts:
    if print_boards:
        # print the initialized board. It should match the input file board.
        #pretty_print_board(board_array,pengu_pos)
        pretty_print_board(end_game_state)
    # end if print_boards
    print('pengu pos = '+str(pengu_pos))
    print('pengu pts = '+str(pengu_score))
    print('move history = '+str(move_history[1:])+
          ' length = '+str(len(move_history[1:])))
    print('fish remaining = '+str(end_game_state.count_fish()))
# end if end_game_printouts

#%% print the output file

if print_to_output_file:
    # open output file to write the game to
    f = open(output_filename,'w')   # ,w means write over/clear existing file
    
    # write the move history at the top of the file
    for index,move_key in enumerate(move_history):
        if move_key != 0:
            f.write(str(move_key)) # write the move in num key format
        # end if checking "no move" move key at the beginning of the output
    # end for through move history
    
    # next line gets pengu's score
    f.write('\n'+str(pengu_score))
    
    # close and reopen the file in append mode
    f.close()
    f = open(output_filename,'a') # ,a means append output to end of the file
    
    # abbreviate row and column for convenience
    p_row = pengu_pos[0]
    p_col = pengu_pos[1]
    
    # print the board to the file
    for i,row in enumerate(board_array):
        # start with a newline for each row. Keeps a blank line from being
        # written at the end of the file.
        f.write('\n')
        
        # go through the characters in the row of the board
        for j,char in enumerate(row):
            # handle case where Pengu is standing on a snow patch or hazard
            if i == p_row and j == p_col: # if printing where pengu is standing
                # handle the case where pengu is on a hazard = dead
                if (board_array[p_row][p_col] == 'S' # shark death
                        or board_array[p_row][p_col] == 'U'): # bear death
                    f.write('X') # both get an X for pengu
                else:
                    f.write('P') # otherwise, write P for pengu's location
                # end if else handling pengu's position
            else:
                f.write(char)
            # end if else writing board characters
        # end for loop through characters within the row
    # end for loop through rows
    f.close() # close the file
# end if print_to_output_file
#%% imports

import sys 
import time

# custom imports
from PenguBoard import goal_hw2, goal_hw3
from PenguIDDFS import IDDFS_algorithm
import PenguUtil

sys_arg_testing = False
print_boards = True
do_IDDFS_solution = True #If your going to do options like this, put them all at the top... I am not searching your file to find what options I can or can't do. 
end_game_printouts = True
print_to_output_file = True

#%% get board from input file
if sys_arg_testing:
    # argv[0] = name of the program, PenguMain.py
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
else:
    input_filename='input_file_hw3.txt'
    output_filename='output_file.txt'

this_game_start = PenguUtil.readPenguBoardFile(input_filename)

#%% do IDDFS algorithm
if do_IDDFS_solution:
    
    # keep track of total time elapsed doing the algorithm
    time_before = time.time()
    
    # get the goal path using the IDDFS algorithm
    IDDFS_goal_path = IDDFS_algorithm(this_game_start,goal_hw3)
    
    move_history = IDDFS_goal_path
    
    if print_boards:
        # print the initialized board. It should match the input file board.
        this_game_start.pretty_print_board()
    # end if print_boards
    
    # carry out the solution moves to get Pengu's position and score
    end_game_state = this_game_start.make_list_of_moves(move_history)
    
    time_taken = time.time()-time_before
    print('IDDFS elapsed time was '+f'{time_taken:2f}')
# end if do_IDDFS_solution



if end_game_printouts:
    PenguUtil.endGamePrintouts(end_game_state,move_history,print_boards)

#%% print the output file

if print_to_output_file:
    PenguUtil.printToOutputFile(end_game_state,move_history,output_filename)
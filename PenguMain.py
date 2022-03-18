#%% change log/update history
# -*- coding: utf-8 -*-
"""
CS 5400 Introduction to Artificial Intelligence
Jeremiah Rittenhouse
Graduate Student, Missouri University of Science and Technology

2/11/2022
"""

"""
Began code 2/11/2022
My plan is to use a 2D array to store the board and a row, column location to
keep track of Pengu location.
"""

"""
Pengu game working 2/15/2022
Luckly I caught the '6 move limit' rule. I almost missed that. Currently the 
only problem I know of in my code is duplicated functionality to f.write() the
output file and pretty_print_board() print the board to the console.

Going through code and commenting it now.
"""

"""
I think homework 1 is completely ready to submit. My goal now, 2/21/2022, is to
start programming the generic search algorithm, first using BFS. From class, 
the generic search algorithm looks like:

FUNCTION: GenericGraphSearch

INPUT: A graph
       A start state, s
       A goal() function

BEGIN:
    frontier = {[s]}
    
    WHILE frontier is not empty:
        select path p = [n0, n1, n2, ..., nk]
        
        IF goal(nk):
            RETURN p
        ELSE:
            FOR every neighbor nk+1 of nk:
                insert [n0, n1, n2, ..., nk, nk+1] to frontier
"""


"""
Begin trying to implement BFS 3/2/2022.

My plan is to keep all the functions in Pengu_fcns.py. We'll see how it goes!
My only concern right now is that the generic search algorithm takes a "graph"
input. How do I send the graph to the BFS algorithm? Is it just sending the 
Pengu game board?
"""

"""
Before class on 3/2/2022, I think I have it working!

Method: BFS_algorithm uses action keys to store path and state information. I
do not store the game board at each state, I only store the list of actions. 
Therefore, I recalculate the game state by carrying out the "move history" 
list each time through the frontier loop. 

BFS_algorithm walkthrough:
    first, select and remove a path
    calculate the board and game state resulting from following that path
    check goal function (did pengu earn 8 points yet?)
    check game end (do not extend frontier paths where pengu is dead or all
                    fish are gone)
    extend frontier with available moves from the current state
# loop

In order to implement the algorithm with the initial state, I added a "0" to
the action key list, which means "no action". This is not a valid move, but
I use it to start the algorithm. I then trim the leading zero from the move
history at the print to output file stage.

The other detail I'm not the happiest with is that I have two similar goal-
ish functions. One to check game end via death or zero fish remaining, the
other to check if Pengu gained 8 points. Two separate checks were useful in
the BFS_algorithm because even though the game ends at Pengu death, the 
algorithm should NOT return the path to that ending, because it does not
satisfy the goal.
"""

"""
Began trying to implement ID-DFS 3/10/2022

4pm on 3/10, I got majorly distracted writing a function to encode a board
to a string and another function to decode the string to a board. My plan
was to use the string encoding to store game states for pruning the search
space (don't search duplicates of the same state). Now I am working on 
changing the "board_in,pengu_pos" functions and arguments to use a new
PenguGameBoard class.
"""

"""
Working on ID-DFS 3/11/2022

I think I have basic ID-DFS working without any search pruning. I'm getting
a correct goal path according to Discord responses. However, it takes 7 min
to reach that goal path. 

After implementing a hash method to prune the search tree, I can get to ~12
seconds on my PC. However, my goal path length is 17, not optimal. :(
"""

"""
Working on pruning ID-DFS 3/12/2022

After sacrificing a bunch of brain cells, I got my hash method working by
including the path length in the hash table. I used some tricky array
indexing/slicing to do a numpy array for speed, and it works as fast as
the nonoptimal 17 length path. I got 24 points on the hw3 example in 16
seconds and 19 moves. Unfortunately, I hit run on the 2500by2500 board,
and it revealed that my hash method is crippled by large size. :( My hash
function uses "string_from_board" that stores way more information from the
board than it needs to. Aaand it becomes very slow to process a large board.

I'm considering reprogramming the entire code to store the game state more
efficiently...but my time turner isn't working today yet.
"""

#%% imports

# custom imports
from Pengu_fcns import PenguGameBoard

from Pengu_fcns import string_from_board, board_from_string

from Pengu_fcns import pretty_print_board, list_valid_moves, pick_random_move
from Pengu_fcns import make_move, count_fish, check_game_end

from Pengu_fcns import BFS_algorithm, make_list_of_moves
from Pengu_fcns import IDDFS_algorithm
from Pengu_fcns import goal_hw2, goal_hw3

import sys 
# from 
# https://stackoverflow.com/questions/16179875/command-line-input-in-python
#arg1 = sys.argv[1]
#arg2 = sys.argv[2]

import time # for looking at how long things are taking

#%% get board from input file

sys_arg_testing = False
spyder_console_testing = False
print_boards = False

if sys_arg_testing:
    # argv[0] = name of the program, PenguMain.py
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
elif spyder_console_testing:
    # Input data file on spyder console line:
    input_line = input('enter the input filename, space, '+
                       'output filename here\n'
                       )
    input_filename = input_line.split()[0] # first input is the input file name
    output_filename = input_line.split()[1] # 2nd is output file name
else:
    input_filename='input_file_hw3.txt'
    output_filename='output_file.txt'


# G:\My Drive\School and Semester Stuff\2022 Spring\CS5400_Intro_to_AI\Hw02
'''
filepath = (r'G:/My Drive/School and Semester Stuff/2022 Spring/'+
            'CS5400_Intro_to_AI/Hw02/')
'''
filepath = ''
infile = (filepath+input_filename)
data = open(infile, "r")  # open infile in read mode

# it is known that the first line of the input file has the number of rows, 
# space, number of columns

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

#%% pick random move until game end

do_random_moves = False

if do_random_moves:
    move_history = []   # empty list holds the move history
    pengu_score = 0     # holds pengu's score
    
    # initialize a copy of the game board by making a zero move
    updated_game = make_move(this_game_start,0)
    #print('updated_game is type')
    #print(type(updated_game))
    
    # loop until game end condition (death or all fish gathered),
    # or 6 moves happen
    #while (check_game_end(board_array,pengu_pos) != True 
    while (check_game_end(updated_game) != True 
           and len(move_history) < 6):
        
        # first create a list of valid moves to choose from (num key format)
        #valid_moves = list_valid_moves(board_array,pengu_pos)
        valid_moves = list_valid_moves(updated_game)
        
        # pick a random move (num key format)
        move_key = pick_random_move(valid_moves)
        move_history.append(move_key) # add the move to the move history
        
#        (updated_board, # update the board, pengu position, find any points
#         pengu_pos,     # that were gained by the random move
#         points_gained
#        ) = make_move(board_array,pengu_pos,move_key)
        updated_game = make_move(updated_game,move_key)
        
        # add any points gained to pengu's score 
        # (just adds 0 if no points gained)
        #pengu_score = pengu_score+points_gained
        
        # print the board to the console after each move
        #pretty_print_board(board_array,pengu_pos)
        pretty_print_board(updated_game)
    # end while loop
    end_game_state = updated_game
# end if do_random_moves

#%% do BFS algorithm

do_BFS_solution = False

if do_BFS_solution:
    
    # keep track of total time elapsed doing the algorithm
    time_before = time.time()
    
    # get the goal path using the BFS algorithm
    #BFS_goal_path = BFS_algorithm(board_array,pengu_pos)
    BFS_goal_path = BFS_algorithm(this_game_start)
    
    move_history = BFS_goal_path
    
    if print_boards:
        # print the initialized board. It should match the input file board.
        #pretty_print_board(board_array,pengu_pos)
        pretty_print_board(this_game_start)
    # end if print_boards
    
    # carry out the solution moves to get Pengu's position and score
    end_game_state = make_list_of_moves(this_game_start,move_history)
    
    time_taken = time.time()-time_before
    print('elapsed time was '+str(time_taken))
# end if do_BFS_solution


#%% do IDDFS algorithm

do_IDDFS_solution = True

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
    end_game_state = make_list_of_moves(this_game_start,move_history)
    
    time_taken = time.time()-time_before
    print('IDDFS elapsed time was '+f'{time_taken:2f}')
# end if do_IDDFS_solution

#%% play pengu in console

pengu_in_console = False

# just play pengu via manual input to the console
if pengu_in_console:
    
    # track moves and score
    move_number = 0
    move_history = []
    pengu_score = 0
    
    updated_board = make_move(this_game_start,0)
    
    #while check_game_end(board_array,pengu_pos) != True:
    while check_game_end(updated_board) != True:
        # print game state and info
        #pretty_print_board(board_array,pengu_pos)
        #print('Move history: '+str(move_history)+
        #      ', move number '+str(move_number)+
        #      ', score = '+str(pengu_score))
        
        pretty_print_board(updated_board)
        
        # Input move key on spyder console line:
        input_move = input('Enter the move key:\n')
        
        input_move = int(input_move)
        move_history.append(input_move)
        
        # update the board and game state with the new move
        #(board_array,
        # pengu_pos,
        # points_gained
        # ) = make_move(board_array,pengu_pos,input_move)
        updated_board = make_move(updated_board,input_move)
        
        #pengu_score = pengu_score+points_gained
        
        move_number = move_number+1
    # end while check_game_end not true
    
    end_game_state = updated_board
# end if pengu_in_console

#%% end game printouts
# print some information to the console after finishing the play loop
# maybe delete these after testing

end_game_printouts = True

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
    print('fish remaining = '+str(count_fish(board_array)))
# end if end_game_printouts

#%% print the output file

print_to_output_file = True

if print_to_output_file:
    #output_filename = 'output_test.txt' # for manual testing
    
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
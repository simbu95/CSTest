#%% imports
import random # for random.choice() to get a random move
from collections import deque # for the deque object
import sys # to check frontier size
import time # for optimization testing
import numpy as np # for hash storage

#%% global variables

# this is num key format, the index will correspond to column and row effect in
# the below row_fx and col_fx "table" (suggested by Dr. Morales in class)
possible_moves = [0,1,2,3,4,6,7,8,9]

# table of movement effects based on row and column
# adding one to row goes DOWN a row
# adding one to a col goes RIGHT one col
row_fx = [0, 1, 1, 1, 0, 0,-1,-1,-1] # e.g. a '1' move goes down and left, so
col_fx = [0,-1, 0, 1,-1, 1,-1, 0, 1] # add 1 to row, subtract 1 from column

# board string encoding/decoding variables
board_string_line_end = '/'
board_string_header_separator = '|'
board_string_tile_separator = ','

board_tile_chars = set(['#',' ','*','S','U','0'])

#%% Pengu class
def move_parse(move_key):
    """Given a move, map it into row_fx and col_fx indices."""
    move_idx = possible_moves.index(move_key)
    return(move_idx)
    
def pick_random_move(valid_moves_list):
    """Given a list of num key moves, return a random one."""
    choice = random.choice(valid_moves_list)
    return(choice)

class PenguGameBoard:
    """
    Holds all the information related to a state of the Pengu game. That is,
    there is a 2D list of lists that holds the game board, a tuple of the
    coordinates of Pengu's position on the board, and a score number holding
    Pengu's current accumulated score.
    
    Init takes board, position tuple
    
    Consider future expansion to improve checking visited states capability.
    """
    
    def __init__(self,board_in,position_in,score_in,totalFish=None):
        self.board = board_in
        self.position = position_in
        self.score = score_in
        if(totalFish != None):
            self.totalFish = totalFish
        else:
            self.totalFish=self.count_fish()
    # end def __init__
    
    def __repr__(self):
        return(f'{self.board}\n'
               +f'pengu pos = {self.position}\n'
               +f'pengu pts = {self.score}'
               )
    
    def pretty_print_board(self):
        """
        Given a board state object, print it in pretty formatting to the console.
        """
        
        # abbreviate row and column for convenience
        p_row = self.position[0]
        p_col = self.position[1]
        
        # go through the board array and print to the console
        for i,row in enumerate(self.board):
            for j,char in enumerate(row):
                # need to handle case where Pengu is standing on a snow patch
                if i == p_row and j == p_col:
                    # must also handle the case where pengu is on a hazard = dead
                    if (self.board[p_row][p_col] == 'S' or 
                        self.board[p_row][p_col] == 'U'):
                        print('X',end='')
                    else:
                        print('P',end='')
                else:
                    print(char,end='')
                # end if handling pengu's position
            # end for loop through characters within the row
            print('\n',end='')
        # end for loop through rows
        print('Position is '+str(self.position)+', score is '+str(self.score))
    # end def pretty_print_board

    def list_valid_moves(self):
        """
        Given game state in, return a list of valid moves by key number.
        """
        valid_moves = [] # start with an empty list to add valid moves to
        
        # abbreviate row and column for convenience
        p_row = self.position[0]
        p_col = self.position[1]
        
        # go through the possible moves list and see if they can be completed
        for index,move_key in enumerate(possible_moves):
            
            if move_key == 0: # skip the 0th entry, 0 = no move
                continue
            move = move_parse(move_key)
            
            # get the board character/symbol of each possible move
            check_char = self.board[p_row+row_fx[move]][p_col+col_fx[move]]
            if check_char == '#':   # cannot move into a wall, do not add the move 
                pass                # to the valid moves list
            else:
                valid_moves.append(move_key) # otherwise add the move to the list
            # end character check
        # end for loop through possible moves by index
        return(valid_moves) # return the list of valid moves
    # end def list_valid_moves


# end def pick_random_move

    def copy_board(self):
        """
        Given a board, manually copy it. This is needed to avoid unexpected 
        copy behavior.
        """
        # manually copy output board 
        # otherwise python points to the entries in the input board and modifies
        # those, producing unexpected behavior
        board_rows = len(self.board)
        board_cols = len(self.board[0])
        # initialize empty board
        board_out = ([['']*board_cols for i in range(board_rows)]) 
        # copy the board
        for row_idx,row in enumerate(self.board):
            for col_idx,char in enumerate(row):
                board_out[row_idx][col_idx] = char
            # end for col_idx
        # end for row_idx
        return(board_out)
    # end def copy_board

    def string_from_board(self):
        board_string = ''
        endline_char = board_string_line_end
        last_tile = '' # won't match the first char, 'x' != '#'
        tile_count = 0
        
        pengu_row = self.position[0]
        pengu_col = self.position[1]
        
        board_rows = len(self.board)
        board_cols = len(self.board[0])
        
        # first entry in the string is pengu x and y coordinates
        board_string = (str(pengu_row)+board_string_header_separator
                        +str(pengu_col)+board_string_header_separator
                        +str(self.score)+board_string_header_separator
                        +str(board_rows)+board_string_header_separator
                        +str(board_cols)+board_string_header_separator
                        )
        
        for row_idx in range(board_rows):
            for col_idx in range(board_cols):
                this_tile = self.board[row_idx][col_idx]
                if this_tile == last_tile:
                    tile_count = tile_count+1
                    continue
                board_string = board_string+last_tile
                if tile_count != 0:
                    board_string = (board_string
                                    +str(tile_count)
                                    +board_string_tile_separator
                                    )
                # end if appending the tile count
                tile_count = 1 # because this tile is the first of its type
                last_tile = this_tile
            # end for col_idx
            board_string = board_string+last_tile+str(tile_count)
            if row_idx != board_rows-1: # don't add '/' at end of string
                board_string = board_string+endline_char
            tile_count = 0 # don't add another tile for each row
            last_tile = ''
        # end for row_idx
        return(board_string)
    # end def string_from_board

    def make_move(self,move_key):
        """
        Given a game state and a move key, return the game state after the move.
        """
        
        if move_key == 0: # 0 = no move
            return(self)
        # end if move == 0
        
        # convert num key move into the move table index to test moves
        move = move_parse(move_key)
        
        # abbreviate row and column for convenience
        p_row = self.position[0]
        p_col = self.position[1]
        
        board_out = self.copy_board()
        
        points_gained = 0 # will count any fish pengu's move picks up
        
        next_row = p_row+row_fx[move] # holds the first row of pengu's move
        next_col = p_col+col_fx[move] # first column of pengu's move
        
        # get the symbol in the first cell of pengu's move
        next_space_char = self.board[next_row][next_col] 
        
        # do the moving until a wall is reached
        while next_space_char != '#':
            
            # update pengu position before incrementing/continuing his move
            p_row = next_row
            p_col = next_col
            
            # handle the different board space encounters (snow, hazard, fish)
            # handle updating the board (remove '*' when a fish is collected)
            if self.board[p_row][p_col] == '*': # if a fish is picked up
                board_out[p_row][p_col] = ' ' # replace it with ice under fish
                points_gained = points_gained+1 # add a point for picking up fish
                #print('pengu gained a point')
            # handle the hazards
            elif self.board[p_row][p_col] == 'S' or self.board[p_row][p_col] == 'U':
                #print('broke in make_move for S or U')
                break # pengu stops if he dies
            elif self.board[p_row][p_col] == '0':
                #print('broke in make_move  for 0')
                break # pengu stops if he hits a snow patch
            # end if elifs handling fish, hazards, snow
            
            # next space indices
            next_row = p_row+row_fx[move]
            next_col = p_col+col_fx[move]
            
            # holds '#' when the next space is a wall
            next_space_char = self.board[next_row][next_col] # next cell symbol
        # end while loop
        
        pengu_position = (p_row,p_col) # update pengu's position
        
        game_out = PenguGameBoard(board_out,pengu_position,
                                  self.score+points_gained,self.totalFish)
        return(game_out)
    # end def make_move
    
    def make_list_of_moves(self,moves):
        """
        Given the game state and a list of moves, execute the moves in order and
        return the game state after the moves.
        """
        
        # first initialize variables by calling the make_move function with no move
        # i.e. copy the current board and position before starting the loop
        updated_game = self.make_move(0)
        
        # go through the passed list of moves and carry them out
        for index,move in enumerate(moves):
            updated_game = updated_game.make_move(move)
        return(updated_game)
    # end def make_list_of_moves

    def count_fish(self):
        """Given board, count the number of remaining fish."""
        the_count = 0 # increment for each existing fish
        
        # go through the board and increment the_count for each '*' found
        for i,row in enumerate(self.board):
            for j,char in enumerate(row):
                if char == '*':
                    the_count = the_count+1
                else:
                    pass
                # end if incrementing the_count for each '*' found
            # end j loop through cols within rows
        # end i loop through rows
        return(the_count)
    # end def count_fish

    def check_game_end(self):
        """
        Given board, pengu position, check if the game is over. Return True if 
        the game is over, return False if the game should continue.
        
        Logic: if pengu is atop a shark or bear, the game is over because death;
        if pengu is not atop any of the above, the game is over when all fish are
        collected (no fish are left on the board).
        """
        p_row = self.position[0]
        p_col = self.position[1]
        
        if self.board[p_row][p_col] == 'U' or self.board[p_row][p_col] == 'S':
            #print('Pengu is dead!')
            return(True)
        elif self.score >= self.totalFish:
            print('Pengu is a winner!')
            return(True)
        else:
            return(False)
        # end ifs handling whether the game ends or not
    # end def check_game_end
def decode_row(row_in):
    """
    Given an encoded row input, decode it into pengu tile notation.
    """
    row_out = ''
    
    row_split = row_in.split(board_string_tile_separator)
    
    for idx,encoded_tile in enumerate(row_split):
        the_tile = encoded_tile[0]
        number_of_tiles = int(encoded_tile[1:])
        row_out = row_out+the_tile*number_of_tiles
    # end for through the row
    return(row_out)
# end def decode_row

def board_from_string(string_in):
    """
    Parse a board string into an actual board. For the encoding method, see
    the string_from_board function docstring.
    """
    split_string = string_in.split(board_string_header_separator)
    #print(split_string)
    #print(type(split_string))
    pengu_row = int(split_string[0])
    #print(pengu_row)
    #print(type(pengu_row))
    pengu_col = int(split_string[1])
    #print(pengu_col)
    pengu_score = int(split_string[2])
    
    board_rows = int(split_string[3])
    #print(board_rows)
    board_cols = int(split_string[4])
    #print(board_cols)
    
    board_row_split = split_string[5].split(board_string_line_end)
    #print(board_row_split)
    
    # initialize empty board
    board_out = ([['']*board_cols for i in range(board_rows)])
    
    # populate the board with the correct characters
    for i in range(board_rows):
        encoded_row = board_row_split[i]
        #print(encoded_row)
        decoded_row = decode_row(encoded_row)
        board_out[i] = decoded_row
    # end for i in board rows
    
    #print(board_out)
    
    game_state_out = PenguGameBoard(board_out,
                                    (pengu_row,pengu_col),
                                    pengu_score
                                    )
    
    return(game_state_out)
# end def board_from_string

#***************************************************************************************************
#Everything below here should probably be in a different file, keep the Game State and AI seperate
#I would also recommend putting each AI into a different function if possible, and helper functions such as hashing in a util file, if they are shared. 
#***************************************************************************************************

#def goal_hw2(board_in,pengu_position,score):
def goal_hw2(score_in):
    """
    Given board, pengu position, and score, return True if goal is achieved,
    False otherwise.
    """
    
    if score_in >= 8:
        return(True)
    else:
        return(False)
    # end if checking goal
# end def goal_hw2

def goal_hw3(score_in):
    
    if score_in >= 20:
        return(True)
    else:
        return(False)
    # end if checking goal
# end def goal_hw3

#def BFS_algorithm(board_in,pengu_position):

def hash_check_BDFS(game_in,path_length,hash_table_in):
    """
    Given a game state, length, hash table, check the hash table for the game
    state. If the new path to the state is shorter, replace the existing
    hash. Otherwise, skip the current state (because it is a longer path
    to an explored state). Return boolean True if path should be extended,
    False if path should not be extended, and return the hash table.
    
    """
    hashed_board = hash(game_in.string_from_board()) # hash of game state string
    # hash table also needs the path length to compare and keep shorter paths
    # to visited states
    hash_table_entry = np.array([[hashed_board,path_length]])
    
    should_extend_path = True
    
    # check if the hashed game state string exists in the hash table
    if hash_table_entry[0,0] not in hash_table_in:
        # if the state has not been reached before, just append it
        hash_table_in = np.append(hash_table_in,
                                  hash_table_entry,
                                  axis=0
                                  )
    else: # need to check length of existing path vs current path to state
        # First, locate the matching game state in the hash table via a 
        # boolean masking method.
        # Mask holds 'True' where visited game state is equivalent to the
        # currently found game state.
        hash_row_mask = (hash_table_in == hashed_board)[:,0]
        # [:,0] goes through all the rows of hash table and looks only at the
        # hash, ignoring the path length column.
        
        # If the currently explored path to a previously found game state
        # is shorter than the stored state path length, replace previously
        # found (longer) path with the new path.
        if path_length < hash_table_in[hash_row_mask,1]:
            # Current path is shorter, replace the longer path hash in
            # hash_table_in with the current path to the same state
            hash_table_in[hash_row_mask,:] = hash_table_entry
            # [hash_row_mask,:] pulls out the matching game state row with
            # the path length column. Replace the matched game state and 
            # path length with the shorter (current) path.
        else:
            # Current path is longer, should not extend path to neighbors.
            should_extend_path = False
        # end if else checking path length
    # end if checking hashed board
    return(should_extend_path,hash_table_in)
# end def hash_check_BDFS

def BoundedDFS_algorithm(game_in,goal_fcn,depth_limit):
    numits = 0
    move_history = [0,] 
    
    depth_hit = False
    frontier = deque([move_history])
    
    # hash table
    explored_hashes = np.empty((0,2))
    
    while frontier != deque([]): # while frontier is not empty
        
        numits = numits+1
        
        # select and remove a path
        selected_history = frontier.pop() # remove the last in path (select and remove)
        updated_board = game_in.make_list_of_moves(selected_history)
        move_options = updated_board.list_valid_moves()
        
        if len(selected_history) == depth_limit: 
            if goal_fcn(updated_board.score):
                return(selected_history)
            elif len(move_options) != 0: #nk has neighbors
                depth_hit=True
            # end if goal_fcn/elif game end/elif nk has neighbors
        else: # for every neighbor nk+1 of nk add nk+1 to frontier
            if updated_board.check_game_end():
                #print('continued in else due to check game end == true')
                continue # skip the cases where Pengu dies
            
            # If no Pengu death, calculate the hash of the state and see if
            # it has been visited already.
            (should_extend,
             explored_hashes # this gets the extended table if unvisited state
             ) = hash_check_BDFS(updated_board,
                                 len(selected_history),
                                 explored_hashes
                                 )
            
            if should_extend == False:
                continue # skip the visited paths according to the hash table
            
            #print('extending moves')
            for move in move_options: # finally do the path extensions
                extended_history = selected_history+[move]
                frontier.append(extended_history)
            # end for move in move_options extending frontier w/ neighbors of n
        # end if length(p) == depth_limit
    # end while frontier not empty loop
    print('no goal satisfying path found. depth hit is '+str(depth_hit))
    print('number of loop iterations = '+str(numits))
    return(depth_hit)
# end def BoundedDFS_algorithm

def IDDFS_algorithm(game_in,goal_fcn):
    depth = 1
    res = True
    
    while True: # just loop ("REPEAT")
        
        time_before = time.time()
        
        res = BoundedDFS_algorithm(game_in,goal_fcn,depth)
        #print('res = '+str(res))
        #print(type(res))
        
        if isinstance(res,list): # if res is a path
            print('reached depth '+str(depth))
            return(res)
        else:
            depth = depth+1
            print('depth = '+str(depth))
        
        time_taken = time.time()-time_before
        print('IDDFS loop time was '+f'{time_taken:2f}')
        
        if res == False: # until not res
            break
        # end if res == false
    
    # end while true loop
    print('no goal satisfying path found.')
    return(False)
# end def IDDFS_algorithm
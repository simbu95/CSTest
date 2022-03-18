#%% imports
import random # for random.choice() to get a random move
import time # for optimization testing
import numpy as np

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

def move_parse(move_key):
    """Given a move, map it into row_fx and col_fx indices."""
    move_idx = possible_moves.index(move_key)
    return(move_idx)
    
def pick_random_move(valid_moves_list):
    """Given a list of num key moves, return a random one."""
    choice = random.choice(valid_moves_list)
    return(choice)

#%% Pengu class
class PenguGameBoard:
    """
    Holds all the information related to a state of the Pengu game. That is,
    there is a 2D list of lists that holds the game board, a tuple of the
    coordinates of Pengu's position on the board, and a score number holding
    Pengu's current accumulated score.
    
    Init takes board, position tuple
    
    Consider future expansion to improve checking visited states capability.
    """
    
    def __init__(self,hazards,fish,position_in,score_in,totalFish=None):
        self.hazards = hazards
        self.fish = fish #new numpy array to handle fishes
        self.position = position_in
        self.score = score_in
        if(totalFish != None):
            self.totalFish = totalFish
        else:
            self.totalFish=np.count_nonzero(fish)
    # end def __init__
    
    def __repr__(self):
        return(f'{self.hazards}\n'
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
        for i,row in enumerate(self.hazards):
            for j,char in enumerate(row):
                # need to handle case where Pengu is standing on a snow patch
                if i == p_row and j == p_col:
                    # must also handle the case where pengu is on a hazard = dead
                    if (self.hazards[p_row][p_col] == 'S' or 
                        self.hazards[p_row][p_col] == 'U'):
                        print('X',end='')
                    else:
                        print('P',end='')
                else:
                    if(self.fish[i,j]):
                        print('*',end='')
                    else:
                        print(char,end='')
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
            check_char = self.hazards[p_row+row_fx[move]][p_col+col_fx[move]]
            if check_char == '#':   # cannot move into a wall, do not add the move 
                pass                # to the valid moves list
            else:
                valid_moves.append(move_key) # otherwise add the move to the list
            # end character check
        # end for loop through possible moves by index
        return(valid_moves) # return the list of valid moves
    # end def list_valid_moves

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
        
        fish_copy = np.copy(self.fish)
        
        points_gained = 0 # will count any fish pengu's move picks up
        
        next_row = p_row+row_fx[move] # holds the first row of pengu's move
        next_col = p_col+col_fx[move] # first column of pengu's move
        
        # get the symbol in the first cell of pengu's move
        next_space_char = self.hazards[next_row][next_col] 
        
        # do the moving until a wall is reached
        while next_space_char != '#':
            
            # update pengu position before incrementing/continuing his move
            p_row = next_row
            p_col = next_col
            
            # handle the different board space encounters (snow, hazard, fish)
            # handle updating the board (remove '*' when a fish is collected)
            if fish_copy[p_row,p_col] != 0: # if a fish is picked up
                fish_copy[p_row,p_col] = 0 # remove fish
                points_gained = points_gained+1 # add a point for picking up fish
            # handle the hazards
            elif self.hazards[p_row][p_col] == 'S' or self.hazards[p_row][p_col] == 'U':
                #print('broke in make_move for S or U')
                break # pengu stops if he dies
            elif self.hazards[p_row][p_col] == '0':
                break # pengu stops if he hits a snow patch
            
            # next space indices
            next_row = p_row+row_fx[move]
            next_col = p_col+col_fx[move]
            
            # holds '#' when the next space is a wall
            next_space_char = self.hazards[next_row][next_col] # next cell symbol
        # end while loop
        
        pengu_position = (p_row,p_col) # update pengu's position
        
        game_out = PenguGameBoard(self.hazards,fish_copy,pengu_position,
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
        
        if self.hazards[p_row][p_col] == 'U' or self.hazards[p_row][p_col] == 'S':
            #print('Pengu is dead!')
            return(True)
        elif self.score >= self.totalFish:
            print('Pengu is a winner!')
            return(True)
        else:
            return(False)
        # end ifs handling whether the game ends or not
    # end def check_game_end

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


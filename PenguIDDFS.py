#%% imports
from collections import deque # for the deque object
import numpy as np # for hash storage
import time # for optimization testing

def hash_check_BDFS(game_in,path_length,hash_table_in):
    #This is technically bad, as a large enough state space would take up all computer memory, but better then before. 
    hashed_board = str(np.append(game_in.fish.flatten(),game_in.position)) 
    if hashed_board not in hash_table_in:
        # if the state has not been reached before, just append it
        hash_table_in[hashed_board]=path_length
    else: 
        if path_length < hash_table_in[hashed_board]:
            # Current path is shorter, replace the longer path hash in
            # hash_table_in with the current path to the same state
            hash_table_in[hashed_board] = path_length
        else:
            # Current path is longer, should not extend path to neighbors.
            return False
    return True
    

def BoundedDFS_algorithm(game_in,goal_fcn,depth_limit):
    numits = 0
    move_history = [0,] 
    
    depth_hit = False
    frontier = deque([move_history])
    
    # hash table
    explored_hashes = {}
    
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
            should_extend = hash_check_BDFS(updated_board,
                                 len(selected_history),
                                 explored_hashes
                                 )
            
            if should_extend == False:
                continue # skip the visited paths according to the hash table
            for move in move_options: # finally do the path extensions
                extended_history = selected_history+[move]
                frontier.append(extended_history)
                
    print('no goal satisfying path found. depth hit is '+str(depth_hit))
    print('number of loop iterations = '+str(numits))
    return(depth_hit)

def IDDFS_algorithm(game_in,goal_fcn):
    depth = 1
    res = True
    
    while True:
        
        time_before = time.time()
        
        res = BoundedDFS_algorithm(game_in,goal_fcn,depth)
        
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
            
    print('no goal satisfying path found.')
    return(False)
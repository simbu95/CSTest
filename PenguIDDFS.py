#%% imports
from collections import deque # for the deque object
import numpy as np # for hash storage
import time # for optimization testing

def hash_check_BDFS(game_in,path_length,hash_table_in):

    hashed_board = hash(str(np.append(game_in.fish.flatten(),game_in.position))) # hash of game state
    # hash table also needs the path length to compare and keep shorter paths
    # to visited states
    hash_table_entry = np.array([[hashed_board,path_length]]) #this is a poor way to do hashing... 
    
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
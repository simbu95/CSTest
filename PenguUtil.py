from PenguBoard import PenguGameBoard

def readPenguBoardFile(input_filename):
    data = open(input_filename, "r")  # open infile in read mode

    # the first line of the input file has the number of rows, 
    # space, number of columns

    #Honestly you should implement a read from file function in your game board class but details... 
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

    return PenguGameBoard(board_array,pengu_pos,0)
    
def endGamePrintouts(end,move_history,print_boards):
    if print_boards:
        end.pretty_print_board()
    # end if print_boards
    print('pengu pos = '+str(end.position))
    print('pengu pts = '+str(end.score))
    print('move history = '+str(move_history[1:])+
          ' length = '+str(len(move_history[1:])))
    print('fish remaining = '+str(end.count_fish())) #This could also be totalFish-score
    
def printToOutputFile(end,move_history,output_filename):
    # open output file to write the game to
    f = open(output_filename,'w')   # ,w means write over/clear existing file
    
    # write the move history at the top of the file
    for index,move_key in enumerate(move_history):
        if move_key != 0:
            f.write(str(move_key)) # write the move in num key format
        # end if checking "no move" move key at the beginning of the output
    # end for through move history
    
    # next line gets pengu's score
    f.write('\n'+str(end.score))
    
    # close and reopen the file in append mode
    # Why is this being done? I mean its fine... but...
    f.close()
    f = open(output_filename,'a') # ,a means append output to end of the file
    
    # abbreviate row and column for convenience
    p_row = end.position[0]
    p_col = end.position[1]
    
    # print the board to the file
    for i,row in enumerate(end.board):
        # start with a newline for each row. Keeps a blank line from being
        # written at the end of the file.
        f.write('\n')
        
        # go through the characters in the row of the board
        for j,char in enumerate(row):
            # handle case where Pengu is standing on a snow patch or hazard
            if i == p_row and j == p_col: # if printing where pengu is standing
                # handle the case where pengu is on a hazard = dead
                if (end.board[p_row][p_col] == 'S' # shark death
                        or end.board[p_row][p_col] == 'U'): # bear death
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
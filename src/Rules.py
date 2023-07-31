"""
This is a file that holds all the functions to check for patterns in the board that is created
"""

import Actions
#must have the board passed in, will act as a sort of main function to check the board for patterns
def runRules(board):
    maxRow = len(board)
    maxCol = len(board[0])
    actionTaken = False
    for row in range(maxRow):
        for column in range(maxCol):
            #if set to false, will not visit space again for efficiency purposes
            if(board[row][column].testAgain == False):
               continue
            if(checkAroundToMark(board, row, column, maxRow, maxCol) or checkAroundToClear(board, row, column, maxRow, maxCol)):
                actionTaken = True
    if not actionTaken:
        return 1
    else:
        return 0


#pass the board in, checks if there are as many flags as bombs around a spot
def checkAroundToClear(board, row, col, maxRow, maxCol):
    value = (board[row][col]).val
    
    if(value != '.' and value != 'X' and value != '-'):
        holder = getGreenAndFlag(board, row, col, maxRow, maxCol)#gets number of green spaces and flag spaces
        flagCount = holder[1]
        greenCount = holder[0]

        if(flagCount == int(value) and greenCount > 0):#if there is as many flags as there are bombs, click all around
            Actions.clickAllAround(board, row, col, maxRow, maxCol)
            print("Clear all around " + str(col ) +", " + str(row))
            board[row][col].testAgain = False#to ensure this space wont be tested again
            return True


#pass the board in, checks if there are as man green spaces as there are supposed to be bombs
def checkAroundToMark(board, row, col, maxRow, maxCol):
    value = (board[row][col]).val#number stores in the current cell
    
    if(value != '.' and value != 'X' and value != '-'):
        holder = getGreenAndFlag(board, row, col, maxRow, maxCol)#0 index is number of greens around the cell 1 index is number of flags
        flagCount = holder[1]
        greenCount = holder[0]
        
        if((greenCount + flagCount == int(value)) and int(value) - flagCount != 0):#checks if there are as man green spaces as there are supposed to be bombs, flag all around
            print("Add a flag to every spot around " + str(col ) +", " + str(row ))
            Actions.rightClickAllAround(board, row, col, maxRow, maxCol)
            return True




#returns and array [greencounter, flagCounter] of the maxRow sqaures surrounding the cell
def getGreenAndFlag(board, row, col, maxRow, maxCol):
    flagCounter = checkForChar('X', board, row, col, maxRow, maxCol)
    greenCounter = checkForChar('-', board, row, col, maxRow, maxCol)

    return [greenCounter, flagCounter]


#returns the number of occurences of passed in char in the 8 spaces surrounding the current location
def checkForChar(currChar, board, row, col, maxRow, maxCol):
    counter = 0

    #will loop through the 3x3 grid of cells around passed in cell
    for currRow in range(row - 1, row + 2):
        for currCol in range(col - 1, col + 2):

            if(currRow  < maxRow and currRow >= 0 and currCol < maxCol and currCol >= 0):#tests to make sure number is in correct range
                currentCell = board[currRow][currCol]

                if(currentCell.val == currChar):
                    counter += 1


    return counter
        
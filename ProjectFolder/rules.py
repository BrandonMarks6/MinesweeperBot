"""
This is a file that holds all the functions to check for patterns in the board that is created
"""

import actions
import os
#must have the board passed in, will act as a sort of main function to check the board for patterns
def runRules(board):
    maxRow = len(board)
    maxCol = len(board[0])
    actionTaken = False
    for row in range(len(board)):
        for column in range(len(board[row])):
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
    holder = getGreenAndFlag(board, row, col, maxRow, maxCol)
    value = (board[row][col]).val
    flagCount = holder[1]
    greenCount = holder[0]

    if(value != '.' and value != 'X' and value != '-'):
        if(flagCount == int(value) and greenCount > 0):
            actions.clickAllAround(board, row, col, maxRow, maxCol)
            print("Clear all around " + str(col ) +", " + str(row))
            board[row][col].testAgain = False
            return True


#pass the board in, 
def checkAroundToMark(board, row, col, maxRow, maxCol):

    holder = getGreenAndFlag(board, row, col, maxRow, maxCol)#0 index is number of greens around the cell 1 index is number of flags
    value = (board[row][col]).val#number stores in the current cell
    flagCount = holder[1]
    greenCount = holder[0]


    if(value != '.' and value != 'X' and value != '-'):
        #possibly be improved by - amount of flags but errorrs will need to be fixed(THIS WILL NEED TO BE IMPLEMENTED FOR THE PROGRAM TO WORK)
        if((greenCount + flagCount == int(value)) and int(value) - flagCount != 0):
            print("Add a flag to every spot around " + str(col ) +", " + str(row ))
            actions.rightClickAllAround(board, row, col, maxRow, maxCol)
            return True




#returns and array [greencounter, flagCounter] of the maxRow sqaures surrounding the cell
def getGreenAndFlag(board, row, col, maxRow, maxCol):
    
    flagCounter = 0
    #check down left
    if(row + 1 < maxRow and col - 1 >= 0 and board[row + 1][col - 1].val == 'X'):
        flagCounter += 1
    #check down    
    if(row + 1 < maxRow and board[row + 1][col].val == 'X'):
        flagCounter += 1
    #check down right
    if(row + 1 < maxRow and col + 1 < maxCol and board[row + 1][col + 1].val == 'X'):
        flagCounter += 1
    #check left
    if(col - 1 >= 0 and board[row][col - 1].val == 'X'):
        flagCounter += 1
    #check right
    if(col + 1 < maxCol and board[row][col + 1].val == 'X'):
        flagCounter += 1
    #check up left
    if(row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1].val == 'X'):
        flagCounter += 1
    #check up
    if(row - 1 >= 0 and board[row - 1][col].val == 'X'):
        flagCounter += 1
    #check up right
    if(row - 1 >= 0 and col + 1 < maxCol and board[row - 1][col + 1].val == 'X'):
        flagCounter += 1

    greenCounter = 0
    #check down left
    if(row + 1 < maxRow and col - 1 >= 0 and board[row + 1][col - 1].val == '-'):
        greenCounter += 1
    #check down    
    if(row + 1 < maxRow and board[row + 1][col].val == '-'):
        greenCounter += 1
    #check down right
    if(row + 1 < maxRow and col + 1 < maxCol and board[row + 1][col + 1].val == '-'):
        greenCounter += 1
    #check left
    if(col - 1 >= 0 and board[row][col - 1].val == '-'):
        greenCounter += 1
    #check right
    if(col + 1 < maxCol and board[row][col + 1].val == '-'):
        greenCounter += 1
    #check up left
    if(row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1].val == '-'):
        greenCounter += 1
    #check up
    if(row - 1 >= 0 and board[row - 1][col].val == '-'):
        greenCounter += 1
    #check up right
    if(row - 1 >= 0 and col + 1 < maxCol and board[row - 1][col + 1].val == '-'):
        greenCounter += 1


    return [greenCounter, flagCounter]
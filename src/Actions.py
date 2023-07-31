"""
this file will hold all of the action funtions to work on the board
"""
import pyautogui

#constants
PADDING_FACTOR = 20
PIXEL_DIVISION_FACTOR = 2 #Is used to convert coordinates from pyautoguin to correct location

def clickAllAround(board, row, col, maxRow, maxCol):
    #will loop through the 3x3 grid of cells around passed in cell
    for currRow in range(row - 1, row + 2):

        for currCol in range(col - 1, col + 2):
        
            if(currRow  < maxRow and currRow >= 0 and currCol < maxCol and currCol >= 0):#tests to make sure number is in correct range
                currrentSpace = board[currRow][currCol]

                if(not currrentSpace.clicked and currrentSpace.val == '-'):#if cell has not already been clickd and it is a correct value, click it and mark as clicked
                    pyautogui.click(currrentSpace.coord1/PIXEL_DIVISION_FACTOR + PADDING_FACTOR, currrentSpace.coord2/PIXEL_DIVISION_FACTOR + PADDING_FACTOR)
                    currrentSpace.clicked = True
    

def rightClickAllAround(board, row, col, maxRow, maxCol):
    #will loop through the 3x3 grid of cells around passed in cell
    for currRow in range(row - 1, row + 2):

        for currCol in range(col - 1, col + 2):
        
            if(currRow  < maxRow and currRow >= 0 and currCol < maxCol and currCol >= 0):#tests to make sure number is in correct range
                currrentSpace = board[currRow][currCol]
                
                if(not currrentSpace.clicked and currrentSpace.val == '-'):#if cell has not already been clickd and it is a correct value, click it and mark as clicked
                    pyautogui.rightClick(currrentSpace.coord1/PIXEL_DIVISION_FACTOR + PADDING_FACTOR, currrentSpace.coord2/PIXEL_DIVISION_FACTOR + PADDING_FACTOR)
                    board[currRow][currCol].val = 'X'
    
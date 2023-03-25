import rules

import keyboard
import pyautogui, cv2, time, os, sys
import numpy as np
from PIL import Image



"""
Color RGB Values
Blue(1) = (56, 116, 203)
Green(2) = (80, 140, 70)
Red(3) = (193, 63, 56)
Purple(4) = (113, 38, 156)
Yellow(5) = (240, 148, 54)

Use the win32api to click because it is faster than pyaautogui
-pause for .01 second to make sure it executes

pyautogui.locate takes an negligible amount of time 
pyautogui.screenshot is around .25 seconds
"""


"""
Class will be used to hold data for one cell on the board along with coordinated in order to know where the cell is located on the board
val = what is at the location on the screen 
coord1 = top
coord2 = left


Val key:
1 : 1
2 : 2
3 : 3
4 : 4
5 : 5
X : Flag
. : empty square
- : green(unclicked square)
"""



class cell:
    def __init__(self, val, coord1, coord2):
        self.val = val
        self.coord1 = coord1
        self.coord2 = coord2
        self.testAgain = True 



#numbers to divide by based on the size of the board
#8
#14
scalingNumberRow = 14
#10
#18
scalingNumberCol = 18


extraPixelsForInitialBoard = 10
extraPixelsForCellScan = 20

currBoard = []
#makes a 2d array filled with zeroes to store cell objects in
for x in range(scalingNumberRow):
    column_elements = []
    for y in range(scalingNumberCol):
        column_elements.append('0')
    currBoard.append(column_elements)








"""
will quit the program when the q button is pressed
this check is spread throughout the program so it should execute close to always
"""
def checkQuitPause():
    if keyboard.is_pressed('q'): 
        os.system( "say The program is done" )
        sys.exit("Quit")

def checkWin():
    if pyautogui.locateOnScreen('PictureHolder/WinImage.png'):
        os.system( "say The program is done" )
        sys.exit("Quit")




"""
takes in boxCoords
returns nothing

gets a copy of the board with scanBoard
then runs looper to check rules in each location on the board
asks user if they would like to run ahain or quit
calls runAgain on this inpout to see the input and will run or stop accordingly
"""
def runScanner(boxCoords):    
    while True:
        checkQuitPause()
        scanBoard(boxCoords)
        #runRules will check each rule and act accordingly on the board
        rules.runRules(currBoard)
        checkWin()
        os.system( "say Current Board is scanned" )



"""
takes in nothing
returns a set of boxcoords

locates the board with pyautogui.locateOnScreen()
returns that value
"""
def findBoard():
    #waits two seconds after called to search for the game board
    time.sleep(2)

    boardLocEasy = (pyautogui.locateOnScreen('PictureHolder/EasyMap.png', confidence = .9))
    if boardLocEasy:
        main.scalingNumberRow = 8
        main.scalingNumberCol = 10
        os.system( "say Easy Board Loacated" )
        return boardLocEasy

    boardLocMedium = (pyautogui.locateOnScreen('PictureHolder/MedMap.png', confidence = .9))
    if boardLocMedium:
        os.system( "say Medium Board Loacated" )
        scalingNumberRow = 14
        scalingNumberCol = 18
        return boardLocMedium
    
    print("Board not found")
    os.system( "say Board could not be found" )
    sys.exit("Quit")




"""
takes in boxCoords
returns a 2d  array representing the board

makes an empty 2d array according to size of board
scans each box in the array and fills in the according location on the array with the info
stores info in each location with a cell object

def __init__(self, val, coord1, coord2):
        self.val = val
        self.coord1 = coord1
        self.coord2 = coord2

prints board
then returns

"""
def scanBoard(boxCoords):
    start = time.time()

    print("Board Scan Started")


    for row in range(scalingNumberRow):
        for column in range(scalingNumberCol):
            #skips the piece if it is already known that it will not change
            if(currBoard[row][column] != '0' and currBoard[row][column].val != '-'):
                continue
            checkQuitPause()
            
            #takes a picture with extra wide of the coordinates input so an image of a number can be found inside the  picture
            im1 = pyautogui.screenshot(region=((boxCoords.left) - extraPixelsForInitialBoard + (column * boxCoords.width/scalingNumberCol), (boxCoords.top) - extraPixelsForInitialBoard + (row * boxCoords.height/scalingNumberRow), (boxCoords.width/scalingNumberCol) + extraPixelsForCellScan, (boxCoords.height/scalingNumberRow) + extraPixelsForCellScan))
            im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
            cv2.imwrite("CheckThis.png", im1)

            check = Image.open('CheckThis.png')
            pix = check.load()


            whatIsVal = '.'
            #checks each box for a number or flag according to the pictures in the "numbers" folder
            if pyautogui.locate('numbers/One.png', 'CheckThis.png', confidence = .8, grayscale= True) or pyautogui.locate('numbers/MedOne.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = '1'
            elif pyautogui.locate('numbers/Two.png', 'CheckThis.png', confidence = .8, grayscale= True) or pyautogui.locate('numbers/MedTwo.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = '2'
            elif pyautogui.locate('numbers/Three.png', 'CheckThis.png', confidence = .8, grayscale= True) or pyautogui.locate('numbers/MedThree.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = '3'
            elif pyautogui.locate('numbers/Four.png', 'CheckThis.png', confidence = .8, grayscale= True) or pyautogui.locate('numbers/MedFour.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = '4'
            elif pyautogui.locate('numbers/Five.png', 'CheckThis.png', confidence = .8, grayscale= True) or pyautogui.locate('numbers/MedFive.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = '5'
            elif pyautogui.locate('numbers/Six.png', 'CheckThis.png', confidence = .8, grayscale= True) or pyautogui.locate('numbers/MedSix.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = '6'
            elif pyautogui.locate('numbers/Flag.png', 'CheckThis.png', confidence = .8, grayscale= True):
                whatIsVal = 'X'

            if whatIsVal == '.':
                #checks against the RGB values of the color of a light green or dark green square
                if(pix[20,20] == (179, 214, 101)) or (pix[20,20] == (172, 208, 94)):
                    whatIsVal = '-'

            
            if(currBoard[row][column] == '0'):
                #makes a cell object for each space in the output array
                currBoard[row][column] = cell(whatIsVal, ((boxCoords.left) - extraPixelsForInitialBoard + (column * boxCoords.width/scalingNumberCol)), (boxCoords.top) - extraPixelsForInitialBoard + (row * boxCoords.height/scalingNumberRow))
            else:
                currBoard[row][column].val = whatIsVal


    #prints the gameboard
    for row in range(len(currBoard)):
        for column in range(len(currBoard[row])):
            print(currBoard[row][column].val, end = " ") #print each element
        print()


    end = time.time()
    print("Board Scan complete in", int(end - start), "seconds")






"""
Main function
starts a "timer" when program is started
find the board and stores it coordinates
runs the scanner on the board to populate array
ends the timer and oprints the timer 
then computer will say the program is done"""
def main():
    print("Please have a blank version of google minesweeper on your screen so the board can be located")

    """
    testing portion

    class Box:
        def __init__(self, left, top, width, height):
            self.left = left
            self.top = top
            self.width = width
            self.height = height

    #hard coded coordinates of the box for testing
    my_box = Box(left=990, top=707, width=897, height=721)
    runScanner(my_box)
    """

    location = findBoard()
    runScanner(location)




#calls the main function
if __name__ == "__main__":
    main()
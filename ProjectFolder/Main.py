#######################################
# Name: Brandon Marks                 #
# Purpose: to play google minesweeper #
#######################################
import rules

import pyautogui, cv2, time, os, sys
import numpy as np
from PIL import Image

"""
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

#constants to be used within the program
EASY_LENGTH = 10
EASY_HEIGHT = 8
MEDIUM_LENGTH = 18
MEDIUM_HEIGHT = 14
HARD_LENGTH = 24
HARD_HEIGHT = 20


#class will represent each cell on the board
class cell:
    def __init__(self, val, coord1, coord2):
        self.val = val
        self.coord1 = coord1
        self.coord2 = coord2
        self.testAgain = True 
        self.clicked = False


"""
will check for win or lose images on screen and terminate program if seen
"""
def checkWinOrLose():
    if pyautogui.locateOnScreen('PictureHolder/WinImage.png'):
        os.system( "say Game Won. The program is done" )
        sys.exit("Quit")

    if pyautogui.locateOnScreen('PictureHolder/LoseImage.png'):
        os.system( "say Game Lost. The program is done" )
        sys.exit("Quit")



"""
runs the main functionality of the code
"""
def runScanner(boxCoords, rowNum, colNum):    

    currBoard = []
    #makes a 2d array filled with zeroes to store cell objects in
    for x in range(rowNum):
        column_elements = []
        for y in range(colNum):
            column_elements.append('0')
        currBoard.append(column_elements)

    counter = 0
    
    #will run until program is terminated
    while True:        
        #populates the current board by scanning screen for images
        scanBoard(currBoard, boxCoords, rowNum, colNum)

        #prints current board
        for row in range(len(currBoard)):
            for column in range(len(currBoard[row])):
                print(currBoard[row][column].val, end = " ") 
            print()

        #runRules will check each rule and act accordingly on the board
        #if no actions taken after 3 loops, user is asked to click a green piece
        counter += rules.runRules(currBoard)
        if counter >= 3:
            print("Please Click a green piece on the board")
            os.system( "say Please Click a green piece on the board" )
            counter = 0

        checkWinOrLose()
        os.system( "say Current Board is scanned" )



"""
locates the board with pyautogui.locateOnScreen()
returns the location of the board along with the grid length and height
"""
def findBoard():
    #waits two seconds after called to search for the game board so user has time to switch screens if neccessary
    time.sleep(4)

    boardLocEasy = (pyautogui.locateOnScreen('PictureHolder/EasyMap.png', confidence = .8))
    if boardLocEasy:
        print("Easy Board Loacated")
        os.system( "say Easy Board Loacated" )
        return boardLocEasy, EASY_HEIGHT, EASY_LENGTH

    boardLocMedium = (pyautogui.locateOnScreen('PictureHolder/MedMap.png', confidence = .9))
    if boardLocMedium:
        print("Medium Board Loacated")
        os.system( "say Medium Board Loacated" )
        return boardLocMedium, MEDIUM_HEIGHT, MEDIUM_LENGTH
    
    boardLocHard = (pyautogui.locateOnScreen('PictureHolder/HardMap.png', confidence = .9))
    if boardLocHard:
        print("Hard Board Loacated")
        os.system( "say Hard Board Loacated" )
        return boardLocHard, HARD_HEIGHT, HARD_LENGTH
    
    print("Board not found")
    os.system( "say Board could not be found" )
    sys.exit("Quit")



"""
Scans and populates the board
"""
def scanBoard(currBoard, boxCoords, rowParam, colParam):
    start = time.time()
    print("Board Scan Started")
    #fills board with cells containing brown spaces
    for row in range(rowParam):
        for column in range(colParam):
            currBoard[row][column] = cell('.', ((boxCoords.left) + (column * boxCoords.width/colParam)), (boxCoords.top) + (row * boxCoords.height/rowParam))


    #determines which list based on size of board
    if rowParam == EASY_HEIGHT:
        pictureList = {'numbers/One.png' : '1', 'numbers/Two.png': '2', 'numbers/Three.png': '3', 'numbers/Four.png': '4', 'numbers/Five.png': '5', 'numbers/Six.png': '6', 'numbers/Flag.png': 'X'}
    if rowParam == MEDIUM_HEIGHT:
        pictureList = {'numbers/MedOne.png' : '1', 'numbers/MedTwo.png': '2', 'numbers/MedThree.png': '3', 'numbers/MedFour.png': '4', 'numbers/MedFive.png': '5', 'numbers/MedSix.png': '6', 'numbers/MedSeven.png': '7',  'numbers/MedFlag.png': 'X'}
    if rowParam == HARD_HEIGHT:
        pictureList = {'numbers/HardOne.png' : '1', 'numbers/HardTwo.png': '2', 'numbers/HardThree.png': '3', 'numbers/HardFour.png': '4', 'numbers/HardFive.png': '5', 'numbers/MedSix.png': '6',  'numbers/HardFlag.png': 'X'}

    #will check for each picture on the screen
    for currentPicture in pictureList.keys():

        #makes a tuple of all the locations of the current picture
        #loops through each location in the tuple
        allFoundLocations = pyautogui.locateAllOnScreen(currentPicture, grayscale=True, confidence=0.85)
        for currentCoords in allFoundLocations:
            rowToInsert = 0

            #while loop will loop through current rows in board until the correct location is found of the current location of the picture
            while rowToInsert + 1 < rowParam:
                bottomRangeRows = currBoard[rowToInsert][0].coord2
                topRangeRows = currBoard[rowToInsert + 1][0].coord2
                if currentCoords.top > bottomRangeRows and currentCoords.top < topRangeRows:
                    break
                rowToInsert += 1


            #while loop will loop through current columns in board until the correct location is found of the current location of the picture
            colToInsert = 0
            while colToInsert + 1 < colParam:
                bottomRangeCols = currBoard[0][colToInsert].coord1
                topRangeCols = currBoard[0][colToInsert + 1].coord1
                if currentCoords.left > bottomRangeCols and currentCoords.left < topRangeCols:
                    break
                colToInsert += 1

            #inserts in correct spot based on the coordinates of the found item
            currBoard[rowToInsert][colToInsert].val = pictureList.get(currentPicture)



    #below will add all correct green spaces to the board

    #takes a picture with extra wide of the board to make sure to capture entire thing
    im1 = pyautogui.screenshot(region=(boxCoords))
    im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
    #writes the image to "CheckThis.png" 
    cv2.imwrite("CheckThis.png", im1)

    check = Image.open('CheckThis.png')
    pix = check.load()

    picHeight = check.height
    picLength = check.size[0]

    paddingNum = 10

    for row in range(rowParam):
        for column in range(colParam):
            #checks against the RGB values of the color of a light green or dark green square
            lightGreenValues = (179, 214, 101)
            darkGreenValues = (172, 208, 94)
            if(pix[(column * (picLength /colParam)) + paddingNum, (row * (picHeight /rowParam)) + paddingNum] == lightGreenValues) or (pix[(column * (picLength /colParam) + paddingNum), (row * (picHeight /rowParam) + paddingNum)] == darkGreenValues):
                if(currBoard[row][column].val != 'X'):#only assigns a green tile if there is not a flag currently on the tile
                    currBoard[row][column].val = '-'


    end = time.time()
    print("Board Scan complete in", int(end - start), "seconds")




###########################################################################################################
#Main Function will find the board then enter the board into the scanner with the row and column numbers
def main():
    print("Please have a blank version of google minesweeper on your screen so the board can be located")

    location, rowNum, colNum = findBoard()
    runScanner(location, rowNum, colNum)

#calls the main function
if __name__ == "__main__":
    main()
###########################################################################################################

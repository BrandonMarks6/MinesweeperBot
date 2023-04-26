#######################################
# Name: Brandon Marks                 #
# Purpose: to play google minesweeper #
#######################################
import rules

import keyboard
import pyautogui, cv2, time, os, sys
import numpy as np
from PIL import Image



"""
Notes:

Use the win32api to click because it is faster than pyaautogui
-pause for .01 second to make sure it executes

pyautogui.screenshot is around .25 seconds
Pyautogui locate all is much faster.(Returns a generator of locations)
"""

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

class cell:
    #will represent each cell on the board
    def __init__(self, val, coord1, coord2):
        self.val = val
        self.coord1 = coord1
        self.coord2 = coord2
        self.testAgain = True 
        self.clicked = False


"""
will quit the program when the q button is pressed
this check is spread throughout the program so it should execute close to always
"""
def checkQuitPause():
    return
    if keyboard.is_pressed('q'): 
        os.system( "say The program is done" )
        sys.exit("Quit")


#keyboard.add_hotkey("q", lambda: sys.exit("Quit"))


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
    
    #will run intil program is terminated
    while True:
        checkQuitPause()
        
        #populates the current board
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

    boardLocEasy = (pyautogui.locateOnScreen('PictureHolder/EasyMap.png', confidence = .9))
    if boardLocEasy:
        print("Easy Board Loacated")
        os.system( "say Easy Board Loacated" )
        return boardLocEasy, 8, 10

    boardLocMedium = (pyautogui.locateOnScreen('PictureHolder/MedMap.png', confidence = .9))
    if boardLocMedium:
        print("Medium Board Loacated")
        os.system( "say Medium Board Loacated" )
        return boardLocMedium, 14, 18
    
    boardLocHard = (pyautogui.locateOnScreen('PictureHolder/HardMap.png', confidence = .9))
    if boardLocHard:
        print("Hard Board Loacated")
        os.system( "say Hard Board Loacated" )
        return boardLocHard, 20, 24
    
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
    if rowParam == 8:
        pictureList = {'numbers/One.png' : '1', 'numbers/Two.png': '2', 'numbers/Three.png': '3', 'numbers/Four.png': '4', 'numbers/Five.png': '5', 'numbers/Six.png': '6', 'numbers/Flag.png': 'X'}
    if rowParam == 14:
        pictureList = {'numbers/MedOne.png' : '1', 'numbers/MedTwo.png': '2', 'numbers/MedThree.png': '3', 'numbers/MedFour.png': '4', 'numbers/MedFive.png': '5', 'numbers/MedSix.png': '6', 'numbers/MedSeven.png': '7',  'numbers/MedFlag.png': 'X'}
    if rowParam == 20:
        pictureList = {'numbers/HardOne.png' : '1', 'numbers/HardTwo.png': '2', 'numbers/HardThree.png': '3', 'numbers/HardFour.png': '4', 'numbers/HardFive.png': '5', 'numbers/MedSix.png': '6',  'numbers/HardFlag.png': 'X'}

    #will check for each picture on the screen
    for currentPicture in pictureList.keys():
        #makes a tuple of all the locations of the ucrrent picture
        #loops through each location in the tuple
        for currentCoords in pyautogui.locateAllOnScreen(currentPicture, grayscale=True, confidence=0.85):
            rowToInsert = 0
            while rowToInsert + 1 < rowParam:
                if currentCoords.top > currBoard[rowToInsert][0].coord2 and currentCoords.top < currBoard[rowToInsert + 1][0].coord2:
                    break
                rowToInsert += 1

            colToInsert = 0
            while colToInsert + 1 < colParam:
                if currentCoords.left > currBoard[0][colToInsert].coord1 and currentCoords.left < currBoard[0][colToInsert + 1].coord1:
                    break
                colToInsert += 1

            #inserts in ocrrect spot based on the coordinates of the found item
            currBoard[rowToInsert][colToInsert].val = pictureList.get(currentPicture)



    #below will add all correct green spaces to the board

    #takes a picture with extra wide of the coordinates input so an image of a number can be found inside the  picture
    im1 = pyautogui.screenshot(region=(boxCoords))
    im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
    cv2.imwrite("CheckThis.png", im1)

    check = Image.open('CheckThis.png')
    pix = check.load()

    picHeight = check.height
    picLength = check.size[0]

    for row in range(rowParam):
        for column in range(colParam):
            #checks against the RGB values of the color of a light green or dark green square
            if(pix[(column * (picLength /colParam)) + 10, (row * (picHeight /rowParam)) + 10] == (179, 214, 101)) or (pix[(column * (picLength /colParam) + 10), (row * (picHeight /rowParam) + 10)] == (172, 208, 94)):
                if(currBoard[row][column].val != 'X'):
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

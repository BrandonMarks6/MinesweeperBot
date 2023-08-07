import time
import sys

import pyautogui
import cv2

import numpy as np
from PIL import Image

from minesweeper_rules import MinesweeperRules
from board_values import BoardValues
from actions import Actions


class BoardFunctions:
    # constants to be used within the program
    EASY_LENGTH = 10
    EASY_HEIGHT = 8
    MEDIUM_LENGTH = 18
    MEDIUM_HEIGHT = 14
    HARD_LENGTH = 24
    HARD_HEIGHT = 20

    # class will represent each cell on the board
    class cell:
        def __init__(self, val, coord1, coord2):
            self.val = val
            self.coord1 = coord1
            self.coord2 = coord2
            self.test_again = True
            self.clicked = False

    def __init__(self):
        #allows program to click faster and makes sure program can be easily killed
        pyautogui.PAUSE = .001

        self.BoardValuesObj = BoardValues()
        self.ActionObj = Actions(self.BoardValuesObj)
        self.MinesweeperRulesObj = MinesweeperRules(self.ActionObj)
        
        

    
    


    """
    will check for win or lose images on screen and terminate program if seen
    """


    def check_win_or_lose(self):
        if pyautogui.locateOnScreen("PictureHolder/WinImage.png"):
            print("Game won. Exiting Program")
            sys.exit("Quit")

        if pyautogui.locateOnScreen("PictureHolder/LoseImage.png"):
            print("Game lost. Exiting program")
            sys.exit("Quit")


    """
    runs the main functionality of the code
    """


    def run_scanner(self, box_coords, row_num, col_num):
        curr_board = []
        # makes a 2d array filled with zeroes to store cell objects in
        for _ in range(row_num):
            column_elements = []
            for _ in range(col_num):
                column_elements.append("0")
            curr_board.append(column_elements)

        
        actionNoTakenCount = 0

        #deeper scn is only done if common numbers are found in default scan
        doDeepScan = False 

        # will run until program is terminated
        while True:
            # populates the passed in board by scanning screen for images
            self.scan_board(curr_board, box_coords, row_num, col_num, doDeepScan)
            doDeepScan = False

            # prints current board to terminal
            for row in range(len(curr_board)):
                for column in range(len(curr_board[row])):
                    print(curr_board[row][column].val, end=" ")
                print()

            # runRules will check each rule and act accordingly on the board
            # if no actions taken after 3 loops, user is asked to click a green piece
            actionNoTakenCount += self.MinesweeperRulesObj.run_rules(curr_board)
            if actionNoTakenCount >= 1:
                doDeepScan = True

            if actionNoTakenCount >= 3:
                print("Please Click a green piece on the board")
                actionNoTakenCount = 0

            self.check_win_or_lose()


    """
    locates the board with pyautogui.locateOnScreen()
    returns the location of the board along with the grid length and height
    """


    def find_board(self):
        # waits two seconds after called to search for the game board
        time.sleep(4)

        #will attempt to find 10 times
        for _ in range(10):
            board_loc_easy = pyautogui.locateOnScreen(
                "PictureHolder/EasyMap.png", confidence=0.85)
            if board_loc_easy:
                print("Easy Board Loacated")
                self.double_click_middle(board_loc_easy)
                return board_loc_easy, self.EASY_HEIGHT, self.EASY_LENGTH

            board_loc_medium = pyautogui.locateOnScreen(
                "PictureHolder/MedMap.png", confidence=0.9
            )
            if board_loc_medium:
                print("Medium Board Loacated")
                self.double_click_middle(board_loc_medium)
                return board_loc_medium, self.MEDIUM_HEIGHT, self.MEDIUM_LENGTH

            board_loc_hard = pyautogui.locateOnScreen(
                "PictureHolder/HardMap.png", confidence=0.9)
            if board_loc_hard:
                print("Hard Board Loacated")
                self.double_click_middle(board_loc_hard)
                return board_loc_hard, self.HARD_HEIGHT, self.HARD_LENGTH
            
            print("Board not found")
            time.sleep(4)

        print("Board not found after 10 attempts")
        sys.exit("Quit")


    def double_click_middle(self, coords):
        length_middle = coords.left / 2 + (coords.width / 4)
        height_middle = coords.top / 2 + (coords.height / 4)
        pyautogui.click(length_middle, height_middle)
        pyautogui.click(length_middle, height_middle)
        time.sleep(.5)

    def populate_board(self, picture_list, curr_board, box_coords, row_param, col_param):
            # will check for each picture on the screen
            for current_picture in picture_list.keys():
                # makes a tuple of all the locations of the current picture
                # loops through each location in the tuple
                all_found_locations = pyautogui.locateAllOnScreen(
                    current_picture, grayscale=True, confidence=0.85
                )
                for current_coords in all_found_locations:
                    row_to_insert = 0

                    # loop through current rows in board until the location is found
                    while row_to_insert + 1 < row_param:
                        bottom_range_rows = curr_board[row_to_insert][0].coord2
                        top_range_rows = curr_board[row_to_insert + 1][0].coord2
                        if (
                            current_coords.top > bottom_range_rows
                            and current_coords.top < top_range_rows
                        ):
                            break
                        row_to_insert += 1

                    # loop through current rows in board until the location is found
                    col_to_insert = 0
                    while col_to_insert + 1 < col_param:
                        bottom_range_cols = curr_board[0][col_to_insert].coord1
                        top_range_cols = curr_board[0][col_to_insert + 1].coord1
                        if (
                            current_coords.left > bottom_range_cols
                            and current_coords.left < top_range_cols
                        ):
                            break
                        col_to_insert += 1

                    # inserts in correct spot based on the coordinates of the found item
                    curr_board[row_to_insert][col_to_insert].val = picture_list.get(
                        current_picture)

            # below will add all correct green spaces to the board

            # takes a picture with extra wide of the board to make sure to capture entire thing
            im1 = pyautogui.screenshot(region=(box_coords))
            im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
            # writes the image to "CheckThis.png"
            cv2.imwrite("CheckThis.png", im1)

            check = Image.open("CheckThis.png")
            pix = check.load()

            pic_height = check.height
            pic_length = check.size[0]

            padding_num = 10

            for row in range(row_param):
                for column in range(col_param):
                    # checks against the RGB values of the color of a light green or dark green square
                    light_green_values = (179, 214, 101)
                    dark_green_values = (172, 208, 94)
                    if (
                        pix[
                            (column * (pic_length / col_param)) + padding_num,
                            (row * (pic_height / row_param)) + padding_num,
                        ]
                        == light_green_values
                    ) or (
                        pix[
                            (column * (pic_length / col_param) + padding_num),
                            (row * (pic_height / row_param) + padding_num),
                        ]
                        == dark_green_values
                    ):
                        if ( 
                            curr_board[row][column].val != self.BoardValuesObj.flag
                        ):  # only assigns a green tile if there is not a flag currently on the tile
                            curr_board[row][column].val = self.BoardValuesObj.unclicked_square

    """
    Scans and populates the board
    """
    def scan_board(self, curr_board, box_coords, row_param, col_param, doDeepScan):
        start = time.time()
        print()
        print()
        print("Board Scan Started")
        # fills board with cells containing brown spaces
        for row in range(row_param):
            for column in range(col_param):
                curr_board[row][column] = self.cell(
                    ".",
                    ((box_coords.left) + (column * box_coords.width / col_param)),
                    (box_coords.top) + (row * box_coords.height / row_param),
                )

        # determines which list based on size of board
        if row_param == self.EASY_HEIGHT and doDeepScan:
            picture_list = {
                "numbers/One.png": "1",
                "numbers/Two.png": "2",
                "numbers/Three.png": "3",
                "numbers/Four.png": "4",
                "numbers/Five.png": "5",
                "numbers/Six.png": "6",
                "numbers/Flag.png": "X",
            }

        if row_param == self.EASY_HEIGHT and not doDeepScan:
            picture_list = {
                "numbers/One.png": "1",
                "numbers/Two.png": "2",
                "numbers/Three.png": "3",
                "numbers/Flag.png": "X",
            }

        if row_param == self.MEDIUM_HEIGHT and doDeepScan:
            picture_list = {
                "numbers/MedOne.png": "1",
                "numbers/MedTwo.png": "2",
                "numbers/MedThree.png": "3",
                "numbers/MedFour.png": "4",
                "numbers/MedFive.png": "5",
                "numbers/MedSix.png": "6",
                "numbers/MedSeven.png": "7",
                "numbers/MedFlag.png": "X",
            }

        if row_param == self.MEDIUM_HEIGHT and not doDeepScan:
            picture_list = {
                "numbers/MedOne.png": "1",
                "numbers/MedTwo.png": "2",
                "numbers/MedThree.png": "3",
                "numbers/MedFlag.png": "X",
            }

        if row_param == self.HARD_HEIGHT and doDeepScan:
            picture_list = {
                "numbers/HardOne.png": "1",
                "numbers/HardTwo.png": "2",
                "numbers/HardThree.png": "3",
                "numbers/HardFour.png": "4",
                "numbers/HardFive.png": "5",
                "numbers/MedSix.png": "6",
                "numbers/HardFlag.png": "X",
            }

        if row_param == self.HARD_HEIGHT and not doDeepScan:
            picture_list = {
                "numbers/HardOne.png": "1",
                "numbers/HardTwo.png": "2",
                "numbers/HardThree.png": "3",
                "numbers/HardFlag.png": "X",
            }

        self.populate_board(picture_list, curr_board, box_coords, row_param, col_param)

        end = time.time()
        print("Board Scan complete in", int(end - start), "seconds")


        
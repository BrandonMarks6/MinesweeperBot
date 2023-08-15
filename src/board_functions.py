import time
import sys

import pyautogui
import cv2
import threading
from pynput import keyboard

import numpy as np
from PIL import Image

from minesweeper_rules import MinesweeperRules
from board_values import BoardValues
from actions import Actions
from display_data import DisplayData


class BoardFunctions:
    # constants to be used within the program
    EASY_LENGTH: int = 10
    EASY_HEIGHT: int = 8
    MEDIUM_LENGTH: int = 18
    MEDIUM_HEIGHT: int = 14
    HARD_LENGTH: int = 24
    HARD_HEIGHT: int = 20

    # class will represent each cell on the board
    class cell:
        def __init__(self, character: str, x_position: int, y_position: int) -> None:
            self.character: str = character
            self.x_position: int = x_position
            self.y_position: int = y_position
            self.test_again: bool = True
            self.clicked: bool = False

    def __init__(self) -> None:
        # allows program to click faster and makes sure program can be easily killed
        pyautogui.PAUSE = 0.001

        self.exit_event = threading.Event()

        self.BoardValuesObj = BoardValues()
        self.DisplayDataObj = DisplayData()
        self.ActionObj = Actions(self.BoardValuesObj)
        self.MinesweeperRulesObj = MinesweeperRules(
            self.ActionObj, self.BoardValuesObj, self.DisplayDataObj
        )

    def start_listener(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def on_key_press(self, key):
        try:
            # Convert the key to a string
            key_str = key.char
            if key_str == "q":
                exit_quit_message: str = "\nExit Key pressed. Exiting program ASAP\n"
                self.DisplayDataObj.display(exit_quit_message)
                self.exit_event.set()  # Signal the program to exit
                return False
        except AttributeError:
            pass  # Ignore special keys (non-character keys)

    def run_program(self):
        # Start the keyboard listener in a separate thread
        keyboard_thread = threading.Thread(target=self.start_listener)
        keyboard_thread.daemon = True  # Set the thread as daemon
        keyboard_thread.start()

        location, row_num, col_num = self.find_board()
        if location is not None:
            self.run_scanner(location, row_num, col_num)

        self.DisplayDataObj.display("\nProgram Complete\n")

    """
    will check for win or lose images on screen and terminate program if seen
    """

    def check_game_over(self) -> bool:
        if pyautogui.locateOnScreen("PictureHolder/WinImage.png"):
            exit_win_message: str = "Game won. Exiting Program"
            self.DisplayDataObj.display(exit_win_message)
            return True

        if pyautogui.locateOnScreen("PictureHolder/LoseImage.png"):
            exit_lose_message: str = "Game lost. Exiting program"
            self.DisplayDataObj.display(exit_lose_message)
            return True

        return False

    """
    runs the main functionality of the code
    """

    def run_scanner(self, box_coords: tuple, row_num: int, col_num: int) -> bool:
        curr_board: list = []
        # makes a 2d array filled with zeroes to store cell objects in
        for _ in range(row_num):
            column_elements: list = []
            for _ in range(col_num):
                place_holder: str = "0"
                column_elements.append(place_holder)
            curr_board.append(column_elements)

        action_not_taken_count: int = 0

        # deeper scn is only done if common numbers are found in default scan
        do_deep_scan: bool = False

        running: bool = True
        # will run until program is terminated
        while running:
            # populates the passed in board by scanning screen for images
            self.scan_board(curr_board, box_coords, row_num, col_num, do_deep_scan)
            do_deep_scan = False

            if self.exit_event.is_set():
                running = False
                break

            # self.DisplayDataObj.displays current board to terminal
            for row in range(len(curr_board)):
                current_row = []
                for column in range(len(curr_board[row])):
                    current_cell = curr_board[row][column]
                    current_row.append(current_cell.character)
                    current_row.append(" ")
                self.DisplayDataObj.display("".join(current_row))

            # runRules will check each rule and act accordingly on the board
            # if no actions taken after 3 loops, user is asked to click a green piece
            if self.MinesweeperRulesObj.check_minesweeper_rules(curr_board) <= 0:
                action_not_taken_count += 1

            if action_not_taken_count >= 1:
                do_deep_scan = True

            min_missing_actions = 3
            if action_not_taken_count >= min_missing_actions:
                actions_not_taken_message: str = (
                    "Please Click a green piece on the board"
                )
                self.DisplayDataObj.display(actions_not_taken_message)
                action_not_taken_count = 0

            game_ended: bool = self.check_game_over()
            running = not game_ended

            if self.exit_event.is_set():
                running = False
        return False

    """
    locates the board with pyautogui.locateOnScreen()
    returns the location of the board along with the grid length and height
    """

    def find_board(self) -> tuple:
        # waits two seconds after called to search for the game board
        seconds_to_sleep = 4
        time.sleep(seconds_to_sleep)

        # will attempt to find 10 times
        interation_number: int = 10
        for location_attempt_num in range(interation_number):
            if self.exit_event.is_set():
                return None, None, None
            board_loc_easy: bool = pyautogui.locateOnScreen(
                "PictureHolder/EasyMap.png", confidence=0.85
            )
            if board_loc_easy:
                self.DisplayDataObj.display("Easy Board Loacated")
                self.double_click_middle(board_loc_easy)
                return board_loc_easy, self.EASY_HEIGHT, self.EASY_LENGTH

            board_loc_medium: bool = pyautogui.locateOnScreen(
                "PictureHolder/MedMap.png", confidence=0.9
            )
            if board_loc_medium:
                self.DisplayDataObj.display("Medium Board Loacated")
                self.double_click_middle(board_loc_medium)
                return board_loc_medium, self.MEDIUM_HEIGHT, self.MEDIUM_LENGTH

            board_loc_hard: bool = pyautogui.locateOnScreen(
                "PictureHolder/HardMap.png", confidence=0.9
            )
            if board_loc_hard:
                self.DisplayDataObj.display("Hard Board Loacated")
                self.double_click_middle(board_loc_hard)
                return board_loc_hard, self.HARD_HEIGHT, self.HARD_LENGTH

            if location_attempt_num == 10:
                self.DisplayDataObj.display(
                    "Board not found after 10 attempts. Exiting"
                )
                break
            else:
                self.DisplayDataObj.display("Board not found")
            time.sleep(seconds_to_sleep)
        return None, None, None

    def double_click_middle(self, coords: tuple) -> None:
        pixel_resolution_number: int = 2
        length_middle: int = coords.left / pixel_resolution_number + (
            coords.width / (2 * pixel_resolution_number)
        )
        height_middle: int = coords.top / pixel_resolution_number + (
            coords.height / (2 * pixel_resolution_number)
        )
        pyautogui.click(length_middle, height_middle)
        pyautogui.click(length_middle, height_middle)
        time.sleep(0.5)

    def populate_board(
        self,
        picture_list: list,
        curr_board: list,
        box_coords: tuple,
        row_param: int,
        col_param: int,
    ) -> None:
        # will check for each picture on the screen
        for current_picture in picture_list.keys():
            # makes a tuple of all the locations of the current picture
            # loops through each location in the tuple
            all_found_locations = pyautogui.locateAllOnScreen(
                current_picture, grayscale=True, confidence=0.85
            )

            """will check through all avaliable coords, incrementing until current set 
            of coordinates are between upper and lower bound. repeats for x and y planes
            """
            for current_coords in all_found_locations:
                row_to_insert: int = 0

                # loop through current rows in board until the location is found
                while row_to_insert + 1 < row_param:
                    bottom_range_rows: int = curr_board[row_to_insert][0].y_position
                    top_range_rows: int = curr_board[row_to_insert + 1][0].y_position
                    if (
                        current_coords.top > bottom_range_rows
                        and current_coords.top < top_range_rows
                    ):
                        break
                    row_to_insert += 1

                # loop through current rows in board until the location is found
                col_to_insert: int = 0
                while col_to_insert + 1 < col_param:
                    bottom_range_cols: int = curr_board[0][col_to_insert].x_position
                    top_range_cols: int = curr_board[0][col_to_insert + 1].x_position
                    if (
                        current_coords.left > bottom_range_cols
                        and current_coords.left < top_range_cols
                    ):
                        break
                    col_to_insert += 1

                # inserts in correct spot based on the coordinates of the found item
                current_cell = curr_board[row_to_insert][col_to_insert]
                current_cell.character = picture_list.get(current_picture)

        # below will add all correct green spaces to the board

        # takes a picture with extra wide of the board to make sure to capture entire thing
        im1 = pyautogui.screenshot(region=(box_coords))
        im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
        # writes the image to "CheckThis.png"
        cv2.imwrite("CheckThis.png", im1)

        check = Image.open("CheckThis.png")
        pix = check.load()

        pic_height: int = check.height
        pic_length: int = check.size[0]

        padding_num: int = 10

        for row in range(row_param):
            for column in range(col_param):
                # checks against the RGB values of the color of a light green or dark green square
                light_green_values = (179, 214, 101)
                dark_green_values = (172, 208, 94)
                current_cell = curr_board[row][column]
                if (
                    current_cell.character != self.BoardValuesObj.flag
                ):  # only assigns a green tile if there is not a flag currently on the cell
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
                        current_cell.character = self.BoardValuesObj.unclicked_square

    """
    Scans and populates the board
    """

    def scan_board(
        self,
        curr_board: list,
        box_coords: tuple,
        row_param: int,
        col_param: int,
        do_deep_scan: bool,
    ) -> None:
        start_time = time.time()
        self.DisplayDataObj.display("\n\nBoard Scan Started")
        # fills board with cells containing brown spaces
        for row in range(row_param):
            for column in range(col_param):
                curr_board[row][column] = self.cell(
                    self.BoardValuesObj.clicked_square,
                    ((box_coords.left) + (column * box_coords.width / col_param)),
                    (box_coords.top) + (row * box_coords.height / row_param),
                )

        # determines which list based on size of board
        if row_param == self.EASY_HEIGHT and do_deep_scan:
            picture_list = {
                "numbers/One.png": self.BoardValuesObj.one,
                "numbers/Two.png": self.BoardValuesObj.two,
                "numbers/Three.png": self.BoardValuesObj.three,
                "numbers/Four.png": self.BoardValuesObj.four,
                "numbers/Five.png": self.BoardValuesObj.five,
                "numbers/Six.png": self.BoardValuesObj.six,
                "numbers/Flag.png": self.BoardValuesObj.flag,
            }
        elif row_param == self.EASY_HEIGHT and not do_deep_scan:
            picture_list = {
                "numbers/One.png": self.BoardValuesObj.one,
                "numbers/Two.png": self.BoardValuesObj.two,
                "numbers/Three.png": self.BoardValuesObj.three,
                "numbers/Flag.png": self.BoardValuesObj.flag,
            }
        elif row_param == self.MEDIUM_HEIGHT and do_deep_scan:
            picture_list = {
                "numbers/MedOne.png": self.BoardValuesObj.one,
                "numbers/MedTwo.png": self.BoardValuesObj.two,
                "numbers/MedThree.png": self.BoardValuesObj.three,
                "numbers/MedFour.png": self.BoardValuesObj.four,
                "numbers/MedFive.png": self.BoardValuesObj.five,
                "numbers/MedSix.png": self.BoardValuesObj.six,
                "numbers/MedSeven.png": self.BoardValuesObj.seven,
                "numbers/MedFlag.png": self.BoardValuesObj.flag,
            }
        elif row_param == self.MEDIUM_HEIGHT and not do_deep_scan:
            picture_list = {
                "numbers/MedOne.png": self.BoardValuesObj.one,
                "numbers/MedTwo.png": self.BoardValuesObj.two,
                "numbers/MedThree.png": self.BoardValuesObj.three,
                "numbers/MedFlag.png": self.BoardValuesObj.flag,
            }
        elif row_param == self.HARD_HEIGHT and do_deep_scan:
            picture_list = {
                "numbers/HardOne.png": self.BoardValuesObj.one,
                "numbers/HardTwo.png": self.BoardValuesObj.two,
                "numbers/HardThree.png": self.BoardValuesObj.three,
                "numbers/HardFour.png": self.BoardValuesObj.four,
                "numbers/HardFive.png": self.BoardValuesObj.five,
                "numbers/MedSix.png": self.BoardValuesObj.six,
                "numbers/HardFlag.png": self.BoardValuesObj.flag,
            }
        elif row_param == self.HARD_HEIGHT and not do_deep_scan:
            picture_list = {
                "numbers/HardOne.png": self.BoardValuesObj.one,
                "numbers/HardTwo.png": self.BoardValuesObj.two,
                "numbers/HardThree.png": self.BoardValuesObj.three,
                "numbers/HardFlag.png": self.BoardValuesObj.flag,
            }

        self.populate_board(picture_list, curr_board, box_coords, row_param, col_param)

        end_time = time.time()
        board_scan_message = (
            "Board Scan complete in " + str((end_time - start_time)) + " seconds"
        )
        self.DisplayDataObj.display(board_scan_message)

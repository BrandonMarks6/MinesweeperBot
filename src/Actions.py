"""
this file will hold all of the action funtions to work on the board
"""
import pyautogui

# constants
PADDING_FACTOR = 20
PIXEL_DIVISION_FACTOR = (
    2  # Is used to convert coordinates from pyautogui to correct location
)


def click_all_around(board, row, col, max_row, max_col):
    # will loop through the 3x3 grid of cells around passed in cell
    for curr_row in range(row - 1, row + 2):
        for curr_col in range(col - 1, col + 2):
            if (
                0 <= curr_row < max_row  and 0 <= curr_col < max_col
            ):  # tests to make sure number is in correct range
                current_space = board[curr_row][curr_col]

                if (
                    not current_space.clicked and current_space.val == "-"
                ):  # if cell has not already been clickd and it is a correct value,
                    #click it and mark as clicked
                    pyautogui.click(
                        current_space.coord1 / PIXEL_DIVISION_FACTOR + PADDING_FACTOR,
                        current_space.coord2 / PIXEL_DIVISION_FACTOR + PADDING_FACTOR,
                    )
                    current_space.clicked = True


def right_click_all_around(board, row, col, max_row, max_col):
    # will loop through the 3x3 grid of cells around passed in cell
    for curr_row in range(row - 1, row + 2):
        for curr_col in range(col - 1, col + 2):
            if (
                0 <= curr_row < max_row and 0 <= curr_col < max_col
            ):  # tests to make sure number is in correct range
                current_space = board[curr_row][curr_col]

                if (
                    not current_space.clicked and current_space.val == "-"
                ):  # if cell has not already been clickd and it is a correct value,
                    #click it and mark as clicked
                    pyautogui.rightClick(
                        current_space.coord1 / PIXEL_DIVISION_FACTOR + PADDING_FACTOR,
                        current_space.coord2 / PIXEL_DIVISION_FACTOR + PADDING_FACTOR,
                    )
                    board[curr_row][curr_col].val = "X"

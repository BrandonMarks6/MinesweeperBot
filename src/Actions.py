"""
this file will hold all of the action funtions to work on the board
"""
import pyautogui


class Actions:
    def __init__(self, board_values) -> None:
        self.board_values = board_values

    # constants
    MINIMUM_ROW_COL = 0
    PADDING_FACTOR: int = 20
    PIXEL_DIVISION_FACTOR: int = (
        2  # Is used to convert coordinates from pyautogui to correct location
    )

    def click_all_around(
        self, board: list, row: int, col: int, max_row: int, max_col: int
    ) -> None:
        low_bound_row = row - 1
        up_bound_row = row + 2
        low_bound_col = col - 1
        up_bound_col = col + 2
        # will loop through the 3x3 grid of cells around passed in cell
        for curr_row in range(low_bound_row, up_bound_row):
            for curr_col in range(low_bound_col, up_bound_col):
                if (
                    self.MINIMUM_ROW_COL <= curr_row < max_row
                    and self.MINIMUM_ROW_COL <= curr_col < max_col
                ):  # tests to make sure number is in correct range
                    current_space = board[curr_row][curr_col]
                    if (
                        not current_space.clicked
                        and current_space.character
                        == self.board_values.unclicked_square
                    ):  # if cell has not already been clickd and it is a correct value,
                        # click it and mark as clicked
                        pyautogui.click(
                            current_space.x_position / self.PIXEL_DIVISION_FACTOR
                            + self.PADDING_FACTOR,
                            current_space.y_position / self.PIXEL_DIVISION_FACTOR
                            + self.PADDING_FACTOR,
                        )
                        current_space.clicked = True

    def right_click_all_around(
        self, board: list, row: int, col: int, max_row: int, max_col: int
    ) -> None:
        # will loop through the 3x3 grid of cells around passed in cell
        low_bound_row = row - 1
        up_bound_row = row + 2
        low_bound_col = col - 1
        up_bound_col = col + 2
        # will loop through the 3x3 grid of cells around passed in cell
        for curr_row in range(low_bound_row, up_bound_row):
            for curr_col in range(low_bound_col, up_bound_col):
                if (
                    self.MINIMUM_ROW_COL <= curr_row < max_row
                    and self.MINIMUM_ROW_COL <= curr_col < max_col
                ):  # tests to make sure number is in correct range
                    current_space = board[curr_row][curr_col]

                    if (
                        not current_space.clicked
                        and current_space.character
                        == self.board_values.unclicked_square
                    ):  # if cell has not already been clickd and it is a correct value,
                        # click it and mark as clicked
                        pyautogui.rightClick(
                            current_space.x_position / self.PIXEL_DIVISION_FACTOR
                            + self.PADDING_FACTOR,
                            current_space.y_position / self.PIXEL_DIVISION_FACTOR
                            + self.PADDING_FACTOR,
                        )
                        board[curr_row][curr_col].character = self.board_values.flag

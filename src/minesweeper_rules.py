"""
This is a file that holds all the functions to check for patterns in the board that
 is created
"""


class MinesweeperRules:
    # constants
    MINIMUM_ROW_COL = 0

    def __init__(self, action_object, board_values_object, display_object) -> None:
        self.action_object = action_object
        self.board_values_object = board_values_object
        self.display_object = display_object

    # must have the board passed in, will act as a sort of main function to check the
    # board for patterns
    def check_minesweeper_rules(self, board: list) -> int:
        max_row = len(board)
        max_col = len(board[self.MINIMUM_ROW_COL])
        action_taken_counter: int = 0
        for row in range(max_row):
            for column in range(max_col):
                # if set to false, will not visit space again for efficiency purposes
                if board[row][column].test_again is False:
                    continue
                if self.check_around_to_mark(
                    board, row, column, max_row, max_col
                ) or self.check_around_to_clear(board, row, column, max_row, max_col):
                    action_taken_counter += 1
        return action_taken_counter

    # pass the board in, checks if there are as many flags as bombs around a spot
    def check_around_to_clear(
        self, board: list, row: int, col: int, max_row: int, max_col: int
    ) -> bool:
        character = (board[row][col]).character

        if character not in (
            self.board_values_object.clicked_square,
            self.board_values_object.flag,
            self.board_values_object.unclicked_square,
        ):
            # gets number of green spaces and flag spaces
            flag_count = self.count_char_in_surrounding(
                self.board_values_object.flag, board, row, col, max_row, max_col
            )
            green_count = self.count_char_in_surrounding(
                self.board_values_object.unclicked_square,
                board,
                row,
                col,
                max_row,
                max_col,
            )

            # if there is as many flags as there are bombs, click all around
            minimum_greens_to_click = 0
            if flag_count == int(character) and green_count > minimum_greens_to_click:
                self.action_object.click_all_around(board, row, col, max_row, max_col)
                action: str = "Clearing all around " + str(col) + ", " + str(row)
                self.display_object.display(action)
                # to ensure this space wont be tested again
                board[row][col].test_again = False
                return True

        return False

    # pass the board in, checks if there are as man green spaces as
    # there are supposed to be bombs
    def check_around_to_mark(
        self, board: list, row: int, col: int, max_row: int, max_col: int
    ) -> bool:
        character = (board[row][col]).character  # number stores in the current cell

        if character not in (
            self.board_values_object.clicked_square,
            self.board_values_object.flag,
            self.board_values_object.unclicked_square,
        ):
            # 0 index is number of greens around the cell 1 index is number of flags
            flag_count = self.count_char_in_surrounding(
                self.board_values_object.flag, board, row, col, max_row, max_col
            )
            green_count = self.count_char_in_surrounding(
                self.board_values_object.unclicked_square,
                board,
                row,
                col,
                max_row,
                max_col,
            )
            # checks if there are as man green spaces as there are supposed to be bombs,
            # flag all around
            if (green_count + flag_count == int(character)) and int(
                character
            ) - flag_count != 0:
                action: str = (
                    "Adding a flag to every spot around " + str(col) + ", " + str(row)
                )
                self.display_object.display(action)
                self.action_object.right_click_all_around(
                    board, row, col, max_row, max_col
                )
                return True

        return False

    # returns the number of occurences of passed in char in the 8 spaces surrounding
    # the current location
    def count_char_in_surrounding(
        self,
        curr_char: str,
        board: list,
        row: int,
        col: int,
        max_row: int,
        max_col: int,
    ) -> int:
        occurrence_counter: int = 0

        low_bound_row = row - 1
        up_bound_row = row + 2
        low_bound_col = col - 1
        up_bound_col = col + 2
        # will loop through the 3x3 grid of cells around passed in cell
        for curr_row in range(low_bound_row, up_bound_row):
            for curr_col in range(low_bound_col, up_bound_col):
                # tests to make sure number is in correct range
                if (
                    max_row > curr_row >= self.MINIMUM_ROW_COL
                    and max_col > curr_col >= self.MINIMUM_ROW_COL
                ):
                    current_cell = board[curr_row][curr_col]

                    if current_cell.character == curr_char:
                        occurrence_counter += 1

        return occurrence_counter

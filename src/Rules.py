"""
This is a file that holds all the functions to check for patterns in the board that
 is created
"""

import Actions


# must have the board passed in, will act as a sort of main function to check the
# board for patterns
def run_rules(board):
    max_row = len(board)
    max_col = len(board[0])
    action_taken = False
    for row in range(max_row):
        for column in range(max_col):
            # if set to false, will not visit space again for efficiency purposes
            if board[row][column].test_again is False:
                continue
            if check_around_to_mark(
                board, row, column, max_row, max_col
            ) or check_around_to_clear(board, row, column, max_row, max_col):
                action_taken = True
    if not action_taken:
        return 1
    return 0


# pass the board in, checks if there are as many flags as bombs around a spot
def check_around_to_clear(board, row, col, max_row, max_col):
    value = (board[row][col]).val

    if value not in ('.', 'X', '-'):
        # gets number of green spaces and flag spaces
        holder = get_green_and_flag(board, row, col, max_row, max_col)
        flag_count = holder[1]
        green_count = holder[0]

        # if there is as many flags as there are bombs, click all around
        if flag_count == int(value) and green_count > 0:
            Actions.click_all_around(board, row, col, max_row, max_col)
            print("Clear all around " + str(col) + ", " + str(row))
            # to ensure this space wont be tested again
            board[row][col].test_again = False  
            return True
        
    return False


# pass the board in, checks if there are as man green spaces as
# there are supposed to be bombs
def check_around_to_mark(board, row, col, max_row, max_col):
    value = (board[row][col]).val  # number stores in the current cell

    if value not in ('.', 'X', '-'):
        # 0 index is number of greens around the cell 1 index is number of flags
        holder = get_green_and_flag(board, row, col, max_row, max_col)
        flag_count = holder[1]
        green_count = holder[0]
        # checks if there are as man green spaces as there are supposed to be bombs,
        # flag all around
        if (green_count + flag_count == int(value)) and int(value) - flag_count != 0:
            print("Add a flag to every spot around " +
                  str(col) + ", " + str(row))
            Actions.right_click_all_around(board, row, col, max_row, max_col)
            return True
        
    return False


# returns and array [green_counter, flag_counter] of the max_row sqaures
# surrounding the cell
def get_green_and_flag(board, row, col, max_row, max_col):
    flag_counter = check_for_char("X", board, row, col, max_row, max_col)
    green_counter = check_for_char("-", board, row, col, max_row, max_col)

    return [green_counter, flag_counter]


# returns the number of occurences of passed in char in the 8 spaces surrounding
# the current location
def check_for_char(curr_char, board, row, col, max_row, max_col):
    counter = 0

    # will loop through the 3x3 grid of cells around passed in cell
    for curr_row in range(row - 1, row + 2):
        for curr_col in range(col - 1, col + 2):
            # tests to make sure number is in correct range
            if (
                max_row > curr_row >= 0
                and max_col > curr_col >= 0
            ):
                current_cell = board[curr_row][curr_col]

                if current_cell.val == curr_char:
                    counter += 1

    return counter

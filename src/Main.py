#######################################
# Name: Brandon Marks                 #
# Purpose: to play google minesweeper #
#######################################
import BoardFunctions


######################################################################################
# Main Function will find the board then enter the board into the scanner
def main():
    print(
        """Please have a blank version of google 
          minesweeper on your screen so the board can be located"""
    )

    location, row_num, col_num = BoardFunctions.find_board()
    BoardFunctions.run_scanner(location, row_num, col_num)


# calls the main function
if __name__ == "__main__":
    main()
###################################################################################

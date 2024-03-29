#######################################
# Name: Brandon Marks                 #
# Purpose: to play google minesweeper #
#######################################
from board_functions import BoardFunctions
from display_data import DisplayData


######################################################################################
# Main Function will find the board then enter the board into the scanner
def main() -> None:
    BoardFunctionsObj = BoardFunctions()
    DisplayDataObj = DisplayData()

    startMessage: str = """Please have a blank version of google 
          minesweeper on your screen so the board can be located"""

    DisplayDataObj.display(startMessage)

    BoardFunctionsObj.run_program()


# calls the main function
if __name__ == "__main__":
    main()
###################################################################################

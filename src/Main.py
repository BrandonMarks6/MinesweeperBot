#######################################
# Name: Brandon Marks                 #
# Purpose: to play google minesweeper #
#######################################
import BoardFunctions



###########################################################################################################
#Main Function will find the board then enter the board into the scanner with the row and column numbers
def main():
    print("Please have a blank version of google minesweeper on your screen so the board can be located")

    location, rowNum, colNum = BoardFunctions.findBoard()
    BoardFunctions.runScanner(location, rowNum, colNum)

#calls the main function
if __name__ == "__main__":
    main()
###########################################################################################################

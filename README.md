# Minesweeper Bot
A program to play google minesweeper

This program uses a combination of photo recognition and graph traversal algorithms to play Google Minesweeper. The locations of the boxes are based on the location of the original board and calculated based on the size of the board. Once board is scanned, actions are printed to the terminal and are automatically clicked with pyautogui click and right click functionality. The program will loop until the user stops it.

Multiple files were used to seperate main functionality from rules to check and actions to take. The main file does the work of locating and scanning the board as well as calling the rules function, runRules(), to traverse the board. The rules file then checks each space according to the rules and calls the actions neccessary depending on what it sees at and around the current cell.

[Link to Video Showing Bot Play the Game(Easy)](https://youtu.be/cROwUfQSFP8)
[Link to Video Showing Bot Play the Game(Medium)](https://youtu.be/lE4W_x1TUSU)


## Instructions:

* All necessary instructions are audible
* The program can be started with a blank version any level difficulty google minesweeper open
* Once board has been located, user may click the board once to start the game
* All functionality should be taken by the computer aftwards unless guessing situation is encountered
* Program can be quit at anytime by holding the 'q' key until the audible message, "The program has been quit" is read

## Important Notes:

* Written and tested only on M1 Macbook Air in Safari
* Currently works on all modes of Google Minesweeper
* Struggles with Hard mode due to the common situation where there has to be a guess in order to complete

## Possible Future Additions

* Efficiency improvements
* Ability to play on multiple different sites of minesweeper
* Functionality on multiple operating systems







"""
this file will hold all of the action funtions to work on the board
"""
import pyautogui


def clickAllAround(board, row, col, maxRow, maxCol):
    #check down left
    if(row + 1 < maxRow and col - 1 >= 0 and board[row + 1][col - 1].val == '-'):
        if not board[row + 1][col - 1].clicked:
            pyautogui.click(board[row + 1][col - 1].coord1/ 2 + 20, board[row + 1][col - 1].coord2 / 2 + 20)
            board[row + 1][col - 1].clicked = True
    #check down    
    if(row + 1 < maxRow and board[row + 1][col].val == '-'):
        if not board[row + 1][col].clicked:
            pyautogui.click(board[row + 1][col].coord1/ 2 + 20, board[row + 1][col].coord2 / 2 + 20)
            board[row + 1][col].clicked = True
    #check down right
    if(row + 1 < maxRow and col + 1 < maxCol and board[row + 1][col + 1].val == '-'):
        if not board[row + 1][col + 1].clicked:
            pyautogui.click(board[row + 1][col + 1].coord1/ 2 + 20, board[row + 1][col + 1].coord2 / 2 + 20)
            board[row + 1][col + 1].clicked = True
    #check left
    if(col - 1 >= 0) and board[row][col - 1].val == '-':
        if not board[row][col - 1].clicked:
            pyautogui.click(board[row][col - 1].coord1/ 2 + 20, board[row][col - 1].coord2 / 2 + 20)
            board[row][col - 1].clicked = True
    #check right
    if(col + 1 < maxCol and board[row][col + 1].val == '-'):
        if not board[row][col + 1].clicked:
            pyautogui.click(board[row][col + 1].coord1/ 2 + 20, board[row][col + 1].coord2 / 2 + 20)
            board[row][col + 1].clicked = True
    #check up left
    if(row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1].val == '-'):
        if not board[row - 1][col - 1].clicked:
            pyautogui.click(board[row - 1][col - 1].coord1/ 2 + 20, board[row - 1][col - 1].coord2 / 2 + 20)
            board[row - 1][col - 1].clicked = True
    #check up
    if(row - 1 >= 0 and board[row - 1][col].val == '-'):
        if not board[row - 1][col].clicked:
            pyautogui.click(board[row - 1][col].coord1/ 2 + 20, board[row - 1][col].coord2 / 2 + 20)
            board[row - 1][col].clicked = True
    #check up right
    if(row - 1 >= 0 and col + 1 < maxCol and board[row - 1][col + 1].val == '-'):
        if not board[row - 1][col + 1].clicked:
            pyautogui.click(board[row - 1][col + 1].coord1/ 2 + 20, board[row - 1][col + 1].coord2 / 2 + 20)
            board[row - 1][col + 1].clicked = True

def rightClickAllAround(board, row, col, maxRow, maxCol):
    #check down left
    if(row + 1 < maxRow and col - 1 >= 0 and board[row + 1][col - 1].val == '-'):
        pyautogui.rightClick(board[row + 1][col - 1].coord1/ 2 + 20, board[row + 1][col - 1].coord2 / 2 + 20)
        board[row + 1][col - 1].val = 'X'
    #check down    
    if(row + 1 < maxRow and board[row + 1][col].val == '-'):
        pyautogui.rightClick(board[row + 1][col].coord1/ 2 + 20, board[row + 1][col].coord2 / 2 + 20)
        board[row + 1][col].val = 'X'
    #check down right
    if(row + 1 < maxRow and col + 1 < maxCol and board[row + 1][col + 1].val == '-'):
        pyautogui.rightClick(board[row + 1][col + 1].coord1/ 2 + 20, board[row + 1][col + 1].coord2 / 2 + 20)
        board[row + 1][col + 1].val = 'X'
    #check left
    if(col - 1 >= 0 and board[row][col - 1].val == '-'):
        pyautogui.rightClick(board[row][col - 1].coord1/ 2 + 20, board[row][col - 1].coord2 / 2 + 20)
        board[row][col - 1].val = 'X'
    #check right
    if(col + 1 < maxCol and board[row][col + 1].val == '-'):
        pyautogui.rightClick(board[row][col + 1].coord1/ 2 + 20, board[row][col + 1].coord2 / 2 + 20)
        board[row][col + 1].val = 'X'
    #check up left
    if(row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1].val == '-'):
        pyautogui.rightClick(board[row - 1][col - 1].coord1/ 2 + 20, board[row - 1][col - 1].coord2 / 2 + 20)
        board[row - 1][col - 1].val = 'X'
    #check up
    if(row - 1 >= 0 and board[row - 1][col].val == '-'):
        pyautogui.rightClick(board[row - 1][col].coord1/ 2 + 20, board[row - 1][col].coord2 / 2 + 20)
        board[row - 1][col].val = 'X'
    #check up right
    if(row - 1 >= 0 and col + 1 < maxCol and board[row - 1][col + 1].val == '-'):
        pyautogui.rightClick(board[row - 1][col + 1].coord1/ 2 + 20, board[row - 1][col + 1].coord2 / 2 + 20)
        board[row - 1][col + 1].val = 'X'


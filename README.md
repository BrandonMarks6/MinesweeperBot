# MinesweeperBot

## Description
A program to autonomously play Google Minesweeper, built using Python3, pyautogui, and CV2. Using a combination of image recognition and graph traversal techniques, the program achieves times much faster than the average player.

Average Times V1:
- Easy: ~700 seconds
- Medium: ~2400 seconds

Average Times V2 (Optimized Scanning):
- Easy: ~45 seconds
- Medium: ~200 seconds

Average Times V3 (Optimized Action Algorithms):
- Easy: 31 seconds
- Medium: 132 seconds

Average Times V4 (Optimized Scanning and Clicking):
- Easy: 19 seconds
- Medium: 61 seconds

## Gameplay Examples

[Easy](https://youtu.be/NYJF3HAblmw)

[Medium](https://youtu.be/3CfEtC1Apzk)

## Installation and Setup Instructions

#### Example:

Clone down this repository. You will need `Python3` installed globally on your machine.

Run:

`python3 Main.py`

## Reflection

This was a personal project built to explore my interest in image recognition and algorithms in the context of a game I loved playing at the time.

I set out to build a project that autonomously played Minesweeper at a level above the average player.

The main challenge I ran into was optimization. The creation of the project was fairly straightforward, but the optimization is where I really had to research to figure it out. This problem allowed me to explore deeper into optimization of algorithms and how the image recognition was really working to figure out what would be the fastest. This showed me firsthand how important efficiency and optimization can really be when something is running hundreds of times or more.

The main reason I chose Python3 to do this project is because of the extensive library of packages, especially ones pertaining to image recognition. I chose Pyautogui and CV2 due to the way they complement each other, as well as the fact that both of them had some functions that were very critical to this project. The Pyautogui locateAllOnScreen function was integral to the optimization that allowed me to cut times by 10X.

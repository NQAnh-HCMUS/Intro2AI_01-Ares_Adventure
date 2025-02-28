# Description: This file contains all the libraries and constants used in the game.
import pygame
import sys
import random
import math
import numpy as np

# constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
CELL_SIZE = 40
PLAYER_SPEED = 3
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define a color board
color_board = {
    "#": BLACK,  # Walls
    " ": WHITE,  # Free spaces
    "$": GRAY,  # Stones
    "@": GREEN,  # Ares the Player
    ".": RED,  # Switch
    "*": BLUE,  # Stone placed on switch
    "+": YELLOW,  # Ares on a switch
}
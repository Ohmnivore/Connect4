# -*- coding: utf-8 -*-

"""

Usage:
  connect4.py server <address> <port>
  connect4.py client <address> <port>
  connect4.py (-h | --help)

Examples:
  connect4.py server 127.0.0.1 6666
  connect4.py client 127.0.0.1 6666

Options:
  -h, --help

"""

from unicurses import *
from docopt import docopt
import threading
import SocketServer
import socket
import random
import sys

ARGS = docopt(__doc__, None, True, "0.1")
print ARGS

RAW_LEVEL_MAP = ['# # # # # # #',
                 '# # # # # # #',
                 '# # # # # # #',
                 '# # # # # # #',
                 '# # # # # # #',
                 '# # # # # # #']


def win_show(win, label, label_color):
    starty, startx = getbegyx(win)
    height, width = getmaxyx(win)
    box(win, 0, 0)
    mvwaddch(win, 2, 0, ACS_LTEE)
    mvwhline(win, 2, 1, ACS_HLINE, width - 2)
    mvwaddch(win, 2, width - 1, ACS_RTEE)
    print_in_middle(win, 1, 0, width, label, COLOR_PAIR(label_color))


def print_in_middle(win, starty, startx, width, string, color):
    if (win == None): win = stdscr
    y, x = getyx(win)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    wattron(win, color)
    mvwaddstr(win, y, x, string)
    wattroff(win, color)
    refresh()


LEVEL_MAP = ['# # # # # # #',
             '# # # # # # #',
             '# # # # # # #',
             '# # # # # # #',
             '# # # # # # #',
             '# # # # # # #']

TURN = 1
COL = 0
RUNNING = True
LAST_X = -1
LAST_Y = -1
MSG = ""

OBJ_CROSS = 'X'
OBJ_EMPTY = '#'
OBJ_CIRCLE = 'O'
MY_CHAR = 'X'
ENEM_CHAR = 'O'
test = random.randint(0, 1)
IS_TURN = False
if test == 1:
    IS_TURN = True
    MY_CHAR = OBJ_CIRCLE
    ENEM_CHAR = OBJ_CROSS
if test == 0:
    IS_TURN = False
    MY_CHAR = OBJ_CROSS
    ENEM_CHAR = OBJ_CIRCLE
global win

#Refactored from http://stackoverflow.com/questions/20201216/connect-4-check-for-winner-algorithm
def getWinner(l):
    global MY_CHAR
    global ENEM_CHAR
    global OBJ_EMPTY
    LEVEL_MAP = zip(*l[::-1])
    if (LEVEL_MAP[0][0] == MY_CHAR and  LEVEL_MAP[1][0] == MY_CHAR and  LEVEL_MAP[2][0] == MY_CHAR and  LEVEL_MAP[3][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][0] == ENEM_CHAR and  LEVEL_MAP[1][0] == ENEM_CHAR and  LEVEL_MAP[2][0] == ENEM_CHAR and  LEVEL_MAP[3][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][0] == MY_CHAR and  LEVEL_MAP[2][0] == MY_CHAR and  LEVEL_MAP[3][0] == MY_CHAR and  LEVEL_MAP[4][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][0] == ENEM_CHAR and  LEVEL_MAP[2][0] == ENEM_CHAR and  LEVEL_MAP[3][0] == ENEM_CHAR and  LEVEL_MAP[4][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][0] == MY_CHAR and  LEVEL_MAP[3][0] == MY_CHAR and  LEVEL_MAP[4][0] == MY_CHAR and  LEVEL_MAP[5][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][0] == ENEM_CHAR and  LEVEL_MAP[3][0] == ENEM_CHAR and  LEVEL_MAP[4][0] == ENEM_CHAR and  LEVEL_MAP[5][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][0] == MY_CHAR and  LEVEL_MAP[4][0] == MY_CHAR and  LEVEL_MAP[5][0] == MY_CHAR and  LEVEL_MAP[6][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][0] == ENEM_CHAR and  LEVEL_MAP[4][0] == ENEM_CHAR and  LEVEL_MAP[5][0] == ENEM_CHAR and  LEVEL_MAP[6][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][1] == MY_CHAR and  LEVEL_MAP[1][1] == MY_CHAR and  LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][1] == ENEM_CHAR and  LEVEL_MAP[1][1] == ENEM_CHAR and  LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][1] == MY_CHAR and  LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][1] == ENEM_CHAR and  LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR and  LEVEL_MAP[5][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR and  LEVEL_MAP[5][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR and  LEVEL_MAP[5][1] == MY_CHAR and  LEVEL_MAP[6][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR and  LEVEL_MAP[5][1] == ENEM_CHAR and  LEVEL_MAP[6][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][2] == MY_CHAR and  LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][2] == ENEM_CHAR and  LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR and  LEVEL_MAP[6][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR and  LEVEL_MAP[6][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][3] == MY_CHAR and  LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][3] == ENEM_CHAR and  LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR and  LEVEL_MAP[6][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR and  LEVEL_MAP[6][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][4] == MY_CHAR and  LEVEL_MAP[1][4] == MY_CHAR and  LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][4] == ENEM_CHAR and  LEVEL_MAP[1][4] == ENEM_CHAR and  LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][4] == MY_CHAR and  LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][4] == ENEM_CHAR and  LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR and  LEVEL_MAP[5][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR and  LEVEL_MAP[5][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR and  LEVEL_MAP[5][4] == MY_CHAR and  LEVEL_MAP[6][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR and  LEVEL_MAP[5][4] == ENEM_CHAR and  LEVEL_MAP[6][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][5] == MY_CHAR and  LEVEL_MAP[1][5] == MY_CHAR and  LEVEL_MAP[2][5] == MY_CHAR and  LEVEL_MAP[3][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][5] == ENEM_CHAR and  LEVEL_MAP[1][5] == ENEM_CHAR and  LEVEL_MAP[2][5] == ENEM_CHAR and  LEVEL_MAP[3][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][5] == MY_CHAR and  LEVEL_MAP[2][5] == MY_CHAR and  LEVEL_MAP[3][5] == MY_CHAR and  LEVEL_MAP[4][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][5] == ENEM_CHAR and  LEVEL_MAP[2][5] == ENEM_CHAR and  LEVEL_MAP[3][5] == ENEM_CHAR and  LEVEL_MAP[4][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][5] == MY_CHAR and  LEVEL_MAP[3][5] == MY_CHAR and  LEVEL_MAP[4][5] == MY_CHAR and  LEVEL_MAP[5][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][5] == ENEM_CHAR and  LEVEL_MAP[3][5] == ENEM_CHAR and  LEVEL_MAP[4][5] == ENEM_CHAR and  LEVEL_MAP[5][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][5] == MY_CHAR and  LEVEL_MAP[4][5] == MY_CHAR and  LEVEL_MAP[5][5] == MY_CHAR and  LEVEL_MAP[6][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][5] == ENEM_CHAR and  LEVEL_MAP[4][5] == ENEM_CHAR and  LEVEL_MAP[5][5] == ENEM_CHAR and  LEVEL_MAP[6][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][0] == MY_CHAR and  LEVEL_MAP[0][1] == MY_CHAR and  LEVEL_MAP[0][2] == MY_CHAR and  LEVEL_MAP[0][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][0] == ENEM_CHAR and  LEVEL_MAP[0][1] == ENEM_CHAR and  LEVEL_MAP[0][2] == ENEM_CHAR and  LEVEL_MAP[0][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][1] == MY_CHAR and  LEVEL_MAP[0][2] == MY_CHAR and  LEVEL_MAP[0][3] == MY_CHAR and  LEVEL_MAP[0][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][1] == ENEM_CHAR and  LEVEL_MAP[0][2] == ENEM_CHAR and  LEVEL_MAP[0][3] == ENEM_CHAR and  LEVEL_MAP[0][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][2] == MY_CHAR and  LEVEL_MAP[0][3] == MY_CHAR and  LEVEL_MAP[0][4] == MY_CHAR and  LEVEL_MAP[0][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][2] == ENEM_CHAR and  LEVEL_MAP[0][3] == ENEM_CHAR and  LEVEL_MAP[0][4] == ENEM_CHAR and  LEVEL_MAP[0][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][0] == MY_CHAR and  LEVEL_MAP[1][1] == MY_CHAR and  LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[1][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][0] == ENEM_CHAR and  LEVEL_MAP[1][1] == ENEM_CHAR and  LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[1][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][1] == MY_CHAR and  LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[1][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][1] == ENEM_CHAR and  LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[1][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[1][4] == MY_CHAR and  LEVEL_MAP[1][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[1][4] == ENEM_CHAR and  LEVEL_MAP[1][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][0] == MY_CHAR and  LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][0] == ENEM_CHAR and  LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[2][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[2][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[2][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[2][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][0] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][0] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[3][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[3][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[4][0] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[4][0] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[4][1] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[4][1] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR and  LEVEL_MAP[4][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR and  LEVEL_MAP[4][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[5][0] == MY_CHAR and  LEVEL_MAP[5][1] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[5][0] == ENEM_CHAR and  LEVEL_MAP[5][1] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[5][1] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR and  LEVEL_MAP[5][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[5][1] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR and  LEVEL_MAP[5][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[5][2] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR and  LEVEL_MAP[5][4] == MY_CHAR and  LEVEL_MAP[5][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[5][2] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR and  LEVEL_MAP[5][4] == ENEM_CHAR and  LEVEL_MAP[5][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[6][0] == MY_CHAR and  LEVEL_MAP[6][1] == MY_CHAR and  LEVEL_MAP[6][2] == MY_CHAR and  LEVEL_MAP[6][3] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[6][0] == ENEM_CHAR and  LEVEL_MAP[6][1] == ENEM_CHAR and  LEVEL_MAP[6][2] == ENEM_CHAR and  LEVEL_MAP[6][3] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[6][1] == MY_CHAR and  LEVEL_MAP[6][2] == MY_CHAR and  LEVEL_MAP[6][3] == MY_CHAR and  LEVEL_MAP[6][4] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[6][1] == ENEM_CHAR and  LEVEL_MAP[6][2] == ENEM_CHAR and  LEVEL_MAP[6][3] == ENEM_CHAR and  LEVEL_MAP[6][4] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[6][2] == MY_CHAR and  LEVEL_MAP[6][3] == MY_CHAR and  LEVEL_MAP[6][4] == MY_CHAR and  LEVEL_MAP[6][5] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[6][2] == ENEM_CHAR and  LEVEL_MAP[6][3] == ENEM_CHAR and  LEVEL_MAP[6][4] == ENEM_CHAR and  LEVEL_MAP[6][5] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][3] == MY_CHAR and  LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[3][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][3] == ENEM_CHAR and  LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[3][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[1][1] == MY_CHAR and  LEVEL_MAP[0][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[1][1] == ENEM_CHAR and  LEVEL_MAP[0][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][4] == MY_CHAR and  LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][4] == ENEM_CHAR and  LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[1][2] == MY_CHAR and  LEVEL_MAP[0][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[1][2] == ENEM_CHAR and  LEVEL_MAP[0][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[0][5] == MY_CHAR and  LEVEL_MAP[1][4] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[0][5] == ENEM_CHAR and  LEVEL_MAP[1][4] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][5] == MY_CHAR and  LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[0][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][5] == ENEM_CHAR and  LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[0][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][3] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[4][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][3] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[4][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[2][1] == MY_CHAR and  LEVEL_MAP[1][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[2][1] == ENEM_CHAR and  LEVEL_MAP[1][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][4] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][4] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[4][4] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR and  LEVEL_MAP[1][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[4][4] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR and  LEVEL_MAP[1][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[1][5] == MY_CHAR and  LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[1][5] == ENEM_CHAR and  LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[4][5] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[1][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[4][5] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[1][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][3] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR and  LEVEL_MAP[5][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][3] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR and  LEVEL_MAP[5][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[5][3] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR and  LEVEL_MAP[2][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[5][3] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR and  LEVEL_MAP[2][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][4] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[5][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][4] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[5][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[5][4] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR and  LEVEL_MAP[2][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[5][4] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR and  LEVEL_MAP[2][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[2][5] == MY_CHAR and  LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[2][5] == ENEM_CHAR and  LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[5][5] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR and  LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[2][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[5][5] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR and  LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[2][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][3] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[5][1] == MY_CHAR and  LEVEL_MAP[6][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][3] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[5][1] == ENEM_CHAR and  LEVEL_MAP[6][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[6][3] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR and  LEVEL_MAP[4][1] == MY_CHAR and  LEVEL_MAP[3][0] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[6][3] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR and  LEVEL_MAP[4][1] == ENEM_CHAR and  LEVEL_MAP[3][0] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][4] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[5][2] == MY_CHAR and  LEVEL_MAP[6][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][4] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[5][2] == ENEM_CHAR and  LEVEL_MAP[6][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[6][4] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR and  LEVEL_MAP[4][2] == MY_CHAR and  LEVEL_MAP[3][1] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[6][4] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR and  LEVEL_MAP[4][2] == ENEM_CHAR and  LEVEL_MAP[3][1] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[3][5] == MY_CHAR and  LEVEL_MAP[4][4] == MY_CHAR and  LEVEL_MAP[5][3] == MY_CHAR and  LEVEL_MAP[6][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[3][5] == ENEM_CHAR and  LEVEL_MAP[4][4] == ENEM_CHAR and  LEVEL_MAP[5][3] == ENEM_CHAR and  LEVEL_MAP[6][2] == ENEM_CHAR): return ENEM_CHAR
    if (LEVEL_MAP[6][5] == MY_CHAR and  LEVEL_MAP[5][4] == MY_CHAR and  LEVEL_MAP[4][3] == MY_CHAR and  LEVEL_MAP[3][2] == MY_CHAR): return MY_CHAR
    if (LEVEL_MAP[6][5] == ENEM_CHAR and  LEVEL_MAP[5][4] == ENEM_CHAR and  LEVEL_MAP[4][3] == ENEM_CHAR and  LEVEL_MAP[3][2] == ENEM_CHAR): return ENEM_CHAR
    return OBJ_EMPTY


def load_level_map():
    global LEVEL_MAP
    LEVEL_MAP = []
    for i in range(len(RAW_LEVEL_MAP)):
        LEVEL_MAP.append( [] )
        for j in range(len(RAW_LEVEL_MAP[i])):
            LEVEL_MAP[i].append(RAW_LEVEL_MAP[i][j])

def render_game_map():
    # render the map
    mvwaddstr(win, 3, 2, "             ")
    mvwaddstr(win, 3, 2 + 2 * COL, "^")
    for i in range(len(LEVEL_MAP)):
            for j in range(len(LEVEL_MAP[i])):
                obj = LEVEL_MAP[i][j]
                y = i + 4
                x = j + 2
                if obj == OBJ_EMPTY:
                    wattron(win, A_DIM)
                    mvwaddstr(win, y, x, obj)
                    wattroff(win, A_DIM)
                elif obj == OBJ_CIRCLE:
                    wattron(win, COLOR_PAIR(2) | A_BOLD)
                    mvwaddstr(win, y, x, obj)
                    wattroff(win, COLOR_PAIR(2) | A_BOLD)
                elif obj == OBJ_CROSS:
                    wattron(win, COLOR_PAIR(3) | A_BOLD)
                    mvwaddstr(win, y, x, obj)
                    wattroff(win, COLOR_PAIR(3) | A_BOLD)

def render_status_bar():
    global IS_TURN
    attron(A_BOLD)
    if IS_TURN is True:
        mvaddstr(21, 0, "Your turn      ")
    else:
        mvaddstr(21, 0, "Opponent's turn")
    attron(COLOR_PAIR(1))
    mvaddstr(22, 0, str.format("Turn: {0}. Last play at ({1}, {2}).\n{3}",
             TURN, LAST_X, LAST_Y, MSG))
    attroff(COLOR_PAIR(1))
    attroff(A_BOLD)
    #clrtoeol()

def add(col, symbol):
    global LAST_X
    global LAST_Y
    global TURN
    global MSG

    stop = False
    count = 0
    while stop is False:
        if LEVEL_MAP[count + 1][col * 2] != OBJ_EMPTY:
            stop = True
            LEVEL_MAP[count][col * 2] = symbol
            LAST_X = col
            LAST_Y = 5 - count
            TURN += 1
        else:
            count += 1
        if count == 5:
            stop = True
            LEVEL_MAP[count][col * 2] = symbol
            LAST_X = col
            LAST_Y = 5 - count
    if getWinner(LEVEL_MAP) == ENEM_CHAR:
        MSG = "YOU JUST LOST"
        IS_TURN = False
    if getWinner(LEVEL_MAP) == MY_CHAR:
        MSG = "YOU JUST WON"
        IS_TURN = False
    render_game_map()
    render_status_bar()
    update_panels()
    doupdate()

global CLIENT

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    #client = ""

    def handle(self):
        global TO_PLACE
        global IS_TURN
        global RUNNING
        global CLIENT
        # self.request is the TCP socket connected to the client
        while RUNNING:
            CLIENT = self.request
            #print CLIENT
            self.data = self.request.recv(1024)
            if self.data[0] == '0' and IS_TURN is False:
                add(int(self.data[1]), ENEM_CHAR)
                IS_TURN = True
            #print "{} wrote:".format(self.client_address[0])
            #print self.data
            # just send back the same data, but upper-cased
            #self.request.sendall(self.data.upper())

# the main loop

stdscr = initscr()
noecho()
cbreak()
curs_set(0)
keypad(stdscr, True)

start_color()
init_pair(1, COLOR_YELLOW, COLOR_BLACK) # used for the status bar
init_pair(2, COLOR_CYAN, COLOR_BLACK) # used for the walls
init_pair(3, COLOR_RED, COLOR_BLACK) # used for the statues
init_pair(4, COLOR_RED, COLOR_BLACK) # used for low hit points

win = newwin(11, 17, 2, 2)
win_show(win, "Connect 4", 1)
my_panel = new_panel(win)
update_panels()
doupdate()

load_level_map()


def update(conn):
    #clear()
    global COL
    global RUNNING
    global IS_TURN
    global CLIENT
    while RUNNING is True:
        render_game_map()
        update_panels()
        render_status_bar()
        doupdate()

        k = getch()
        if k == KEY_LEFT:
            COL -= 1
        elif k == KEY_RIGHT:
            COL += 1
        elif k == CCHAR('q') or k == CCHAR('Q'):
            clear()
            move(0, 0)
            refresh()
            #getch()
            clear()
            refresh()
            endwin()
            print("Graceful exit...")
            RUNNING = False
            sys.exit()
            if ARGS["server"] is True:
                conn.close()
            if ARGS["client"] is True:
                conn.close()
        elif k == 32:
            if IS_TURN is True:
                add(COL, MY_CHAR)
                IS_TURN = False
                if ARGS["server"] is True:
                    CLIENT.sendall(str.format("0{0}", COL))
                if ARGS["client"] is True:
                    conn.sendall(str.format("0{0}", COL))
        if COL < 0:
            COL = 6
        if COL > 6:
            COL = 0
        #elif k == KEY_UP:
            #move_player(PLAYER_X, PLAYER_Y - 1)
        #elif k == KEY_DOWN:
            #move_player(PLAYER_X, PLAYER_Y + 1)
        #elif k == CCHAR('f'):
            #fight()

if ARGS["server"] is True:
    ##print ARGS["<address>"], ARGS["<port>"]
    #HOST, PORT = ARGS["<address>"], int(ARGS["<port>"])

    ## Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    ## Activate the server; this will keep running until you
    ## interrupt the program with Ctrl-C
    #t = threading.Thread(target=update, args = (server,))
    #t.daemon = True
    #t.start()
    #server.serve_forever()
    global RUNNING

    HOST, PORT = ARGS["<address>"], int(ARGS["<port>"])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    CLIENT, addr = sock.accept()
    if IS_TURN is True:
        turnstr = "11"
    else:
        turnstr = "10"
    CLIENT.sendall(turnstr)
    t = threading.Thread(target=update, args = (sock,))
    t.daemon = True
    t.start()
    #sock.settimeout(1)
    #print 'Connected by', addr
    #sock.sendall("Init")

    while RUNNING is True:
        received = CLIENT.recv(4)
        #if not data: break
        #print received
        if received[0] == '0' and IS_TURN is False:
            IS_TURN = True
            add(int(received[1]), ENEM_CHAR)
    sock.close()
    t.stop()

if ARGS["client"] is True:
    global RUNNING
    HOST, PORT = ARGS["<address>"], int(ARGS["<port>"])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    #sock.sendall("Init")
    t = threading.Thread(target=update, args = (sock,))
    t.daemon = True
    t.start()

    while RUNNING is True:
        received = sock.recv(4)
        #print received
        if received[0] == '0':
            IS_TURN = True
            add(int(received[1]), ENEM_CHAR)
        if received[0] == '1':
            if received[1] == '1':
                IS_TURN = False
                MY_CHAR = OBJ_CROSS
                ENEM_CHAR = OBJ_CIRCLE
            else:
                IS_TURN = True
                MY_CHAR = OBJ_CIRCLE
                ENEM_CHAR = OBJ_CROSS
            render_status_bar()
            doupdate()
    sock.close()
    t.stop()
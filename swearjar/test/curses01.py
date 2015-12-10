#!/usr/bin/python

import curses
import math
import os
import sys
import fcntl
import struct
import termios
import array
import logging
import time

logging.basicConfig(filename='example.log',level=logging.DEBUG)

WELCOME="Chronicles Main Menu"
HELP="<Help> - Instructions"
MENU1="1. Edit Data"


def center(s,n):
	return " "*int(math.floor((n-1-len(s))/2)) + s + " "*(n-len(s)-int(math.floor((n-1-len(s))/2)))

s = curses.initscr()
curses.curs_set(0)
curses.noecho()
#curses.raw()
#curses.cbreak()

MAXY,MAXX = s.getmaxyx()

try:
	s.addnstr(0,     0, center(WELCOME,MAXX), MAXX, curses.A_REVERSE)
	s.addnstr(MAXY-2,    0, center(HELP + " " + str(sys.stdout.isatty()) + " " + str(MAXY) + "," + str(MAXX),MAXX), MAXX, curses.A_REVERSE)
except:
	pass

s.refresh()
time.sleep(0.2)
s.addnstr(5,     4, MENU1, MAXX)

while True:
	s.refresh()
	k = s.getch()
	if chr(k) == 'q': break

	try:
		s.addnstr(MAXY-2,0, center(HELP + " YOU PRESSED A KEY: " + chr(k) + " <" + str(MAXY) + "," + str(MAXX) + ">" ,MAXX),    MAXX, curses.A_REVERSE)
	except:
		pass

curses.endwin()

#!/usr/bin/python

import curses, curses.textpad, curses.ascii
import math, os, sys, fcntl, struct, termios, array, time
import logging

logging.basicConfig(filename='menu01.log',level=logging.DEBUG)

__doc__="""\
The program presents a series of menus that we're going to use for testing.
1. Enter new person
2. Update person
3. Search for person
4. Delete person

The tests will navigate through the menu options and perform various actions.
Below are the test numbers and their corresponding activities.  This series of
tests simulates several data entry scenarios.

  1. After the main menu loads, type "1" to select the option to enter a new person.
  2. On the Enter New Person screen, type in First Name, Last Name, Phone numbers
     with tabs in between to shift fields.
"""

WELCOME="Main Menu"
MENU_HELP="Enter the menu item you want to select"
MENU=["New Person","Edit Person","Delete Person","Exit"]

WELCOME_NEW="Enter New Information"
NEW_HELP="Key in the new information.  Press <tab> to change fields and <enter> to save."
FIELDS=["First Name","Last Name","Identifier","Address","City","State","Zip"]

def center_text(s,n):
	return " "*int(math.floor((n-1-len(s))/2)) + s + " "*(n-len(s)-int(math.floor((n-1-len(s))/2)))

def safe_addnstr(screen, r, c, s, m, a=curses.A_NORMAL):
    try:
        screen.addnstr(r, c, str(s), m, a)
        screen.refresh()
    except:
        logging.debug("Error with safe_addnstr: '%s'"%str(s))
        pass

def safe_clearline(screen, r):
    try:
        safe_addnstr(screen, r, 0, center_text('',MAXX), MAXX-1)
    except:
        logging.debug("Error clearingline %d"%r)
        pass

def textbox_validator(c):
    # Replace <tab> with ^g
    if c == curses.ascii.TAB:
        return curses.ascii.ctrl(ord('g'))
    return c


# Paint the menu screen
def paint_menu():
    safe_addnstr(s, 0,         0, center_text(WELCOME,MAXX), MAXX, curses.A_REVERSE)
    safe_addnstr(s, MAXY-1,    0, MENU_HELP, MAXX)

    r = 5
    i = 1
    for item in MENU:
        safe_addnstr(s, r,     4, str(i) + ". " + item, MAXX)
        r = r + 2
        i = i + 1

# Get input
def get_input(s):
	s.refresh()
	return s.getch()

def new_person(s):
    logging.debug("called new person")
    safe_clearline(s, MAXY-1)
    safe_addnstr(s,MAXY-1,0,"OK, Let's add a new person!", MAXX)
    time.sleep(1)

    s.clear()
    safe_addnstr(s, 0,         0, center_text(WELCOME_NEW,MAXX), MAXX, curses.A_REVERSE)
    safe_addnstr(s, MAXY-1,    0, NEW_HELP, MAXX)

    textwins = {}
    textboxes = {}
    values = {}

    r = 5
    i = 1
    for item in FIELDS:
        safe_addnstr(s, r, 4, item, MAXX)
        logging.debug("Creating data entry box for %s on row %d"%(item,r-1))
        box = curses.newwin(3, MAXX - 6 - 20, r-1, 20)
        box.box()
        box.refresh()
        textwins[item] = curses.newwin(1, MAXX - 6 - 22, r, 22)
        textwins[item].refresh()
        textboxes[item] = curses.textpad.Textbox(textwins[item])
        r = r + 3
        i = i + 1

    #TODO: Create Window and TextBox objects next to each label
    #TODO: Place the cursor, visible in the first box
    #TODO: Capture <tab> to move to next box
    #TODO: Capture <enter> to save the results and return to the main screen

    curses.curs_set(1)
    for item in FIELDS:
        textwins[item].refresh()
        values[item] = textboxes[item].edit(textbox_validator)

    curses.curs_set(0)
    safe_clearline(s, MAXY-1)
    safe_addnstr(s,MAXY-1,0,"Returning to main menu", MAXX)
    time.sleep(1)
    s.clear()

    return values

def edit_person(s):
    values = {}
    logging.debug("called edit person")
    safe_clearline(s, MAXY-1)
    safe_addnstr(s,MAXY-1,0,"OK, Let's edit an existing person!", MAXX)
    return values

def delete_person(s):
    values = {}
    logging.debug("called delete person")
    safe_clearline(s, MAXY-1)
    safe_addnstr(s,MAXY-1,0,"You want to delete someone!  :(", MAXX)
    return values

def invalid_option(s,c):
    logging.debug("called invalid option '%s'"%c)
    safe_clearline(s, MAXY-1)
    safe_addnstr(s,MAXY-1,0,"Please enter one of the listed options. :(", MAXX)
    return True


def end(s):
    return False


## This is main()
s = curses.initscr()
curses.curs_set(0)
curses.noecho()
MAXY,MAXX = s.getmaxyx()
loop = True
values = {}

while loop:
    paint_menu()
    c = chr(get_input(s))
    options = {'1' : new_person,
               '2' : edit_person,
               '3' : delete_person,
               '4' : end}

    if c in options.keys() and c != '4':
        values = options[c](s)
        loop = True
    else:
        if c == '4':
            loop = False
        else:
            loop = invalid_option(s,c)


curses.endwin()

print values

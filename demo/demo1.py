import curses

s = curses.initscr()

s.border(0)
s.addstr(12,25, "Python curses!")
s.refresh()
s.getch()

curses.endwin()



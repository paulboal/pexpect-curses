#!/usr/bin/env python
import sys
import logging
import pexepect

sys.path.append ("/Users/paul/Documents/Workspace/GateOne/")

import terminal

rows=24
cols=80
maxread=65536
cmd="./curses01.py"

term = terminal.Terminal(rows, cols)

child = pexpect.spawn(cmd, maxread=maxread, dimensions=(rows,cols))

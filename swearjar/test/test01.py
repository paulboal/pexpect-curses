#!/usr/bin/env python
import sys
import logging
sys.path.append ("../../")

from swearjar import swearjar


t = swearjar.SwearJar(cmd="./curses01.py")

print (t.dumpascii())

# Test #1 See if we can find a menu that looks like "1. Edit Data"
t.expect("1. Edit", timeout=1)

#!/usr/bin/python

import pexpect
import sys
import logging
import vt102
import os
import time 

def termcheck(child, timeout=0):
	time.sleep(0.05)
	try:
		logging.debug("Waiting for EOF or timeout=%d"%timeout)
		child.expect(pexpect.EOF, timeout=timeout)
	except pexpect.exceptions.TIMEOUT:
		logging.debug("Hit timeout and have %d characters in child.before"%len(child.before))

	return child.before

def termkey(child, stream, screen, key, timeout=0):
	logging.debug("Sending '%s' to child"%key)
	child.send(key)
	s = termcheck(child)
	logging.debug("Sending child.before text to vt102 stream")
	stream.process(child.before)
	logging.debug("vt102 screen dump")
	logging.debug(screen)

# START LOGGING
logging.basicConfig(filename='menu_demo.log',level=logging.DEBUG)

# SETUP VT102 EMULATOR
#rows, columns = os.popen('stty size', 'r').read().split()
rows, columns = (50,120)
stream=vt102.stream()
screen=vt102.screen((int(rows), int(columns)))
screen.attach(stream)
logging.debug("Setup vt102 with %d %d"%(int(rows),int(columns)))


logging.debug("Starting demo2.py child process...")
child = pexpect.spawn('./demo2.py', maxread=65536, dimensions=(int(rows),int(columns)))

s = termcheck(child)
logging.debug("Sending child.before (len=%d) text to vt102 stream"%len(child.before))
stream.process(child.before)
logging.debug("vt102 screen dump")
logging.debug(screen)

termkey(child, stream, screen, "a")
termkey(child, stream, screen, "1")

logging.debug("Quiting...")





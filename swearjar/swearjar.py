# -*- coding: utf-8 -*-

# Meta
__version__ = '0.1'
__version_info__ = (0, 1)
__license__ = "TBD"
__author__ = 'Paul Boal <paul.boal@gmail.com>'

__doc__ = """\
See README.md
"""

import pexpect
import sys
import logging
import vt102
import os
import time

# TODO: Decide how to properly integrate this
sys.path.append ("/Users/paul/Documents/Workspace/GateOne/")
import terminal

class SwearJar:

	def __init__(self, cmd="", dimensions=(24,80), maxread=65536, timeout=5):
		# START LOGGING
		logging.basicConfig(filename='swearjar.log',level=logging.DEBUG)

		self.dimensions = dimensions
		self.maxread = maxread
		self.timeout = timeout
		self.term = terminal.Terminal(dimensions[0],dimensions[1])
		self.child = pexpect.spawn(cmd, maxread=maxread, dimensions=dimensions)
		# time.sleep(1)

	def ascii(self):
		return self.term.dump()

	# Locate a specific piece of data somewhere in the buffer
	# By default search is order is from top left to bottom right
	# TODO: add options for bottom-up search
	def locate(self, str):
		pos = (-1,-1)
		r = 0
		for line in self.term.dump():
			c = line.find(str)
			if c != -1:
				logging.debug("locate() found '%s' at %d, %d", str, r, c)
				pos = (r, c)
				break
			r = r + 1

		return pos


	# This should allow you to pass a series of functions
	# It'll cycle through each function and check which is true,
	# and return the index of the first one that was true.
	# Or maybe you pass a mapping of functions (test, response)
	# TODO: need a "locate" function or option for This
	def expect(self, str, timeout=-1):
		if timeout == -1:
			timeout = self.timeout

		go = True
		start = time.clock()
		end = start + timeout
		logging.debug("Starting at %f and waiting until %f"%(start,end))
		pos = (-1,-1)

		while go:
			self._termcheck()
			# time.sleep(0.05)

			pos = self.locate(str)
			if pos != (-1,-1):
				go = False

			if time.clock() > end:
				logging.debug("expect() timed out!")
				go = False

		return pos

	# Wait for one thing, but return the position of something else.
	def expect_locate(self, str_to_expect, str_to_locate, timeout=-1):
		self.expect(str_to_expect, timeout)
		return self.locate(str_to_locate)

	# There should be some helper functions like:
	# expect_row (row=x, regexp=r)

	def _termcheck(self, timeout=0):
		try:
			c = self.child.read_nonblocking(1, timeout)
			self.term.write(c, special_checks=False)
			logging.debug("Processed character: %d"%ord(c))
			logging.debug(self.term.dump())
		except pexpect.exceptions.TIMEOUT:
			logging.debug("Hit timeout")

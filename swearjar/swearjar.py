#!/usr/env python

import pexpect
import sys
import logging
import vt102
import os
import time

class SwearJar:

	def __init__(self, cmd="", dimensions=(24,80), maxread=65536, timeout=5):
		# START LOGGING
		logging.basicConfig(filename='swearjar.log',level=logging.DEBUG)

		self.dimensions = dimensions
		self.maxread = maxread
		self.timeout = timeout
		self.stream=vt102.stream()
		self.screen=vt102.screen(dimensions)
		self.screen.attach(self.stream)
		self.child = pexpect.spawn(cmd, maxread=maxread, dimensions=dimensions)
		# time.sleep(1)

	def ascii(self):
		return self.screen

	# This should allow you to pass a series of functions
	# It'll cycle through each function and check which is true,
	# and return the index of the first one that was true.
	# Or maybe you pass a mapping of functions (test, response)
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
			r = 0
			for line in self.screen.display:
				c = line.find(str)
				if c != -1:
					go = False
					logging.debug("expect() found '%s' at %d, %d", str, r, c)
					pos = (r, c)
			r = r + 1
			# time.sleep(0.05)

			if time.clock() > end:
				logging.debug("expect() timed out!")
				go = False

		return pos

	# There should be some helper functions like:
	# expect_row (row=x, regexp=r)

	def _termcheck(self, timeout=0):
		try:
			c = self.child.read_nonblocking(1, timeout)
			self.stream.consume(c)
			logging.debug("Processed character: %d"%ord(c))
			logging.debug(self.screen)
		except pexpect.exceptions.TIMEOUT:
			logging.debug("Hit timeout")

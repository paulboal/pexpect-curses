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
		time.sleep(1)
		self.buffer = ""
		self.termcheck()

	def dumpascii(self):
		return self.buffer

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

		while go:
			self.buffer = self.termcheck(timeout)
			for line in self.screen.display:
				# logging.debug("Looking at at '%s'"%line)
				#TODO: I don't think this is working
				if str in line:
					go = False
					logging.debug("expect() found %s", str)
					logging.debug(repr(self.buffer))
			time.sleep(0.05)

			if time.clock() > end:
				logging.debug("expect() timed out!")
				go = False

		pass


	# There should be some helper functions like:
	# expect_row (row=x, regexp=r)

	# TODO: Maybe should just be using self.child.read(1) hear,
	# with a check on the timeout.  Then we know exactly which characters were read, and
	# we can pass that character one at a time to the vt102 stream.
	def termcheck(self, timeout=0):
		time.sleep(0.05)
		try:
			logging.debug("Waiting for EOF or timeout=%d"%timeout)
			self.child.expect(pexpect.EOF, timeout=timeout)
		except pexpect.exceptions.TIMEOUT:
			logging.debug("Hit timeout and have %d characters in child.before"%len(self.child.before))

		# NEED TO KNOW IF WE NEED TO PROCESS NEW CHARACTERS
		if self.buffer != self.child.before:
			self.stream.process(self.child.before)
			self.buffer = self.child.before

	def termkey(self, child, stream, screen, key, timeout=0):
		logging.debug("Sending '%s' to child"%key)
		child.send(key)
		s = termcheck(child)
		logging.debug("Sending child.before text to vt102 stream")
		stream.process(child.before)
		logging.debug("vt102 screen dump")
		logging.debug(screen)

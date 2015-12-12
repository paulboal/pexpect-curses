#!/usr/bin/env python
import sys
import logging
sys.path.append ("../../")
import swearjar

import unittest

class TestSwearJar(unittest.TestCase):

    def test01(self):
        t = swearjar.SwearJar(cmd="./curses01.py")
        (r,c) = t.expect("1. Edit", timeout=1)
        self.assertEqual(r,5)
        self.assertEqual(c,4)

    

if __name__ == '__main__':
    unittest.main()

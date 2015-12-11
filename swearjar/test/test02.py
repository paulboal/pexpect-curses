#!/usr/bin/env python
import sys
import logging
sys.path.append ("../../")

import swearjar


t = swearjar.SwearJar(cmd="ncdu", dimensions=(48,148))


# Test #1 See if we can find a menu that looks like "1. Edit Data"
(r,c) = t.expect("test01", timeout=5)
# (r,c) = t.expect_locate("Menu", "1. Edit", timeout=1)

print (t.ascii())
print ("We found our string at %d, %d"%(r,c))

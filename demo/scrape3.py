import vt102
import subprocess
import time
import os
import sys
import fcntl
import struct
import termios
import array

stream = vt102.stream()
screen = vt102.screen((40,100))
screen.attach(stream)

stream.process(sys.stdin.readall())

print(screen)




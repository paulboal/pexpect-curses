import vt102
import subprocess
import time
import os
import sys
import fcntl
import struct
import termios
import array

class WinchPopen(subprocess.Popen):
    def __init__(self, lines, columns, *args, **kwargs):
        #self._winch_push(lines, columns)
        super(WinchPopen, self).__init__(*args, **kwargs)

    def wait(self):
        super(WinchPopen, self).wait()
        self._winch_pop()

    def _winch_push(self, lines, columns):
        fileno = sys.stdout.fileno()
        # Store window size.
        self.__stored_winsize = array.array('h', [0, 0, 0, 0])
        fcntl.ioctl(fileno, termios.TIOCGWINSZ, self.__stored_winsize, True)
        # Mangle window size.
        buf = array.array('h', [lines, columns, 0, 0])  # struct winsize
	fileno=super(WinchPopen,self).stdout.fileno()
        for fileno in (super(WinchPopen,self)._getstdin().fileno(), super(WinchPopen,self)._getstdout().fileno(),
                       super(WinchPopen,self)._getstderr().fileno()):
            fcntl.ioctl(fileno, termios.TIOCSWINSZ, buf)

    def _winch_pop(self):
        for fileno in (super(WinchPopen,self).stdin.fileno(), super(WinchPopen,self).stdout.fileno(),
                       super(WinchPopen,self).stderr.fileno()):
            fcntl.ioctl(fileno, termios.TIOCSWINSZ,
                        self.__stored_winsize)


stream = vt102.stream()
screen = vt102.screen((40,100))
screen.attach(stream)

p = WinchPopen(columns=100, lines=40, args=['python','demo2.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
fd = p.stdout.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
#fi = p.stdin.fileno()
#fm = fcntl.fcntl(fi, fcntl.F_GETFL)
#fcntl.ioctl(fi, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))

print("sleeping first...")
time.sleep(1)

stream.process(p.stdout.read())

print(screen)

p.communicate('\r\n')



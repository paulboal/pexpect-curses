import vt102
import subprocess
import time
from threading import Thread
from Queue import Queue, Empty

# For capturing output asynchronously
def enq_output(out, queue):
	for line in iter(out.read(1), b''):
		queue.put(line)
	out.close


stream = vt102.stream()
screen = vt102.screen((24,80))
screen.attach(stream)

p = subprocess.Popen(['python','demo2.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
q = Queue()
t = Thread(target=enq_output, args=(p.stdout, q))
t.daemon
t.start()

print("sleeping first...")
time.sleep(1)

try:
	stream.process(q.get_nowait())
except:
	print("no input yet...")

p.communicate('\r\n')
stream.process(p.stdout)

print(screen)


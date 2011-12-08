import guest
import arp
import os
import signal
import subprocess
import shlex
import string

class Perf:
    measures = ["LLC-loads", "LLC-load-misses", "LLC-stores", "LLC-sotre-misses", "LLC-prefetch-misses", "instructions", "cpu-cycles"]

    def __init__(self, pid):
        self.pid = pid
        self.args = shlex.split("sudo perf stat -e LLC-loads -e LLC-load-misses -e LLC-stores -e LLC-store-misses -e LLC-prefetch-misses -e instructions -e cpu-cycles -p " + str(pid))
        self.pipe = None

    def __del__(self):
        self.close()

    def close(self):
        if self.pipe is not None:
            self.pipe.send_signal(signal.SIGINT)

    def get(self):
        result = {}
        self.close()
        if self.pipe is not None:
            (_, out) = self.pipe.communicate()

            for line in out.split('\n'):
                cols = [s for s in line.split(' ') if s != '']
                if len(cols) >= 2 and cols[1] in Perf.measures:
                    result[cols[1]] = int(cols[0].replace(',', ''))

        self.pipe = subprocess.Popen(self.args, stderr = subprocess.PIPE)
        return result

if __name__ == "__main__":
    pass

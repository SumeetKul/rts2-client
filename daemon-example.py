#!/usr/bin/env python

import sys, time, os.path
from daemon import Daemon


class MyDaemon(Daemon):
    def run(self):
        while True:
            while not os.path.exists("/home/sirius/Desktop/lock/lol"):
                time.sleep(1)
            if os.path.isfile("/home/sirius/Desktop/lock/lol"):
                sys.stdout.write(str(lel)+'\n')
            else:
                raise ValueError("%s dne" % "/home/sirius/Desktop/lock/lol")


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import datetime
import signal
import subprocess
import sys
import threading
import time

class Borg:
    """Borg pattern to implement singleton"""

    _collective = {}

    def __new__(cls, *args, **kwargs):
        """new-style borg pattern implementation"""
        self = object.__new__(cls, *args, **kwargs)
        self.__dict__ = cls._collective
        return self

class Event(Borg):
    """Store our threading.Event object"""

    _event = None

    def __init__(self):
        Borg.__init__(self)
        if (self._event == None):
            self._event = threading.Event()

    @property
    def event(self):
        return getattr(self, '_event', None)


def signal_handler(signal, frame):
    """CTRL-C signal handler"""
    Event().event.set()
    sys.exit(1)


def status(target, stop_event):
    """Print the countdown of how much time is left"""
    interval = 1

    # loop while no event occurs
    while (not stop_event.is_set()):
        t = target - time.time()

        # if we are past the target time, exit the loop
        if (t < 0):
            break
        
        print("\rRemaining time: ", str(datetime.timedelta(seconds=round(t))), end="")
        sys.stdout.flush()
        
        # Sleep
        stop_event.wait(interval)

    print()
    print(str(datetime.datetime.now()))


def parse_args():
    """Parse arguments and return amount of seconds"""
    parser = argparse.ArgumentParser()
    parser.add_argument('hours', type=int)
    parser.add_argument('minutes', type=int)
    parser.add_argument('seconds', type=int, nargs='?', default=0)
    args = parser.parse_args()

    return 60 * (60 * args.hours + args.minutes) + args.seconds


def main():
    seconds = parse_args()
    t_stop = Event().event

    # start the thread
    t = threading.Thread(target=status, args=(time.time() + seconds, t_stop))
    t.start()

    # set signal so we can cleanly CTRL-C
    signal.signal(signal.SIGINT, signal_handler)

    # sleep for the required amount of time
    time.sleep(seconds)

    # stop the status thread, and wait for it to finish
    t_stop.set()
    t.join()

    print("Executing...")
    subprocess.call(["/cygdrive/c/Program Files (x86)/AT&T Network Client/NetClient", "-exitnow"])


if __name__ == '__main__':
    main()

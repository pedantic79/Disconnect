#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function

import argparse
import datetime
import platform
import signal
import subprocess
import sys
import threading
import time

class Borg(object):
    """Base class to implement new-style borg pattern"""

    _collective = {}

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls, *args, **kwargs)
        self.__dict__ = cls._collective
        return self


class Event(Borg):
    """Singleton to store and retrieve a threading.Event object"""

    _event = None

    def __init__(self):
        Borg.__init__(self)
        if self._event == None:
            self._event = threading.Event()

    @property
    def event(self):
        return getattr(self, '_event', None)


def signal_handler(signal, frame):
    """CTRL-C signal handler"""
    Event().event.set() # stop the status thread
    sys.exit(1)


def round_half_up(f):
    """Have sane rounding where .5 and higher always rounds away from 0"""
    return int(f + (-.5 if f < 0 else .5)) 


def status(time_delta):
    """Print the countdown of how much time is left"""
    stop_event = Event().event
    target = datetime.datetime.now() + time_delta
    interval = 1

    # loop while no event occurs
    while not stop_event.is_set():
        seconds = round_half_up((target - datetime.datetime.now()).total_seconds())

        # if we are past the target time, exit the loop
        if seconds < 0:
            break
        
        # print time on the same line
        print('\rRemaining: ', str(datetime.timedelta(seconds=seconds)), end='')
        sys.stdout.flush()
        
        # sleep
        stop_event.wait(interval)

    print()
    print('NOW: ', str(datetime.datetime.now()))


def parse_args():
    """Parse arguments and return amount of seconds"""
    parser = argparse.ArgumentParser()
    parser.add_argument('hours', type=int)
    parser.add_argument('minutes', type=int)
    parser.add_argument('seconds', type=int, nargs='?', default=0)
    args = parser.parse_args()

    td = datetime.timedelta(hours=args.hours, minutes=args.minutes, seconds=args.seconds)

    print('ETA: ', str(datetime.datetime.now() + td))
    return td


def main():
    td = parse_args()
    t_stop = Event().event

    # start the thread
    t = threading.Thread(target=status, args=(td,))
    t.start()

    # set signal so we can cleanly CTRL-C
    signal.signal(signal.SIGINT, signal_handler)

    # sleep for the required amount of time
    time.sleep(td.total_seconds())

    # stop the status thread, and wait for it to finish
    t_stop.set()
    t.join()

    print('Executing Disconnect...')
    if platform.system() == 'Darwin':
        subprocess.call(['/opt/cisco/anyconnect/bin/vpn', 'disconnect'])
    else:
        subprocess.call(['/cygdrive/c/Program Files (x86)/AT&T Network Client/NetClient', '-exitnow'])


if __name__ == '__main__':
    main()

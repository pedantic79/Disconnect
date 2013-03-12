#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import time

from threading import Thread
from threading import Event 
from queue import Queue
from datetime import timedelta

def status(target, interval, stop_event):
    """Print the countdown of how much time is left"""

    while True:
        t = target - time.time()
        if (t < 0):
            break
        
        print(str(timedelta(seconds=t)))

        stop_event.wait(interval)

    print("Finished")


def parse_args():
    """Parse arguments and return amount of seconds"""
    parser = argparse.ArgumentParser()
    parser.add_argument('hour', type=int)
    parser.add_argument('minutes', type=int)
    args = parser.parse_args()

    return 60 * (60 * args.hour + args.minutes)


def main():
    seconds = parse_args()

    t_stop = Event()
    t = Thread(target=status, args=(time.time() + seconds, 10, t_stop))
    t.start()


    time.sleep(seconds)

    t_stop.set()
    t.join()
    print("Finished 2")



if __name__ == '__main__':
    main()

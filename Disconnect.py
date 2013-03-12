#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import datetime
import signal
import subprocess
import sys
import threading
import time

def signal_handler(signal, frame):
    """CTRL-C signal handler"""
    t_stop.set()
    sys.exit(1)


def status(target, interval, stop_event):
    """Print the countdown of how much time is left"""


    # loop while no event occurs
    while (not stop_event.is_set()):
        t = target - time.time()

        # if we are past the target time, exit the loop
        if (t < 0):
            break
        
        print("Remaining time: ", str(datetime.timedelta(seconds=round(t))))
        
        # Sleep
        stop_event.wait(interval)

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


    # start the thread
    t = threading.Thread(target=status, args=(time.time() + seconds, 15*60, t_stop))
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



t_stop = threading.Event()
if __name__ == '__main__':
    main()

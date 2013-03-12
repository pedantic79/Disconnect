#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import time
import threading
import datetime

class StatusThread(threading.Thread):
    def run(self):
        print("Hello World")
        print_time()



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('hour', type=int)
    parser.add_argument('minutes', type=int)
    args = parser.parse_args()

    return 60 * (60 * args.hour + args.minutes)

def print_time(seconds=None):
    if (seconds == None):
        s = time.time()
    else:
        s = seconds


    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s)))


def main():
    seconds = parse_args()
    interval = 89

    t = StatusThread()
    t.start()

    print('Sleeping until: ')
    print_time(seconds + time.time())

    while (seconds > interval): 
        print('Sleeping for {0} second(s)'.format(seconds))
        print_time()
        time.sleep(interval)
        seconds -= interval

    print('Sleeping for {0} seconds(s)'.format(seconds))
    print_time()
    time.sleep(seconds)

    print_time()




if __name__ == '__main__':
    main()

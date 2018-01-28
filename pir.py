#!/usr/bin/env python
# sudo nano /etc/rc.local  && add python /opt/scripts/pir.py 2>&1 >/dev/null &
import sys
import time
import RPi.GPIO as io
import subprocess
import datetime

from os import system 
io.setmode(io.BCM)
SHUTOFF_DELAY = 60  # seconds
PIR_PIN = 23       # Pin 26 on the board
ALIVE_START = datetime.time(6, 15)
ALIVE_END = datetime.time(22, 30)

def main():
    io.setup(PIR_PIN, io.IN)
    turned_off = False
    last_motion_time = time.time()
    now_time = datetime.datetime.now().time()

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            sys.stdout.flush()
            if turned_off and time_in_range(ALIVE_START, ALIVE_END, now_time):
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                turn_off()
        time.sleep(.1)

def turn_on():
    system('vcgencmd display_power 1') 

def turn_off():
    system('vcgencmd display_power 0') 

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()

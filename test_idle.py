#!/usr/bin/python
import sys

from bartclock.led_control_lib import BartStrip

numpixels = 60 # Number of LEDs in strip
datapin   = 23
clockpin  = 24

def main():
    bartstrip = BartStrip(numpixels=numpixels, datapin=datapin, clockpin=clockpin)
    bartstrip.idle()


if __name__=='__main__':
    sys.exit(main())

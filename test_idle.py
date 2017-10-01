#!/usr/bin/python

from bartclock.led_control_lib import BartStrip


def main():
    bartstrip = BartStrip(numpixels=numpixels, datapin=datapin, clockpin=clockpin)
    bartstrip.idle()


if __name__=='__main__':
    sys.exit(main())

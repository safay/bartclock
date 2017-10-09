#!/usr/bin/python
import sys
from ConfigParser import ConfigParser
from bartclock.led_control_lib import BartStrip
from bartclock.idle_modes import mode


def main():
    config = ConfigParser()
    config.read("./config.ini")
    bartstrip = BartStrip(int(config.get('led', 'numpixels')),
                          int(config.get('led', 'datapin')),
                          int(config.get('led', 'clockpin')),
                          float(config.get('led', 'gamma')))
    bartstrip.idle(mode=mode.get(config.get('idle', 'mode')))


if __name__=='__main__':
    sys.exit(main())

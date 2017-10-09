import os
import time
from ConfigParser import ConfigParser
from bartclock.bart_lib import departure_info_for_station, trains_are_coming
from bartclock.led_control_lib import BartStrip


def main():
    config = ConfigParser()
    config.read("./config.ini")
    led_strip = BartStrip(int(config.get('led', 'numpixels')),
                          int(config.get('led', 'datapin')),
                          int(config.get('led', 'clockpin')),
                          float(config.get('led', 'gamma')))
    while True:
        bartinfo = departure_info_for_station(url=config.get('bart', 'base_url'),
                                              key=os.environ.get('BART_API_KEY'),
                                              station=config.get('bart', 'origin'))
        if trains_are_coming(bartinfo):
            led_strip.update(bartinfo)
        time.sleep(5)

if __name__ == "__main__":
    main()

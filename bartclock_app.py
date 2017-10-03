import os
import time
from ConfigParser import ConfigParser
from bartclock.bart_lib import departure_info_for_station, trains_are_coming
from bartclock.led_control_lib import BartStrip


def get_configuration():
    config = ConfigParser()
    # optionally set the bartclock config filepath in the environment, otherwise use ./config.ini
    env_config = os.environ.get('BARTCLOCK_CONFIG')
    if env_config:
        config.read(env_config)
    else:
        config.read("./config.ini")
    return config


def main():
    config = get_configuration()
    # set up strip
    led_strip = BartStrip(int(config.get('led', 'numpixels')),
                          int(config.get('led', 'datapin')),
                          int(config.get('led', 'clockpin')))
    # continuous loop
    while True:
        bartinfo = departure_info_for_station(url=config.get('bart', 'base_url'),
                                              key=os.environ.get('BART_API_KEY'),
                                              station=config.get('bart', 'origin'))
        if trains_are_coming(bartinfo):
            led_strip.update(bartinfo)
        time.sleep(3)
        # {'message': None, 'times': {'Richmond': ['Leaving', '21', '40'], 'Warm Springs': ['Leaving', '20', '40']}}

if __name__ == "__main__":
    main()

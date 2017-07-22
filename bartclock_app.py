import os
import time
from ConfigParser import ConfigParser
from bartclock.bart_lib import departure_info_for_station


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
    # continuous loop
    while True:
        info = departure_info_for_station(url=config.get('bart', 'base_url'),
                                          key=os.environ.get('BART_API_KEY'),
                                          station=config.get('bart', 'origin'))
        time.sleep(15)
        # {'message': None, 'times': {'Richmond': ['Leaving', '21', '40'], 'Warm Springs': ['Leaving', '20', '40']}}


if __name__ == "__main__":
    main()

import requests
from xml.etree import ElementTree
from xml import etree

def departure_info_for_station(url, key, station):
    response = requests.get(url.format(station, key))
    response.text
    root = ElementTree.fromstring(response.text)
    info = {}
    trains = {}
    for station_info in root:
        if station_info.tag == 'station':
            for lines in station_info:
                if lines.tag == 'etd':
                    arr_times = []
                    for train_line in lines:
                        if train_line.tag == 'destination':
                            dest = train_line.text
                        if train_line.tag == 'estimate':
                            for incoming in train_line:
                                if incoming.tag == 'minutes':
                                    arr_times.append(incoming.text)
                    trains[dest] = arr_times
        if station_info.tag == 'message':
            info['message'] = station_info.text
    info['times'] = trains
    return info

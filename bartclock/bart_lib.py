import requests
from xml.etree import ElementTree


def get_raw_response_text(url, key, station):
    response = requests.get(url.format(station, key))
    return response.text


def departure_info_for_station(url, key, station):
    raw_response = get_raw_response_text(url, key, station)
    root = ElementTree.fromstring(raw_response)
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
                                if incoming.tag == 'hexcolor':
                                    color = incoming.text
                    trains[dest] = {'times': arr_times, 'color': color}
        if station_info.tag == 'message':
            info['message'] = station_info.text
    info['times'] = trains
    return info

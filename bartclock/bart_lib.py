import requests
from xml.etree import ElementTree


def get_raw_response_text(url, key, station):
    response = requests.get(url.format(station, key))
    return response.text


def departure_info_for_station(url, key, station):
    raw_response = get_raw_response_text(url, key, station)
    assert '<error>' not in raw_response, "found error in response: {}".format(raw_response)
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


#{'message': None, 'times': {'Richmond': {'color': '#ff9933', 'times': ['13', '38', '61']},
                           # 'Warm Springs': {'color': '#ff9933', 'times': ['13', '35']}}}

def trains_are_coming(info):
    # function returns True if trains are coming...
    times = info.get('times').get('Warm Springs').get('times')
    if len(times) > 0:
        return True
    else:
        return False

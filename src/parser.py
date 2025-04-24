import requests
import location
import time

"""
This method is used to get the data from the LRZ API.
:param loc: the location to get the data from
"""


def get_location_data(loc: location):
    url = "http://graphite-kom.srv.lrz.de/render/?from=-10minutes&target=ap.ap*-?" + loc.lrz_subdistrict_id + "*.ssid.*&format=json"
    time.sleep(1)  # sleep to prevent ratelimit from Api
    data_list = requests.get(url, timeout=30).json()
    if not data_list or None:
        raise ConnectionError("Could not get or parse the json from LRZ")
    if loc.specific_access_points is not None:
        for ap in data_list:
            for i in loc.specific_access_points:
                if i in ap["target"]:
                    datapoint = ap["datapoints"][-2]  # get the second last datapoint to prevent inconsistent data
                    loc.timestamp = datapoint[1]
                    loc.update_clients(datapoint[0])
    else:
        for ap in data_list:
            datapoint = ap["datapoints"][0]
            loc.timestamp = datapoint[1]
            loc.update_clients(datapoint[0])


"""
This method is used to calculate the percentage of the current clients to the maximum clients.
:param loc: the location object to calculate the percentage of
"""


def percentage_calculator(loc: location):
    percent = (loc.clients / loc.static_max_clients)*100
    percent = round(percent, 1)
    if percent > 100:
        percent = 100
    return percent

import requests

from src.location_model import Location


class lrz_Api_Parser:
    """
    This method is used to get the data from the LRZ API.
    :param loc: the location to get the data from
    """
    def get_location_data(loc: Location):
        url = "http://graphite-kom.srv.lrz.de/render/?from=-10minutes&target=ap.ap*-?" + loc.lrz_subdistrict_id + "*.ssid.*&format=json"
        data_list = requests.get(url, timeout=30).json()
        if not data_list or None:
            print("Could not get or parse the json from LRZ")
        loc.append_new_client_row() #apped new row to client list
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

    def percentage_calculator(loc: Location):
        percent = int((loc.clients[-1] / loc.static_max_clients)*100)
        if percent > 100:
            percent = 100
        if percent < 7:
            percent = 7
        return percent

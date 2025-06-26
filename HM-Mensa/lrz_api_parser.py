import requests
import logging

from src.location_model import Location


class lrz_Api_Parser:
    """
    This method is used to get the data from the LRZ API.
    :param loc: the location to get the data from
    """
    def get_location_data(loc: Location):
        logging.info(f"Fetching LRZ API data for location: {loc.name}, subdistrict ID: {loc.lrz_subdistrict_id}")
        url = "http://graphite-kom.srv.lrz.de/render/?from=-10minutes&target=ap.ap*-?" + loc.lrz_subdistrict_id + "*.ssid.*&format=json"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data_list = response.json()
            
            if not data_list:
                logging.error(f"Empty response from LRZ API for location: {loc.name}")
                print("Could not get or parse the json from LRZ")
                return

            logging.debug(f"Successfully retrieved data from LRZ API for location: {loc.name}, data points: {len(data_list)}")
            
            loc.append_new_client_row() #apped new row to client list
            if loc.specific_access_points is not None:
                for ap in data_list:
                    for i in loc.specific_access_points:
                        if i in ap["target"]:
                            datapoint = ap["datapoints"][-2]  # get the second last datapoint to prevent inconsistent data
                            loc.timestamp = datapoint[1]
                            loc.update_clients(datapoint[0])
                            logging.debug(f"Updated clients for {loc.name}, AP: {i}, clients: {datapoint[0]}")
            else:
                for ap in data_list:
                    datapoint = ap["datapoints"][0]
                    loc.timestamp = datapoint[1]
                    loc.update_clients(datapoint[0])
                    logging.debug(f"Updated clients for {loc.name}, AP target: {ap['target']}, clients: {datapoint[0]}")
                    
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from LRZ API for {loc.name}: {str(e)}")
        except (ValueError, KeyError, IndexError) as e:
            logging.error(f"Error parsing LRZ API response for {loc.name}: {str(e)}")


    """
    This method is used to calculate the percentage of the current clients to the maximum clients.
    :param loc: the location object to calculate the percentage of
    """

    def percentage_calculator(loc: Location):
        logging.debug(f"Calculating percentage for {loc.name}: current clients={loc.clients[-1]}, max clients={loc.static_max_clients}")
        percent = int((loc.clients[-1] / loc.static_max_clients)*100)
        if percent > 100:
            percent = 100
            logging.debug(f"Percentage for {loc.name} capped at 100%")
        if percent < 7:
            percent = 0
            logging.debug(f"Percentage for {loc.name} set to minimum 0%")
        logging.info(f"Calculated capacity for {loc.name}: {percent}%")
        return percent
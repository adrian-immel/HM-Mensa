
from location import Location
import yaml

import parser
import html_render

"""
This method runs every 5 minutes.
Its the main method of the program to get data and create the json files.
"""
if __name__ == "__main__":
    location_list: list = [Location("Cafeteria Karlstraße","cafe_karl.html", "rf", 100, ["apa06-4rf"]),
                           Location("Mensa Lothstraße","index.html", "rh", 280, ["apa02-1rh", "apa03-1rh", "apa05-0rh", "apa06-0rh"]),
                           Location("Mensa Pasing","mensa_pasing.html", "rl", 120, ["apa15-0rl", "apa18-0rl"])]
    for location_object in location_list:
        parser.get_location_data(location_object)
        location_object.capacity_level_in_percent = parser.percentage_calculator(location_object)
        html_render.render_barometer_html(location_object)

    #print(yaml.dump(location_list))

    #for location_object in location_list:
    #    jsonConverter.json_creator(location_object, location_object.name)
    #jsonConverter.json_creator(location_list, "all")
    #print("job run at", time.time())

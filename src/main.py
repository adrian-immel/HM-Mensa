
from flask import Flask, send_from_directory, jsonify
from flask_crontab import Crontab
import lrzApiParser
from location import Location
from src.json_location_object import Json_Location


listofjsonLocationObjects: list = []
location_list: list = [Location("StuCafe Karlstraße","cafe_karl.html", "rf", 75, ["apa06-4rf"]),
                           Location("Mensa Lothstraße","index.html", "rh", 280, ["apa02-1rh", "apa03-1rh", "apa06-0rh", "apa05-0rh"]),
                           Location("Mensa Pasing","mensa_pasing.html", "rl", 130, ["apa15-0rl", "apa18-0rl"]),
                           Location("StuCafe Pasing","cafe_pasing.html", "rl", 80, ["apa16-1rl"]),
                           Location("StuCafe Lothstraße","cafe_loth.html", "rr", 85, ["apa36-0rr"])]
app = Flask(__name__)
crontab = Crontab(app)


# Serve index.html from the current directory
@app.route('/')
def index():
   return send_from_directory('../public', 'index.html')


# API endpoint
@app.route('/api')
def api():
    return jsonify(listofjsonLocationObjects)

"""
This method runs every 5 minutes.
Its the main method of the program to get data and create the json files.
"""
@crontab.job(minute="*/5", hour="*", day="*", month="*", day_of_week="*")
def run_schedule():
    temp_listofjsonLocationObjects: list = []
    global listofjsonLocationObjects
    for location_object in location_list:
        lrzApiParser.get_location_data(location_object)
        location_object.capacity_level_in_percent = lrzApiParser.percentage_calculator(location_object)
        json_object = Json_Location(location_object.name, location_object.static_max_clients, location_object.clients,
                      location_object.capacity_level_in_percent, location_object.timestamp)
        temp_listofjsonLocationObjects.append(json_object.get_json())
    listofjsonLocationObjects = temp_listofjsonLocationObjects

if __name__ == '__main__':
    run_schedule()
    print(listofjsonLocationObjects)
    app.run()
else:
    # This runs when imported by a WSGI server
    crontab.init_app(app)



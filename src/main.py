
from flask import Flask, send_from_directory, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from src.json_location_model import Json_Location
from  lrz_api_parser import lrz_Api_Parser
import yaml_parser
import trend_calculator
import time

from src.menu_Api_model import menu_Api_model

app = Flask(__name__)
listofjsonLocationObjects: list = []
list_of_menu_models: list = [menu_Api_model]
location_list: list = yaml_parser.get_location_list()

"""
This method runs every 5 minutes.
Its the main method of the program to get data and create the json files.
"""
def run_schedule():
    temp_listofjsonLocationObjects: list = []
    global listofjsonLocationObjects
    for location_object in location_list:
        lrz_Api_Parser.get_location_data(location_object)
        location_object.capacity_level_in_percent = lrz_Api_Parser.percentage_calculator(location_object)
        trend = trend_calculator.calculate_trend(location_object.clients)
        json_object = Json_Location(location_object.name, location_object.static_max_clients, location_object.clients[-1],
                      location_object.capacity_level_in_percent, location_object.timestamp, trend, location_object.canteen_id)
        temp_listofjsonLocationObjects.append(json_object.get_json())
    listofjsonLocationObjects = temp_listofjsonLocationObjects
    print("Data updated from LRZ")



# Serve index.html from the current directory
@app.route('/')
def index():
   return send_from_directory('../public', 'index.html')


# API endpoint
@app.route('/api')
def capacity_api():
    return listofjsonLocationObjects


@app.route('/api/menu', methods=['GET'])
def menue_api():
    location = request.args.get('location')
    return filter(lambda x: x.location_name == location, listofjsonLocationObjects)


if __name__ == '__main__':
    run_schedule()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(run_schedule,
                  trigger='cron',
                  minute='6/5', # läuft alle 5 min um 6 nach (da die lrz api extrem langsam zum updaten ist
                  second=45)
    sched.start()
    print(location_list)
    app.run()

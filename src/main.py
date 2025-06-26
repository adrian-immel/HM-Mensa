import json
from dataclasses import asdict

from flask import Flask, send_from_directory, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from src.json_location_model import Json_Location
from  lrz_api_parser import lrz_Api_Parser
import yaml_parser
import trend_calculator
import time

from src.menu_Api_model import Menu_Api_Model

app = Flask(__name__)


listofjsonLocationObjects: list = []
location_list: list = yaml_parser.get_location_list()
list_of_menu_models: list[Menu_Api_Model]

"""
This method runs every 5 minutes.
Its the main method of the program to get data and create the json files.
"""
def run_schedule_capacity():
    temp_listofjsonLocationObjects: list = []
    global listofjsonLocationObjects
    for location_object in location_list:
        lrz_Api_Parser.get_location_data(location_object)
        location_object.capacity_level_in_percent = lrz_Api_Parser.percentage_calculator(location_object)
        trend = trend_calculator.calculate_trend(location_object.clients)
        json_object = Json_Location(location_object.name, location_object.static_max_clients, location_object.clients[-1],
                      location_object.capacity_level_in_percent, location_object.timestamp, trend, location_object.canteen_id)
        temp_listofjsonLocationObjects.append(json_object)
    listofjsonLocationObjects = temp_listofjsonLocationObjects
    print("Data updated from LRZ")

def run_schedule_menu():
    global list_of_menu_models
    temp_list_of_menu_models: list[Menu_Api_Model] = []
    for location in location_list:
        if location.canteen_id is not None:
            temp_list_of_menu_models.append(Menu_Api_Model(location.canteen_id))
    for menu_model in temp_list_of_menu_models:
        menu_model.fill_dishes_for_today()
    list_of_menu_models = temp_list_of_menu_models


# Serve index.html from the current directory
@app.route('/')
def index():
   return send_from_directory('../public', 'index.html')


# API endpoint
@app.route('/api/capacity', methods=['GET'])
def capacity_api():
    location = request.args.get('location')
    for location_object in listofjsonLocationObjects:
        if location_object.name == location:
            return jsonify(asdict(location_object))
    return jsonify([asdict(location) for location in listofjsonLocationObjects])



@app.route('/api/menu', methods=['GET'])
def menu_api():
    canteen_id = request.args.get('canteen_id')
    for menu_model in list_of_menu_models:
        if menu_model.canteen_id == canteen_id:
            return jsonify(asdict(menu_model))
    return jsonify([asdict(menu) for menu in list_of_menu_models])

if __name__ == '__main__':
    run_schedule_capacity()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(run_schedule_capacity,
                  trigger='cron',
                  minute='6/5',  # every 5 min at 6 after (the LRZ api is really slow)
                  second=45)

    sched.add_job(run_schedule_menu,
                  trigger='cron',
                  hour='0',
                  second=30) # every day at 00:00 and 30 sec
    sched.start()
    print(location_list)
    run_schedule_menu()
    app.run()
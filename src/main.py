from dataclasses import asdict
import logging
import os
from datetime import datetime

from flask import Flask, send_from_directory, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from src.json_location_model import Json_Location
from src.lrz_api_parser import lrz_Api_Parser
import src.yaml_parser as yaml_parser
import src.trend_calculator as trend_calculator
from src.eat_api_parser import update_menu

from src.menu_Api_model import Menu_Api_Model

# Configure logging
def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure file and console handlers
    log_filename = f"logs/hm_mensa_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging initialized")

app = Flask(__name__)

listofjsonLocationObjects: list = []
location_list: list = []
list_of_menu_models: list[Menu_Api_Model] = []

"""
This method runs every 5 minutes.
Its the method of the program to get capacity data from LRZ.
"""
def run_schedule_capacity():
    logging.info("Starting scheduled capacity data update from LRZ")
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
    logging.info("Data updated from LRZ for all locations")

"""
This method runs every night a 0 a Clock.
Its the method of the program to get menu data from the Tum Api.
"""
def run_schedule_menu():
    global list_of_menu_models
    temp_list_of_menu_models: list[Menu_Api_Model] = []
    for location in location_list:
        if location.canteen_id is not None:
            temp_list_of_menu_models.append(Menu_Api_Model(location.canteen_id))
    for menu_model in temp_list_of_menu_models:
        menu_model.fill_dishes_for_today()
    list_of_menu_models = temp_list_of_menu_models
    logging.info("Menu data updated for all canteens")


# Serve index_old.html from the current directory
@app.route('/')
def index():
   return send_from_directory('public', 'index.html')


# API endpoint capacity
@app.route('/api/capacity', methods=['GET'])
def capacity_api():
    location = request.args.get('location')
    if location:
        for location_object in listofjsonLocationObjects:
            if location_object.name == location:
                return jsonify(asdict(location_object))
    return jsonify([asdict(location) for location in listofjsonLocationObjects])


# API endpoint menu
@app.route('/api/menu', methods=['GET'])
def menu_api():
    canteen_id = request.args.get('canteen_id')

    if canteen_id:
        for menu_model in list_of_menu_models:
            if menu_model.canteen_id == canteen_id:
                return jsonify(asdict(menu_model))
    return jsonify([asdict(menu) for menu in list_of_menu_models])

if __name__ == '__main__':
    setup_logging()
    logging.info("Loading location data from YAML configuration")
    location_list = yaml_parser.get_location_list()
    
    logging.info("Running initial LRZ data update")
    run_schedule_capacity()

    logging.info("Running initial menu data update")
    run_schedule_menu()

    logging.info("Setting up scheduler")
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
    
    logging.info("Loaded locations: " + ", ".join([loc.name for loc in location_list]))

    logging.info("Starting Flask web server")
    app.run()
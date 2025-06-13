"""
This class is used to store the data of a location.
"""
import jsonpickle
from datetime import datetime
import pytz
from dataclasses import dataclass



@dataclass
class Json_Location:
    name: str
    static_max_clients: int
    clients: int
    capacity_level_in_percent: float
    time: str
    trend: str

    def __init__(self, name: str, static_max_clients: int, clients: int, capacity_level_in_percent: float, timestamp: int, trend: str):
        self.name = name
        self.static_max_clients = static_max_clients
        self.clients = clients
        self.capacity_level_in_percent = capacity_level_in_percent
        self.time = datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Berlin')).strftime('%H:%M')
        self.trend = trend

    def get_json(self):
        return jsonpickle.encode(self, unpicklable=False)
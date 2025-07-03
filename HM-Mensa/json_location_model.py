"""
This class is used to store the data of a location.
"""
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
    trend: str = None
    canteen_id:str = None

    def __init__(self, name: str, static_max_clients: int, clients: int, capacity_level_in_percent: float, timestamp: int, trend: str, canteen_id: str):
        self.name = name
        self.static_max_clients = static_max_clients
        self.clients = clients
        self.capacity_level_in_percent = capacity_level_in_percent
        self.time = datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Berlin')).strftime('%H:%M')
        self.trend = trend
        self.canteen_id = canteen_id

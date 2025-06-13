from collections import deque
from dataclasses import dataclass
from typing import Optional

"""
This class is used to store the data of a location.
"""
@dataclass
class Location:
    name: str
    lrz_subdistrict_id: str
    clients: list = None
    static_max_clients: int = None
    specific_access_points: Optional[list] = None
    capacity_level_in_percent: float = None
    timestamp: int = None

    def __post_init__(self):
        self.clients = []
    """
    This method is used to update the clients of a location.
    :param clients_to_add: the amount of clients to add to the current amount of clients
    """
    def update_clients(self, clients_to_add: int):
        if clients_to_add is not None:
            self.clients[-1] = round(self.clients[-1] + clients_to_add)

    def append_new_client_row(self):
        self.clients.append(0)
        if len(self.clients) > 3:
            self.clients.pop(0)
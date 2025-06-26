from dataclasses import dataclass

import jsonpickle

from eat_api_parser import update_menu
import  dish_model

@dataclass
class Menu_Api_Model:
    canteen_id: str
    dishes_for_today: [dish_model]

    def __init__(self, canteen_id):
        self.canteen_id = canteen_id

    def fill_dishes_for_today(self):
        self.dishes_for_today = update_menu(self.canteen_id)

    def get_json(self):
        return jsonpickle.encode(self, unpicklable=False)
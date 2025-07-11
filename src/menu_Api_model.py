from dataclasses import dataclass


from src.eat_api_parser import update_menu
import  src.dish_model

@dataclass
class Menu_Api_Model:
    canteen_id: str
    dishes_for_today: [src.dish_model]

    def __init__(self, canteen_id):
        self.canteen_id = canteen_id

    def fill_dishes_for_today(self):
        self.dishes_for_today = update_menu(self.canteen_id)

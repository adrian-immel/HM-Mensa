from dataclasses import dataclass
import  dish_model

@dataclass
class menu_Api_model:
    location_name: str
    dishes_for_today: [dish_model]

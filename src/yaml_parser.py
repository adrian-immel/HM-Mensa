import yaml
from yaml import SafeLoader
from location_model import Location
from src.menu_Api_model import Menu_Api_Model


def get_location_list():
    location_list: list[Location] = []
    with open('../config.yml', 'r') as f:
        yaml_data = yaml.load(f, Loader=SafeLoader)
    for item in yaml_data:
        location = Location(
            name=item['name'],
            lrz_subdistrict_id=item['lrz_subdistrict_id'],
            static_max_clients=item['max_clients'],
            specific_access_points=item.get('access_points'),
            canteen_id = item['canteen_id']
        )
        location_list.append(location)
    return location_list

def get_canteen_list():
    canteen_list: list[Menu_Api_Model] = []
    with open('../config.yml', 'r') as f:
        yaml_data = yaml.load(f, Loader=SafeLoader)
    for item in yaml_data:
        menu_Api_model = Menu_Api_Model(canteen_id = item['canteen_id'])
        canteen_list.append(menu_Api_model)
    return canteen_list
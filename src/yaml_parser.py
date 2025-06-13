import yaml
from yaml import SafeLoader
from location_model import Location


def get_location_list():
    location_list: list[Location] = []
    with open('config.yml', 'r') as f:
        yaml_data = yaml.load(f, Loader=SafeLoader)
    for item in yaml_data:
        location = Location(
            name=item['name'],
            lrz_subdistrict_id=item['lrz_subdistrict_id'],
            static_max_clients=item['max_clients'],
            specific_access_points=item.get('access_points')
        )
        location_list.append(location)
    return location_list


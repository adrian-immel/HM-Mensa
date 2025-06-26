import requests
import json
from datetime import datetime
from src.dish_model import dish_model

def update_menu(canteen_id:str):
    url = "https://tum-dev.github.io/eat-api/"+ canteen_id +"/combined/combined.json"
    json_data = requests.get(url, timeout=30).json()
    dishes = get_dishes_for_current_date(json_data)
    if not dishes or None:
        print("Could not get or parse the json from eat-api for location: " + canteen_id)
    return_dishes: list[dish_model] = []
    for dish in dishes:
        return_dishes.append(dish_model(dish['name'], dish['dish_type'], dish.get('labels')))
    return return_dishes

def get_dishes_for_current_date(json_data):
    """
    Extract all dishes for the current date from the canteen JSON data.

    Args:
        json_data: The JSON data as a string or dict

    Returns:
        list: List of dishes for today, or empty list if no data found
    """
    # Parse JSON if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Search through all weeks and days
    for week in data.get("weeks", []):
        for day in week.get("days", []):
            if day.get("date") == current_date:
                return day.get("dishes", [])

    return []
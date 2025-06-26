import requests
import json
import logging
from datetime import datetime
from src.dish_model import dish_model

def update_menu(canteen_id:str):
    logging.info(f"Fetching menu data from eat-api for canteen: {canteen_id}")
    url = "https://tum-dev.github.io/eat-api/"+ canteen_id +"/combined/combined.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()
        
        dishes = get_dishes_for_current_date(json_data)
        
        if not dishes:
            logging.warning("Could not get or parse the json from eat-api for location: " + canteen_id)
            return []

        logging.debug(f"Successfully retrieved {len(dishes)} dishes for canteen: {canteen_id}")
        
        return_dishes: list[dish_model] = []
        for dish in dishes:
            return_dishes.append(dish_model(dish['name'], dish['dish_type'], dish.get('labels')))
            logging.debug(f"Added dish: {dish['name']}, type: {dish['dish_type']}")
            
        return return_dishes
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from eat-api for canteen {canteen_id}: {str(e)}")
        return []
    except (ValueError, KeyError) as e:
        logging.error(f"Error parsing eat-api response for canteen {canteen_id}: {str(e)}")
        return []

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
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON string: {str(e)}")
            return []
    else:
        data = json_data

    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    logging.debug(f"Looking for dishes for date: {current_date}")

    # Search through all weeks and days
    for week in data.get("weeks", []):
        for day in week.get("days", []):
            if day.get("date") == current_date:
                dishes = day.get("dishes", [])
                logging.debug(f"Found {len(dishes)} dishes for today")
                return dishes

    logging.warning(f"No menu data found for date: {current_date}")
    return []
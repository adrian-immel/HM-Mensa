from dataclasses import dataclass

@dataclass

class dish_model:
    dish_name: str
    dish_type: str
    allergies: list



    def __init__(self, dish_name, dish_type, labes):
        self.dish_name = dish_name
        self.dish_type = dish_type
        # Mapping of enum names to their abbreviations/emojis
        label_to_emoji = {
            "GLUTEN": "🌿",
            "WHEAT": "🌾",
            "RYE": "GlR",
            "BARLEY": "GlG",
            "OAT": "GlH",
            "SPELT": "GlD",
            "HYBRIDS": "GlHy",
            "SHELLFISH": "🦀",
            "CHICKEN_EGGS": "🥚",
            "FISH": "🐟",
            "PEANUTS": "🥜",
            "SOY": "🌱",
            "MILK": "🥛",
            "LACTOSE": "🧀",
            "ALMONDS": "ScM",
            "HAZELNUTS": "🌰",
            "WALNUTS": "ScW",
            "CASHEWS": "ScC",
            "PECAN": "ScP",
            "PISTACHIOS": "ScP",
            "MACADAMIA": "ScMa",
            "CELERY": "Sl",
            "MUSTARD": "Sf",
            "SESAME": "Se",
            "SULPHURS": "🔻",
            "SULFITES": "🔺",
            "LUPIN": "Lu",
            "MOLLUSCS": "🐙",
            "SHELL_FRUITS": "🥥",
            "BAVARIA": "🏔️",
            "MSC": "🎣",
            "DYESTUFF": "🎨",
            "PRESERVATIVES": "🥫",
            "ANTIOXIDANTS": "⚗",
            "FLAVOR_ENHANCER": "🔬",
            "WAXED": "🐝",
            "PHOSPHATES": "🔷",
            "SWEETENERS": "🍬",
            "PHENYLALANINE": "💊",
            "COCOA_CONTAINING_GREASE": "🍫",
            "GELATIN": "🍮",
            "ALCOHOL": "🍷",
            "PORK": "🐖",
            "BEEF": "🐄",
            "VEAL": "🐂",
            "WILD_MEAT": "🐗",
            "LAMB": "🐑",
            "GARLIC": "🧄",
            "POULTRY": "🐔",
            "CEREAL": "🌾",
            "MEAT": "🍖",
            "VEGAN": "🫑",
            "VEGETARIAN": "🥕"
        }
        for label in labes:
            if label in label_to_emoji:
                self.allergies.append({label: label_to_emoji[label]})
            else:
                self.allergies.append({label: None})  # Empty string if no acronym found
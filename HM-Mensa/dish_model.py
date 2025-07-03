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

        label_to_german = {
            "GLUTEN": "Gluten",
            "WHEAT": "Weizen",
            "RYE": "Roggen",
            "BARLEY": "Gerste",
            "OAT": "Hafer",
            "SPELT": "Dinkel",
            "HYBRIDS": "Hybridgetreide",
            "SHELLFISH": "Schalentiere",
            "CHICKEN_EGGS": "Hühnereier",
            "FISH": "Fisch",
            "PEANUTS": "Erdnüsse",
            "SOY": "Soja",
            "MILK": "Milch",
            "LACTOSE": "Laktose",
            "ALMONDS": "Mandeln",
            "HAZELNUTS": "Haselnüsse",
            "WALNUTS": "Walnüsse",
            "CASHEWS": "Cashewnüsse",
            "PECAN": "Pekannüsse",
            "PISTACHIOS": "Pistazien",
            "MACADAMIA": "Macadamianüsse",
            "CELERY": "Sellerie",
            "MUSTARD": "Senf",
            "SESAME": "Sesam",
            "SULPHURS": "Schwefel",
            "SULFITES": "Sulfite",
            "LUPIN": "Lupine",
            "MOLLUSCS": "Weichtiere",
            "SHELL_FRUITS": "Schalenfrüchte",
            "BAVARIA": "Bayern",
            "MSC": "MSC",
            "DYESTUFF": "Farbstoffe",
            "PRESERVATIVES": "Konservierungsstoffe",
            "ANTIOXIDANTS": "Antioxidantien",
            "FLAVOR_ENHANCER": "Geschmacksverstärker",
            "WAXED": "gewachst",
            "PHOSPHATES": "Phosphate",
            "SWEETENERS": "Süßungsmittel",
            "PHENYLALANINE": "Phenylalanin",
            "COCOA_CONTAINING_GREASE": "Kakaofett",
            "GELATIN": "Gelatine",
            "ALCOHOL": "Alkohol",
            "PORK": "Schweinefleisch",
            "BEEF": "Rindfleisch",
            "VEAL": "Kalbfleisch",
            "WILD_MEAT": "Wildfleisch",
            "LAMB": "Lammfleisch",
            "GARLIC": "Knoblauch",
            "POULTRY": "Geflügel",
            "CEREAL": "Getreide",
            "MEAT": "Fleisch",
            "VEGAN": "Vegan",
            "VEGETARIAN": "Vegetarisch"
        }
        temp_allergies = []
        for label in labes:
            if label in label_to_emoji:
                temp_allergies.append((label_to_german[label], label_to_emoji[label]))
            else:
                temp_allergies.append((label, None))  # Empty string if no acronym found
        self.allergies = temp_allergies
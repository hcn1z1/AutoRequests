def state_abbreviation(state_name):
    state_dict = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
        "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY"
    }
    return state_dict.get(state_name, "Invalid state name")

def country_code(country_name):
    country_dict = {
        "United States of America": "USA", "Canada": "CA", "United Kingdom": "GB",
        "Germany": "DE", "France": "FR", "Italy": "IT", "Spain": "ES",
        "Australia": "AU", "Japan": "JP", "China": "CN", "India": "IN",
        "Russia": "RU", "Brazil": "BR", "South Korea": "KR", "Mexico": "MX",
        "Netherlands": "NL", "Turkey": "TR", "Sweden": "SE", "Switzerland": "CH"
    }
    return country_dict.get(country_name, "Invalid country name")

def gender_code(gender):
    gender_dict = {
        "Male":"M",
        "Female":"F"
    }
    return gender_dict[gender]
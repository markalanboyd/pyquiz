"""
Functions for accessing the Open Trivia Database API.
"""

import requests
import html

def request_token() -> str:
    """Request a token from the Open Trivia Database API."""
    API_REQUEST_URL = 'https://opentdb.com/api_token.php?command=request'
    
    request = requests.get(API_REQUEST_URL)
    return request.json()['token']

def request_categories() -> dict:
    """Request a list of categories from the Open Trivia Database API."""
    API_REQUEST_URL = 'https://opentdb.com/api_category.php'
    
    request = requests.get(API_REQUEST_URL)
    return request.json()['trivia_categories']

def parse_categories(categories: dict) -> dict:
    """Parse the categories into a dictionary."""
    parsed_categories = {}
    for category in categories:
        parsed_categories[category['id']] = category['name']
    return parsed_categories

def sort_dictionary(dictionary: dict) -> dict:
    """Sort a dictionary by its values."""
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}

def values_to_list(dictionary: dict) -> list:
    """Convert a dictionary's values into a list."""
    return list(dictionary.values())

token = request_token()
categories = request_categories()
categories = parse_categories(categories)
categories = sort_dictionary(categories)
categories = values_to_list(categories)
print(categories)
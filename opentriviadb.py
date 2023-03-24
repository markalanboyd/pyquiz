"""
Functions for accessing the Open Trivia Database API.
"""
import html
import requests
import urllib.parse


def request_token() -> str:
    """Request a token from the Open Trivia Database API."""
    API_REQUEST_URL = 'https://opentdb.com/api_token.php?command=request'
    
    request = requests.get(API_REQUEST_URL)
    return request.json()['token']

token = request_token()

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

def sort_dict_by_values(dictionary: dict) -> dict:
    """Sort a dictionary by its values."""
    return dict(sorted(dictionary.items(), key=lambda item: item[1]))

def values_to_list(dictionary: dict) -> list:
    """Convert a dictionary's values into a list."""
    return list(dictionary.values())

def swap_keys_values(dictionary: dict) -> dict:
    """Swap a dictionary's keys and values."""
    return {value: key for key, value in dictionary.items()}

def list_categories() -> list:
    """Return a list of categories."""
    raw_categories = request_categories()
    parsed_categories = parse_categories(raw_categories)
    sorted_categories = sort_dict_by_values(parsed_categories)
    categories_list = values_to_list(sorted_categories)
    return categories_list

def get_category_id(category: str) -> int:
    """Return the ID of a category."""
    raw_categories = request_categories()
    parsed_categories = parse_categories(raw_categories)
    sorted_categories = sort_dict_by_values(parsed_categories)
    swapped_categories = swap_keys_values(sorted_categories)
    return swapped_categories[category]

def request_questions(token: str, 
                      category: str = None,
                      difficulty: str = '',
                      type: str = '',
                      amount: int = 1) -> dict:
    """Request questions from the Open Trivia Database API."""
    
    params = {
        'token': token,
        'difficulty': difficulty,
        'type': type,
        'amount': amount,
        }
    
    if category != None:
        params['category'] = get_category_id(category)

    encoded_params = urllib.parse.urlencode(params)
    
    API_REQUEST_URL = f'https://opentdb.com/api.php?{encoded_params}'
    request = requests.get(API_REQUEST_URL)
    return request.json()


category = 'Animals'

print(request_questions(token))

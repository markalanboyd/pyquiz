"""
Functions for accessing the Open Trivia Database API.
"""
import html
import requests
import urllib.parse

# Global constants
API_REQUEST_URL = 'https://opentdb.com/api.php'
API_REQUEST_TOKEN_URL = 'https://opentdb.com/api_token.php?command=request'
API_CATEGORY_URL = 'https://opentdb.com/api_category.php'

API_RESPONSE_CODES = {
    0: 'Success',
    1: 'No results',
    2: 'Invalid parameter',
    3: 'Token not found',
    4: 'Token empty',
}

# Functions
def memoize(func):
    """Memoize a function."""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def request_token() -> str:
    """Request a token from the Open Trivia Database API."""
    request = requests.get(API_REQUEST_TOKEN_URL)
    request.raise_for_status()
    return request.json()['token']

def request_categories() -> dict:
    """Request a list of categories from the Open Trivia Database API."""
    request = requests.get(API_CATEGORY_URL)
    request.raise_for_status()
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

@memoize
def get_categories_dict() -> dict:
    """Return a dictionary of categories."""
    raw_categories = request_categories()
    parsed_categories = parse_categories(raw_categories)
    sorted_categories = sort_dict_by_values(parsed_categories)
    return sorted_categories

def list_categories() -> list:
    """Return a list of categories."""
    categories_dict = get_categories_dict()
    categories_list = values_to_list(categories_dict)
    return categories_list

def get_category_id(category: str) -> int:
    """Return the ID of a category."""
    categories_dict = get_categories_dict()
    swapped_categories = swap_keys_values(categories_dict)
    return swapped_categories[category]

def unescape_html_questions(questions: list) -> list:
    """Unescape HTML entities in a list of questions."""
    for question in questions:
        question['question'] = html.unescape(question['question'])
        question['correct_answer'] = html.unescape(question['correct_answer'])
        for answer in question['incorrect_answers']:
            answer = html.unescape(answer)
    return questions

def request_questions(token: str, 
                      category: str = None,
                      difficulty: str = '',
                      type: str = '',
                      amount: int = 10) -> list:
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
    
    api_request_question_url = f'https://opentdb.com/api.php?{encoded_params}'
    request = requests.get(api_request_question_url)
    request.raise_for_status()
    unescaped_request = unescape_html_questions(request.json()['results'])
    return unescaped_request

def parse_questions(questions: list) -> dict:
    """
    Parse the questions into a dictionary of one string per question.
    """
    questions_dict = {}
    for question in questions:
        questions_dict[questions.index(question)] = question['question']
    return questions_dict

def parse_questions_answers(questions: list) -> dict:
    """Parse the answers into a dictionary of one list per question."""
    answers = {}
    for question in questions:
        answers[questions.index(question)] = [
            question['correct_answer'],
            *question['incorrect_answers'],
            ]
    return answers

def parse_questions_correct_answers(questions: list) -> dict:
    """
    Parse the correct answers into a dictionary of one string per 
    question.
    """
    correct_answers = {}
    for question in questions:
        correct_answers[questions.index(question)] = question['correct_answer']
    return correct_answers

def parse_questions_categories(questions: list) -> dict:
    """
    Parse the categories into a dictionary of one string per question.
    """
    categories = {}
    for question in questions:
        categories[questions.index(question)] = question['category']
    return categories

def parse_questions_types(questions: list) -> dict:
    """
    Parse the type of questions into a dictionary of one string per 
    question.
    """
    types = {}
    for question in questions:
        types[questions.index(question)] = question['type']
    return types

def parse_questions_difficulty(questions: list) -> dict:
    """
    Parse the difficulty of questions into a dictionary of one string 
    per question.
    """
    difficulty = {}
    for question in questions:
        difficulty[questions.index(question)] = question['difficulty']
    return difficulty

def main_test() -> None:
    """Test the main functions."""
    token = request_token()
    category = None
    questions = request_questions(token, category=category, amount=1)
    print(
        '\n',
        # questions,'\n',
        parse_questions_categories(questions),'\n',
        parse_questions_difficulty(questions),'\n',
        parse_questions(questions),'\n',
        parse_questions_types(questions),'\n',
        parse_questions_answers(questions),'\n',
        parse_questions_correct_answers(questions),'\n',
        )

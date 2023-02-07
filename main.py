import requests
import json
from html import unescape
import re

# TODO Check if API can be reached, display error message if not
# TODO Add token to API call to prevent same question being served
# TODO Welcome interface where you can set parameters
# TODO Allow user to type name of category, throw error if mispelled
# TODO Organize categories with subcategories
# TODO Organize functions into module
# TODO Multiple choice support
# TODO Add different modes - lightning etc
# TODO Add analysis file that shows category strengths
# TODO Create algorithm that automatically adjusts difficulty
# TODO Look for something more elegant than TKInterface to make GUI nicer

# Priority:
# TODO Keep score
# TODO Keep high score
# TODO Create TKinterface

API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"

CHARACTER_LIMIT = 100

score = 0


def api_request_categories() -> dict:
    """
    Calls to the trivia API and asks for a list of all available categories.

    :return: Dictionary of trivia categories
    """
    categories_response = requests.get(API_CATEGORIES_URL)
    return categories_response.json()


def api_request_question() -> dict:
    """
    Calls to the API using the config.json file and asks for a question. Creates and then returns a dictionary with just the question and answer paired together.

    :return: Dictionary formatted as {"question":str, "answer":str}.
    """
    with open('question_parameters.json') as f:
        question_parameters = json.loads(f.read())
        question_response = requests.get(url=API_URL, params=question_parameters)
    question_json = question_response.json()
    question_dict = {
        "question": unescape(question_json["results"][0]["question"]),
        "answer": unescape(question_json["results"][0]["correct_answer"]),
    }
    return question_dict


def ask_category() -> None:
    """
    Requests a list of the available categories from the trivia API, prints them on screen, and prompts the user to select one. Once the user has selected a category, it modifies the config.json file with the corresponding category ID number.

    :return: None
    """

    categories_json = api_request_categories()['trivia_categories']
    len_categories = len(categories_json)
    print("Select a category:\n")
    for i in range(len_categories):
        category = categories_json[i]['name']
        print(f"{i + 1}. {category}")
    while True:
        try:
            # user_category_input = input("\nCategory: ")
            user_category_input = 1  # Automatically select General Knowledge for debugging
            selected_category_name = categories_json[int(user_category_input) - 1]['name']
            selected_category_id = categories_json[int(user_category_input) - 1]['id']
            write_parameter("category", selected_category_id)
            print(f"\nYou picked: {selected_category_name}")
        except IndexError:
            print(f"Please enter an integer between 1 and {len_categories}")
            continue
        else:
            break


def ask_difficulty() -> None:
    """
    Ask the user to set one of three levels of difficulty (easy, medium, or hard), and then modifies the config.json file with the response.

    :return: None
    """
    difficulty_dict = {
        "e": "easy",
        "m": "medium",
        "h": "hard",
    }
    difficulty = input("What difficulty: Easy, Medium, or Hard? ")[0].lower()
    write_parameter("difficulty", difficulty_dict[difficulty])


def ask_question() -> None:
    """
    Calls the trivia API requesting a question, then asks that question of the user and evaluates whether their answer is correct or not.

    :return: None
    """

    question_dict = api_request_question()
    wrapped_question = wrap_text(question_dict['question'], CHARACTER_LIMIT)
    user_answer = input(f"{wrapped_question} T/F? ")[0].lower()
    question_answer = question_dict['answer'][0].lower()
    if user_answer == question_answer:
        print("Correct!")
    else:
        print("Incorrect.")


def wrap_text(long_string: str, max_characters: int) -> str:
    """
    Inserts a linebreak into long_string that exceeds max_characters and returns it as a string.

    :param long_string:
    A long string to be broken up.
    :param max_characters:
    Maximum number of characters per line.
    :return:
    String with added newline characters if necessary.
    """
    return '\n'.join(re.findall('.{1,%i}' % max_characters, long_string))


def write_parameter(parameter: str, value: str | int) -> None:
    """
    Writes a value to the external question_parameters.json file for a given parameter.

    :param parameter: 'category', 'difficulty', or 'type'
    :param value: String or integer to be written to the parameter. 'category' takes an integer while 'difficulty' and 'type' take strings.
    :return: None
    """
    with open(file='question_parameters.json', mode='r+') as f:
        question_parameters = json.load(f)
        question_parameters[parameter] = value
        f.seek(0)
        json.dump(question_parameters, f, indent=4)
        f.truncate()


ask_difficulty()
ask_category()
while True:
    ask_question()

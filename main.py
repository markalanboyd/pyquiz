import requests
import json
from html import unescape
import re

# TODO Check if API can be reached, display error message if not
# TODO Welcome interface where you can set parameters
# TODO Allow user to type name of category, throw error if mispelled
# TODO Organize categories with subcategories
# TODO Organize functions into module
# TODO Multiple choice support
# TODO Add different modes - lightning etc
# TODO Add analysis file that shows category strengths
# TODO Create algorithm that automatically adjusts difficulty
# TODO Look for something more elegant than TKInterface to make GUI nicer
# TODO Light/dark mode
# TODO Breakout write json as a function in its own library

# Priority:
# TODO Add token to API call to prevent same question being served
# TODO Create TKinterface


API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"

CHARACTER_LIMIT = 100

score = 0
streak = 0
questions = 0


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
    with open('config.json') as f:
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
            write_json("config.json", "category", selected_category_id)
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
    # difficulty = input("What difficulty: Easy, Medium, or Hard? ")[0].lower()
    difficulty = "e"  # for debugging
    write_json("config.json", "difficulty", difficulty_dict[difficulty])


def ask_question() -> None:
    """
    Calls the trivia API requesting a question, then asks that question of the user, evaluates the answer, and increments the score if correct.

    :return: None
    """
    global score
    global streak
    global questions

    question_dict = api_request_question()
    wrapped_question = wrap_text(question_dict['question'], CHARACTER_LIMIT)
    user_answer = input(f"{wrapped_question} T/F? ")[0].lower()
    question_answer = question_dict['answer'][0].lower()
    questions += 1
    if user_answer == question_answer:
        score += 1
        streak += 1
        print("Correct!")
    else:
        streak = 0
        print("Incorrect.")


def display_score() -> None:
    """
    Displays score and streak stats.

    :return: None
    """
    global score
    global streak
    global questions

    try:
        percent = round(score / questions * 100)
    except ZeroDivisionError:
        percent = 0

    high_score = read_json('user_data.json', 'high score')
    best_streak = read_json('user_data.json', 'high streak')

    if score > high_score:
        write_json('user_data.json', 'high score', score)
    if streak > best_streak:
        write_json('user_data.json', 'best streak', streak)

    print(f"\nScore: {score}/{questions} ({percent}%)  Streak: {streak}"
          f"\nHigh Score: {high_score}  Best Streak: {best_streak}\n")


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


def read_json(file_path: str, key: str) -> str | int:
    try:
        with open(file=file_path, mode='r') as file:
            dictionary = json.load(file)
            return dictionary[key]
    except FileNotFoundError:
        pass
    except KeyError:
        return 0


def write_json(file_path: str, key: str, value: str | int) -> None:
    """
    Writes a value to the external .json file for a given parameter.

    :param file_path: .json file to open and/or create.
    :param key: Key to search for.
    :param value: String or integer to be written.
    :return: None
    """
    try:
        with open(file=file_path, mode='r+') as file:
            dictionary = json.load(file)
            dictionary[key] = value
            file.seek(0)
            json.dump(dictionary, file, indent=4)
    except FileNotFoundError:
        with open(file=file_path, mode='w') as file:
            dictionary = {key: value}
            json.dump(dictionary, file, indent=4)


ask_difficulty()
ask_category()
while True:
    display_score()
    ask_question()

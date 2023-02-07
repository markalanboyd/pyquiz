import requests
import json
from html import unescape

# TODO Check if API can be reached, display error message if not
# TODO Add token to API call to prevent same question being served
# TODO Welcome interface where you can set parameters
# TODO Allow user to type name of category, throw error if mispelled
# TODO Organize categories with subcategories

# Priority:
# TODO Refactor category open/write to file to work for any parameter
# TODO Ask for difficulty

API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"

score = 0


def api_request_question() -> dict:
    with open('question_parameters.json') as f:
        question_parameters = json.loads(f.read())
        question_response = requests.get(url=API_URL, params=question_parameters)
    question_json = question_response.json()
    question_dict = {
        "question": unescape(question_json["results"][0]["question"]),
        "answer": unescape(question_json["results"][0]["correct_answer"]),
    }
    return question_dict


def api_request_categories():
    categories_response = requests.get(API_CATEGORIES_URL)
    return categories_response.json()


def ask_category():
    categories_json = api_request_categories()['trivia_categories']
    print(categories_json)
    len_categories = len(categories_json)
    print("Select a category:\n")
    for i in range(len_categories):
        category = categories_json[i]['name']
        print(f"{i + 1}. {category}")
    while True:
        try:
            # user_category_input = input("\nCategory: ")
            user_category_input = 1
            selected_category_name = categories_json[int(user_category_input) - 1]['name']
            selected_category_id = categories_json[int(user_category_input) - 1]['id']
            write_parameter("category", selected_category_id)
            print(f"\nYou picked: {selected_category_name}")
        except IndexError:
            print(f"Please enter an integer between 1 and {len_categories}")
            continue
        else:
            break


def ask_question(question_dict: dict) -> bool:
    user_answer = input(f"{question_dict['question']} T/F? ")[0].lower()
    question_answer = question_dict['answer'][0].lower()
    if user_answer == question_answer:
        print("Correct!")
    else:
        print("Incorrect.")


def write_parameter(parameter: str, value: str | int):
    with open(file='question_parameters.json', mode='r+') as f:
        question_parameters = json.load(f)
        question_parameters[parameter] = value
        f.seek(0)
        json.dump(question_parameters, f, indent=4)
        f.truncate()


ask_category()
while True:
    question = api_request_question()
    ask_question(question)

# question = parse_question(question_response)
# answer = parse_answer(question_response)
#
# print(question)
# print(answer)

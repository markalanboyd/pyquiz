import requests
import json

# TODO Check if API can be reached, display error message if not
# TODO Add token to API call to prevent same question being served
# TODO Welcome interface where you can set parameters
# TODO Allow user to type name of category, throw error if mispelled

# Priority:
# TODO Refactor category open/write to file to work for any parameter

API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"


def api_request_question():
    with open('question_parameters.json') as question_parameters:
        question_response = requests.get(API_URL, question_parameters)
    return question_response.json()


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
            user_category_input = input("\nCategory: ")
            selected_category_name = categories_json[int(user_category_input) - 1]['name']
            selected_category_id = categories_json[int(user_category_input) - 1]['id']
            print(f"\nYou picked: {selected_category_name}")
            with open(file='question_parameters.json', mode='r+') as f:
                question_parameters = json.load(f)
                question_parameters["category"] = selected_category_id
                f.seek(0)
                json.dump(question_parameters, f, indent=4)
                f.truncate()
        except IndexError:
            print(f"Please enter an integer between 1 and {len_categories}")
            continue
        else:
            break


def parse_answer(json):
    return json['results'][0]['correct_answer']


def parse_question(json):
    return json['results'][0]['question']


ask_category()
# question_response = api_request_question()
# question = parse_question(question_response)
# answer = parse_answer(question_response)
#
# print(question)
# print(answer)
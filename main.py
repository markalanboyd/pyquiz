import requests

# TODO Check if API can be reached, display error message if not
# TODO Add token to API call to prevent same question being served
# TODO Welcome interface where you can set parameters
# TODO Allow user to type name of category, throw error if mispelled

question_params = {
    "amount": 1,
    "category": 1,
    "type": "boolean",
}

API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"


def api_request_question():
    question_response = requests.get(API_URL, question_params)
    return question_response.json()


def api_request_categories():
    categories_response = requests.get(API_CATEGORIES_URL, question_params)
    return categories_response.json()


def ask_category():
    categories_json = api_request_categories()['trivia_categories']
    len_categories = len(categories_json)
    print("Pick a category\n")
    for i in range(len_categories):
        category = categories_json[i]['name']
        print(f"{i + 1}. {category}")
    while True:
        try:
            user_category_input = input("\nCategory: ")
            selected_category = categories_json[int(user_category_input) - 1]['name']
        except IndexError:
            print(f"Please enter an integer between 1 and {len_categories}")
            continue
        else:
            break


def define_params():
    pass


def parse_answer(json):
    return json['results'][0]['correct_answer']


def parse_question(json):
    return json['results'][0]['question']


ask_category()

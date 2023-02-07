import requests

# TODO Check if API can be reached, display error message if not
# TODO Add token to API call to prevent same question being served
# TODO Welcome interface where you can set parameters

question_params = {
    "amount": 1,
    "type": "boolean",
}

API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"


def define_params():
    pass


def parse_answer(json):
    return json['results'][0]['correct_answer']


def parse_question(json):
    return json['results'][0]['question']


def request_question():
    question_response = requests.get(API_URL, question_params)
    return question_response.json()


def request_categories():
    categories_response = requests.get(API_CATEGORIES_URL, question_params)
    return categories_response.json()


categories_json = request_categories()
num_categories = len(categories_json['trivia_categories'])
for i in range(num_categories):
    category = categories_json['trivia_categories'][i]['name']
    print(f"{i + 1}. {category}")
user_category = input("\nEnter number for category: ")



# question_json = request_question()
# question = parse_question(question_json)
# answer = parse_answer(question_json)
#
# print(question)
# print(answer)







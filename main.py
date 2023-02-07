import requests


question_params = {
    "amount": 1,
    "type": "boolean",
}


def request_question():
    question_response = requests.get("https://opentdb.com/api.php", question_params)
    question_response.raise_for_status()
    return question_response.json()


def parse_question(json):
    return question_json['results'][0]['question']


def parse_answer(json):
    return json['results'][0]['correct_answer']


question_json = request_question()
question = parse_question(question_json)
answer = parse_answer(question_json)

print(question)
print(answer)







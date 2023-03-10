import requests
import json
from html import unescape
import re
from tkinter import *

# Todos
# TODO Check if API can be reached, display error message if not
# TODO Organize categories with subcategories
# TODO Multiple choice support
# TODO Add different modes - lightning etc
# TODO Add analysis file that shows category strengths
# TODO Create algorithm that automatically adjusts difficulty
# TODO Look for something more elegant than TKInterface to make GUI nicer
# TODO Break out classes/refactor
# TODO Link difficulty selector to API request


# Global Variables
API_URL = "https://opentdb.com/api.php"
API_CATEGORIES_URL = "https://opentdb.com/api_category.php"
API_TOKEN_URL = "https://opentdb.com/api_token.php?command=request"

CHARACTER_LIMIT = 100

score = 0
streak = 0
questions = 0
previous_score = 0
difficulty_accumulator = 0

question_dict: dict
question_answered = True

user_answer = ''


# Functions

def api_request_categories() -> dict:
    """
    Calls to the trivia API and asks for a list of all available categories.

    :return: Dictionary of trivia categories
    """
    categories_response = requests.get(API_CATEGORIES_URL)
    return categories_response.json()


def api_request_token() -> None:
    token_response = requests.get(API_TOKEN_URL)
    token_string = token_response.json()['token']
    write_json('config.json', key='token', value=f"{token_string}")


def api_request_question() -> dict:
    """
    Calls to the API using the config.json file and asks for a question. Creates and then returns a dictionary with just the question and answer paired together.

    :return: Dictionary formatted as {"question":str, "answer":str}.
    """
    global question_dict

    if selected_difficulty.get() == "Auto":
        auto_difficulty()
        update_scoreboard()

    with open('config.json') as f:
        question_parameters = json.loads(f.read())
        question_response = requests.get(url=API_URL, params=question_parameters)
    question_json = question_response.json()
    question_dict = {
        "question": unescape(question_json["results"][0]["question"]),
        "answer": unescape(question_json["results"][0]["correct_answer"]),
    }
    return question_dict


def update_scoreboard() -> None:
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
    best_streak = read_json('user_data.json', 'best streak')

    if score >= high_score:
        write_json('user_data.json', 'high score', score)
    if streak >= best_streak:
        write_json('user_data.json', 'best streak', streak)

    high_score = read_json('user_data.json', 'high score')
    best_streak = read_json('user_data.json', 'best streak')

    current_difficulty = read_json('config.json', 'difficulty')

    label_score.config(text=f'Score: {score}/{questions}  |  {percent}%  |  Streak: {streak}\n'
                            f'High Score: {high_score}  |  Best Streak: {best_streak}\n'
                            f'Current Difficulty: {current_difficulty.title()}')


def read_json(filepath: str, key: str) -> str | int:
    try:
        with open(file=filepath, mode='r') as file:
            dictionary = json.load(file)
            return dictionary[key]
    except FileNotFoundError:
        pass
    except KeyError:
        return 0


def write_json(filepath: str, key: str, value: str | int) -> None:
    """
    Writes a value to the external .json file for a given parameter.

    :param filepath: .json file to open and/or create.
    :param key: Key to search for.
    :param value: String or integer to be written.
    :return: None
    """
    try:
        with open(file=filepath, mode='r+') as file:
            dictionary = json.load(file)
            dictionary[key] = value
            file.seek(0)
            json.dump(dictionary, file, indent=4)
            file.truncate()
    except FileNotFoundError:
        with open(file=filepath, mode='w') as file:
            dictionary = {key: value}
            json.dump(dictionary, file, indent=4)


def raise_frame(frame_to_raise) -> None:
    frame_to_raise.tkraise()


def next_question() -> None:
    """
    Calls the trivia API requesting a question, then asks that question of the user, evaluates the answer, and increments the score if correct.

    :return: None
    """
    global question_answered, question_dict

    button_true.config(highlightbackground='systemTransparent')
    button_false.config(highlightbackground='systemTransparent')

    if question_answered:
        button_next_question.config(state='disabled')
        button_true.config(state='normal')
        button_false.config(state='normal')
        question_answered = False
        question_dict = api_request_question()
        label_game_question.config(text=question_dict['question'])
        button_true.config(command=answer_true)
        button_false.config(command=answer_false)


def check_answer() -> None:
    global user_answer, question_answered, questions, score, streak, previous_score

    question_answered = True
    button_true.config(command='')
    button_false.config(command='')
    questions += 1

    if user_answer == question_dict['answer']:
        score += 1
        streak += 1
    else:
        streak = 0

    update_scoreboard()


def answer_true() -> None:
    global user_answer

    button_next_question.config(state='normal')
    button_true.config(state='active')
    button_false.config(state='disabled')
    user_answer = 'True'

    if question_dict['answer'] == user_answer:
        button_true.config(highlightbackground='green')
    else:
        button_true.config(highlightbackground='red')

    check_answer()


def answer_false() -> None:
    global user_answer

    button_next_question.config(state='normal')
    button_true.config(state='disabled')
    button_false.config(state='active')
    user_answer = 'False'

    if question_dict['answer'] == user_answer:
        button_false.config(highlightbackground='green')
    else:
        button_false.config(highlightbackground='red')

    check_answer()


def reset_stats() -> None:
    write_json('user_data.json', 'high score', 0)
    write_json('user_data.json', 'best streak', 0)


def write_settings() -> None:
    global auto_difficulty_on

    difficulty_setting = selected_difficulty.get().lower()
    if difficulty_setting != "auto":
        write_json("config.json", key="difficulty", value=difficulty_setting)
        auto_difficulty_on = False
    else:
        auto_difficulty_on = True


def clamp(value: int | float, min_value: int | float, max_value: int | float) -> int | float:
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value


def auto_difficulty() -> None:
    global score, previous_score, difficulty_accumulator

    if score > previous_score:
        previous_score += 1
        difficulty_accumulator += 1
    else:
        difficulty_accumulator -= 3
        difficulty_accumulator = clamp(difficulty_accumulator, 0, 9)

    if 0 <= difficulty_accumulator < 3:
        difficulty_value = 'easy'
    elif 3 <= difficulty_accumulator < 6:
        difficulty_value = 'medium'
    else:
        difficulty_value = 'hard'

    write_json('config.json', key='difficulty', value=difficulty_value)
    print(difficulty_value, difficulty_accumulator)


# Tkinter GUI Setup

root = Tk()
root.title("PyQuiz")
root.geometry("300x400")
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)


frame_welcome = Frame(root)
frame_settings = Frame(root)
frame_game = Frame(root)
frame_stats = Frame(root)

frames = (frame_welcome, frame_settings, frame_game, frame_stats)

for frame in frames:
    frame.grid(row=0, column=0, sticky='news')

raise_frame(frame_welcome)


# Welcome Frame

frame_welcome_title = Frame(frame_welcome, pady=30)
frame_welcome_title.pack()
label_welcome_title = Label(frame_welcome_title, text='PyQuiz', font=("Helvetica", 48))
label_welcome_title.pack()
label_version = Label(frame_welcome_title, text='v0.1', font=("Helvetica", 18))
label_version.pack()

frame_welcome_buttons = Frame(frame_welcome, padx=10, pady=30)
frame_welcome_buttons.pack()
button_new_game = Button(frame_welcome_buttons,
                         text='New Game',
                         command=lambda: [raise_frame(frame_game),
                                          api_request_token(),
                                          next_question(),
                                          update_scoreboard()
                                          ]
                         )
button_new_game.grid(row=0, column=0, columnspan=2, pady=10, sticky='news')
button_stats = Button(frame_welcome_buttons, text='Stats', command=lambda: raise_frame(frame_stats))
button_stats.grid(row=1, column=0)
button_settings = Button(frame_welcome_buttons, text='Settings', command=lambda: raise_frame(frame_settings))
button_settings.grid(row=1, column=1)


# Stats Frame

frame_stats_title = Frame(frame_stats, pady=30)
frame_stats_title.pack()
label_stats_title = Label(frame_stats_title, text='Stats', font=("Helvetica", 24))
label_stats_title.pack()

frame_stats_widgets = Frame(frame_stats)
frame_stats_widgets.pack()
button_stats_reset = Button(frame_stats_widgets, text='Reset Stats', command=reset_stats)
button_stats_reset.pack()
button_stats_back = Button(frame_stats_widgets, text='Back', command=lambda: raise_frame(frame_welcome))
button_stats_back.pack()


# Settings Frame

frame_settings_title = Frame(frame_settings, pady=30)
frame_settings_title.pack()
label_settings_title = Label(frame_settings_title, text='Settings', font=("Helvetica", 24))
label_settings_title.pack()

frame_settings_widgets = Frame(frame_settings)
frame_settings_widgets.pack()

difficulty = [
    "Easy",
    "Medium",
    "Hard",
    "Auto"
]
selected_difficulty = StringVar()
selected_difficulty.set("Easy")

label_difficulty = Label(frame_settings_widgets, text='Difficulty:')
label_difficulty.grid(row=0, column=0, pady=10)
dropdown_difficulty = OptionMenu(frame_settings_widgets, selected_difficulty, *difficulty)
dropdown_difficulty.config(width=4)
dropdown_difficulty.grid(row=0, column=2, pady=10)

button_settings_back = Button(frame_settings_widgets,
                              text='Back',
                              command=lambda: [raise_frame(frame_welcome), write_settings()]
                              )
button_settings_back.grid(row=1, column=1)


# Game Frame

frame_game_title = Frame(frame_game, pady=30)
frame_game_title.pack()
label_game_title = Label(frame_game_title, text="Endless Mode", font=("Helvetica", 24))
label_game_title.pack()

frame_game_question = Frame(frame_game, width=300, height=60)
frame_game_question.pack_propagate(False)
frame_game_question.pack()
label_game_question = Label(frame_game_question, text='Question goes here', wraplength=250, justify=CENTER)
label_game_question.pack()

frame_game_buttons = Frame(frame_game, pady=10)
frame_game_buttons.pack()
button_true = Button(frame_game_buttons, text='True', command=answer_true)
button_true.grid(row=0, column=0, sticky='news')
button_false = Button(frame_game_buttons, text='False', command=answer_false)
button_false.grid(row=0, column=2, sticky='news')
button_next_question = Button(frame_game_buttons, text='Next Question', command=next_question)
button_next_question.grid(row=1, column=0, columnspan=3, sticky='news', pady=10)
button_game_exit = Button(frame_game_buttons, text='Exit', command=lambda: raise_frame(frame_welcome))
button_game_exit.grid(row=2, column=1, pady=10)

frame_game_score = Frame(frame_game)
frame_game_score.pack()
label_score = Label(frame_game_score, text='')
label_score.pack()

# Loop
root.mainloop()

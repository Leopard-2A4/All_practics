import datetime
import random
from datetime import timedelta

from flask import Flask

from Random_choise import *

app = Flask(__name__)

calls = 0


@app.route('/')  # ← ДОБАВЬ ЭТО
def index():
    return 'Добро пожаловать в Random API! Доступные роуты:<br>' \
           '- /hello_world<br>' \
           '- /cars<br>' \
           '- /cats<br>' \
           '- /get_time/now<br>' \
           '- /get_time/future<br>' \
           '- /get_random_word<br>' \
           '- /counter'


@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'


@app.route('/cars')
def cars_func():
    return ', '.join(cars)


@app.route('/cats')
def cat_func():
    return random.choice(cats_list)


@app.route('/get_time/now')
def now_time_func():
    current_time = datetime.datetime.now().time()
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def future_time_func():
    now = datetime.datetime.now()
    current_time_after_hour = now + timedelta(hours=1)
    return f'Точное время через час будет {current_time_after_hour}'


@app.route('/get_random_word')
def random_word_func():
    return random_word()


@app.route('/counter')
def counter_func():
    global calls
    calls += 1
    return f'Вызовов: {calls}'


if __name__ == '__main__':
    app.run(debug=True)

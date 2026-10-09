"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

import datetime

from flask import Flask

app = Flask(__name__)


@app.route('/hello-world/<username>')
def hello_world(username):
    days = [
        "понедельника",
        "вторника",
        "среды",
        "четверга",
        "пятницы",
        "субботы",
        "воскресенья",
    ]
    now_day = days[datetime.datetime.now().weekday()]
    now_day_v2 = {days[0], days[1], days[3], days[-1]}
    if now_day in now_day_v2:
        return f'Привет, {username}. Хорошего {now_day}!'
    else:
        return f'Привет, {username}. Хорошей {now_day}!'


if __name__ == '__main__':
    app.run(debug=True)

"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""
from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    storage[date] = storage.get(date, 0) + number
    return f"Добавлено {number} руб. за {date}"


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    year_str = str(year)
    total = 0
    for date, amount in storage.items():
        if date.startswith(year_str):
            total += amount
    return str(total)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    year_str = str(year)
    month_str = f"{month:02d}"
    total = 0
    for date, amount in storage.items():
        if date.startswith(year_str + month_str):
            total += amount
    return str(total)


if __name__ == "__main__":
    app.run(debug=True)

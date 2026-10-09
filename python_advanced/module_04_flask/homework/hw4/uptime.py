"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    try:
        result = subprocess.run(['uptime'], capture_output=True, text=True, check=True)
        uptime_value = result.stdout.strip()
        return f"Current uptime is {uptime_value}"
    except subprocess.CalledProcessError:
        return "Current uptime is: error executing uptime command"
    except Exception:
        return "Current uptime is: unknown error"


if __name__ == '__main__':
    app.run(debug=True)

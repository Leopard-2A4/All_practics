"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args = request.args.getlist('arg')

    if not args:
        return "No arguments provided. Usage: /ps?arg=a&arg=u&arg=x"

    try:
        result = subprocess.run(['ps'] + args,
                                capture_output=True,
                                text=True,
                                check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing ps: {e}\nStderr: {e.stderr}"
    except Exception as e:
        return f"Unknown error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)

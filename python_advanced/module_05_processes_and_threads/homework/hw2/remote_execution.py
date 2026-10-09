"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
from flask import Flask, request, jsonify
import subprocess
import sys
import signal

app = Flask(__name__)


def run_python_code_in_subprocess(code: str, timeout: int):
    code_file = '/tmp/temp_code.py'
    try:
        with open(code_file, 'w') as f:
            f.write(code)

        process = subprocess.Popen(
            [sys.executable, code_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=lambda: signal.signal(signal.SIGTERM, signal.SIG_DFL),
            text=True
        )

        stdout, stderr = process.communicate(timeout=timeout)

        if process.returncode == 0:
            return stdout or "Код выполнен успешно"
        else:
            return stderr or f"Ошибка (код: {process.returncode})"

    except subprocess.TimeoutExpired:
        process.kill()
        return f"Время выполнения истекло ({timeout} сек)"
    except Exception as e:
        return f"Ошибка: {str(e)}"
    finally:
        try:
            import os
            os.remove(code_file)
        except:
            pass


@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({"error": "Отсутствует поле 'code'"}), 400

    code = data['code']
    timeout = data.get('timeout', 5)

    if not isinstance(timeout, int) or timeout > 30 or timeout <= 0:
        return jsonify({"error": "Тайм-аут должен быть от 1 до 30 секунд"}), 400

    result = run_python_code_in_subprocess(code, timeout)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)


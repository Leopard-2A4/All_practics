"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
from typing import List
import subprocess
import sys
from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError("Port must be integer")

    pids: List[int] = []

    try:
        # lsof -i :5000 -t возвращает только PID (один на строку)
        result = subprocess.run(
            ['lsof', '-i', f':{port}', '-t'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            pids = [int(pid.strip()) for pid in result.stdout.strip().split('\n') if pid.strip()]

    except Exception as e:
        print(f"Ошибка получения PID для порта {port}: {e}", file=sys.stderr)

    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)

    for pid in pids:
        try:
            print(f"Завершаем процесс PID {pid} на порту {port}")
            subprocess.run(['kill', '-9', str(pid)], check=True)
        except subprocess.CalledProcessError:
            print(f"Не удалось завершить процесс {pid}", file=sys.stderr)


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port, debug=True)


if __name__ == '__main__':
    run(5000)

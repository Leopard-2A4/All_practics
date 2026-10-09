"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size():
    """
    Вычисляет средний размер файлов из вывода ls -l через stdin.
    """
    total_size = 0
    file_count = 0

    lines = sys.stdin.readlines()[1:]

    for line in lines:
        parts = line.split()
        if len(parts) >= 5:
            try:
                size = int(parts[4])
                total_size += size
                file_count += 1
            except ValueError:
                continue

    if file_count == 0:
        return "0 Б (нет файлов)"

    avg_size = total_size / file_count

    units = ['Б', 'Кб', 'Мб', 'Гб']
    size = avg_size
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.1f} {units[unit_index]}"


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)

# TODO здесь писать код
import os
from typing import Generator

def count_python_lines(directory: str) -> Generator[int, None, None]:
    """
    Генератор, который для каждого Python-файла в указанной директории
    считает количество непустых строк без комментариев и возвращает это число.
    :param directory: Путь к директории для поиска файлов.
    :yield: Количество строк в очередном Python-файле.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                line_count = 0
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            stripped = line.strip()
                            if stripped and not stripped.startswith('#'):
                                line_count += 1
                except (IOError, UnicodeDecodeError):
                    pass
                yield line_count


directory = input("Введите путь к директории: ")
for count in count_python_lines(directory):
    print(f"Количество строк: {count}")
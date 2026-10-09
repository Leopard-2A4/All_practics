# TODO здесь писать код
import os

# При помощи модуля os (и функции join) сформируйте пути до файлов work_logs.txt и output.txt в папке data
# (output.txt может не быть в папке data, но его нужно будет там создать, при помощи кода)
data_dir = os.path.join('data')
input_file_path = os.path.join(data_dir, 'work_logs.txt')
output_file_path = os.path.join(data_dir, 'output.txt')
def error_log_generator(log_file_path):
    if not os.path.exists(input_file_path):
        print(f"Ошибка: Файл {input_file_path} не существует.")
        print("Создайте папку 'data' и поместите туда файл work_logs.txt")
        return
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if 'ERROR' in line:
                    yield line
    except FileNotFoundError:
        print(f"Ошибка: Файл {log_file_path} не найден.")
    except PermissionError:
        print(f"Ошибка: Нет доступа к файлу {log_file_path}.")

# Документация по join https://docs-python.ru/standart-library/modul-os-path-python/funktsija-join-modulja-os-path/

# Не забудьте проверить наличие файлов перед тем как начать работу с ними
# https://docs-python.ru/standart-library/modul-os-path-python/funktsija-exists-modulja-os-path/

with open(output_file_path, 'w') as output:
    for error_line in error_log_generator(input_file_path):
        output.write(error_line)
print("Файл успешно обработан.")
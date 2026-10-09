# TODO здесь писать код
import os

def get_directory_info(path):
    total_size = 0
    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(path):
        dir_count += len(dirs)
        file_count += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)

    return total_size, file_count, dir_count

path = input('Введите путь до каталога: ')
size, files, dirs = get_directory_info(path)
size_kb = size / 1024

print(path)
print('Размер каталога (в Кбайтах):',size_kb)
print('Количество подкаталогов:', dirs)
print('Количество файлов:',files)
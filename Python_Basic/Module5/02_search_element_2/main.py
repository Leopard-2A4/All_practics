# TODO здесь писать код
def find_key_value(data, target_key, max_depth=None, current_depth=1):
    current_depth += 1
    if target_key in data:
        return data[target_key]
    for value in data.values():
        if isinstance(value, dict):
            result = find_key_value(value, target_key, max_depth, current_depth)
            if result is not None:
               if max_depth is not None and current_depth != max_depth:
                     result = None
                     return result
               return result
site = {
    'html': {
        'head': {
            'title': 'Мой сайт'
        },
        'body': {
            'h2': 'Здесь будет мой заголовок',
            'div': 'Тут, наверное, какой-то блок',
            'p': 'А вот здесь новый абзац'
        }
    }
}

key_name = input('Введите искомый ключ: ')
depth_input = input('Хотите ввести максимальную глубину? Y/N: ').lower()
if depth_input == 'y':
    max_depth = int(input('Введите максимальную глубину: '))
    result = find_key_value(site, key_name, max_depth)
else:
    result = find_key_value(site, key_name)

print('Значение ключа:', result)
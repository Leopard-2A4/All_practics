# TODO здесь писать код
file = open('people.txt', 'r', encoding='utf-8')
errors = open('errors.log', 'w', encoding='utf-8')
full_len = 0
num_of_line = 0

def exp_or_not(line):
    if len(line) < 3:
       return ValueError

for line in file:
    try:
       num_of_line += 1
       line = line.strip()
       full_len += len(line)
       if len(line) < 3:
          errors.write(f'Ошибка: менее трёх символов в строке {num_of_line}')
          raise ValueError
    except ValueError:
        print((f'Ошибка: менее трёх символов в строке {num_of_line}'))
print('Общее количество символов: ',full_len)

file.close()
errors.close()
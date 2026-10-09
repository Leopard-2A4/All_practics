# TODO здесь писать код
number = int(input('Введите длину списка: '))
num_list = [(i % 5 if i % 2 != 0 else 1)for i in range(number)]
print('Результат: ',num_list)
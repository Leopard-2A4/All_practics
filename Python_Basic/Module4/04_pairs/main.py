# TODO здесь писать код
import random

num_list = [random.randint(1, 10) for i in range(10)]
print('Оригинальный список:', num_list)

first_list = num_list[0:-1:2]  # Чётные индексы
second_list = num_list[1:-1:2]  # Нечётные индексы

# Создаём список пар через zip и преобразуем в список
answer = list(zip(first_list, second_list))
print('Список пар:', answer)
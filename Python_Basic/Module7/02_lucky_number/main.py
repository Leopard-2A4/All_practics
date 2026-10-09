# TODO здесь писать код
import random

result = open('out_file.txt', 'w', encoding='utf-8')
sum_of_num = 0

while sum_of_num < 777:
    lose_or_win = random.randint(1, 13)
    if lose_or_win == 13:
        result.write('Вас постигла неудача!')
        break
    else:
        try:
            number = int(input('Введите число: '))
            result.write(str(number) + '\n')
            sum_of_num += number
        except ValueError:
            print('Ошибка ввода, попробуйте снова.')
else:
    result.write('Вы успешно выполнили условие для выхода из порочного цикла!')
result.close()
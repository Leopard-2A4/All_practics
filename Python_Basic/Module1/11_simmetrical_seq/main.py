# TODO здесь писать код
numbers = int(input('Введите количество чисел: '))
num_list = []
first_list = []
second_list = []

for i in range(numbers):
    num_list.append(int(input('Число : ')))
first_list.extend(num_list)

for j in range(len(num_list)):
    half = len(num_list) // 2
    if len(num_list) % 2 != 0:
        if num_list[:half] == num_list[half + 1:]:
            break
    else:
        if num_list[:half] == num_list[:half-1:-1]:
            break
    num_list.append(num_list[j])
    second_list.append(num_list[j])

print('\nПоследовательность: ',first_list)
print('Нужно приписать чисел:',len(second_list))
print('Сами числа: ',second_list)
# TODO здесь писать код
change = 1
a_list = list(input('Введите строку: '))

for i in range(len(a_list)):
    new_list = a_list[-change:] + a_list[:-change]
    new_list_full = ''.join(new_list)
    new_list_rev_full = ''.join(reversed(new_list))
    if new_list_full == new_list_rev_full:
       print('Можно сделать палиндромом')
       break
    else:
       change += 1
else:
    print('Нельзя сделать палиндромом')

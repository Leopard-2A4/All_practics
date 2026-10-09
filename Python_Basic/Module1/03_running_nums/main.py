# TODO здесь писать код
change = int(input('Сдвиг: '))
a_list = [1,2,3,4,5]

print('Изначальный список: ',a_list)

new_list = a_list[-change:] + a_list[:-change]
print('Сдвинутый список: ',new_list)
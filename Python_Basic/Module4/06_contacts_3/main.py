# TODO здесь писать код
def update_dict(telephon):
    name = input('Введите имя и фамилию нового контакта (через пробел): ').title().split(' ')
    name = tuple(name)
    number = int(input('Введите номер телефона: '))
    if name in telephon:
       print('Такой человек уже есть в контактах.')
    else:
      telephon[name] = number
    print('Текущий словарь контактов: ',telephon)

def find_user(telephon):
    who_need_to_find = input('Введите фамилию для поиска: ')
    for name, number in telephon.items():
        if who_need_to_find in name:
            print(f'{name}: {number}')
    else:
        print('Такого пользователя нет в словаре')

print('Введите номер действия: \n1.Добавить контакт.\n2.Найти человека.')

telephon_dict = dict()

while True:

   choose = input()
   if choose == '1':
      update_dict(telephon_dict)
   elif choose == '2':
       find_user(telephon_dict)
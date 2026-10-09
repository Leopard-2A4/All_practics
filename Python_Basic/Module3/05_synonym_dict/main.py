# TODO здесь писать код
syn_dict = dict()

quantity = int(input('Введите количество пар слов: '))
for i in range(quantity):
    print('Пара под номером', i+1, ': ', end='')
    duo = input().split(' — ')
    syn_dict[duo[0].lower()] = duo[1]
    syn_dict[duo[1].lower()] = duo[0]

while True:
    word = input('Введите слово: ').lower()
    if word in syn_dict:
        print('Синоним:', syn_dict[word])
        break
    else:
        print('Такого слова в словаре нет.')
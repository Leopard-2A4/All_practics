# TODO здесь писать код
text_list = list(input('Введите текст: '))
vowels = ['а', 'о', 'у', 'ы', 'и', 'ё', 'е', 'ю', 'я', 'э']

vowel_list = [sym for sym in text_list if sym in vowels]

print('Список гласных букв: ',vowel_list)
print('Длина списка: ',len(vowel_list))
# TODO здесь писать код
text = input('Введите слово: ')
reverse_text = ''

for sym in text:
    reverse_text = sym + reverse_text

if text == reverse_text:
    print('Слово является палиндромом')
else:
    print('Слово не является палиндромом')
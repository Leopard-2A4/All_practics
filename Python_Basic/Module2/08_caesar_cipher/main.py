# TODO здесь писать код
alphabet = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
text = list(input('Введите сообщение: '))
shift = int(input('Введите сдвиг: '))
result = []
for i in text:
    if i in alphabet:
       elem = alphabet.index(i)
       elem = (elem + shift) % len(alphabet)
       result.append(alphabet[elem])
    else:
       result.append(i)

print('Зашифрованное сообщение: ',''.join(result))
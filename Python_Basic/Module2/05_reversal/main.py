# TODO здесь писать код
text = list(input('Введите строку: '))

while text[0] != text[-1]:
    text.remove(text[-1])

answer = ''.join(text[-2:0:-1])

print('Развёрнутая последовательность между первым и последним h: ',answer)
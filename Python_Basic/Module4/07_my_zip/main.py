# TODO здесь писать код
text = list(input('Строка: '))
sym_tuple = (10, 20, 30, 40)

answer = [(text[index], value) for index, value in enumerate(sym_tuple)]

print(*answer, sep='\n')
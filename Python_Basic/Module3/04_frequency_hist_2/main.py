# TODO здесь писать код
def update_dict(words,dict_of_sym):
    for sym in words:
        dict_of_sym[sym] = words.count(sym)

def print_details(dict_of_sym):
    print('Оригинальный словарь частот:')
    for part in sym_dict:
        print(part, ':', dict_of_sym[part])

def answer(dict_of_sym,max_value):
    print('Инвертированный словарь частот:')
    for i in range(1,max_value+1):
        words = []
        words = [sym for sym in dict_of_sym if dict_of_sym[sym] == i]
        print(i,':',words)

text = list(input('Введите текст: '))
sym_dict = dict()
update_dict(text,sym_dict)

print_details(sym_dict)

maximum = max(sym_dict.values())

answer(sym_dict,maximum)
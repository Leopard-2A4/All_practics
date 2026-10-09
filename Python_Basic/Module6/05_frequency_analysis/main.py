# TODO здесь писать код
import re

def count_of_sym(english,sym):
    sym_count = round(english.count(sym)/len(english),3)
    return sym_count

def print_dict(final_dict):
    print('Содержимое файла analysis.txt:')
    sorted_data = dict(sorted(final_dict.items(), key=lambda x: (-x[1], x[0])))
    for key, value in sorted_data.items():
        print(key, '->', value)

def is_it_text(text):
    answer = dict()
    text = text.lower()
    english_letters = re.findall(r'[a-z]', text)
    for sym in english_letters:
        answer[sym] = count_of_sym(english_letters, sym)
    print_dict(answer)

file = open('text.txt', 'r')
text = file.read()
print('Содержимое файла text.txt:\n',text)
is_it_text(text)
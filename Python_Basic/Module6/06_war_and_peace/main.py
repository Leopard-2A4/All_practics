# TODO здесь писать код
import zipfile
from collections import Counter

with zipfile.ZipFile('voina-i-mir.zip', mode='r') as archive:
    text = archive.read('voyna-i-mir.txt').decode(encoding="utf-8")

alphabet = set(chr(i) for i in list(range(ord('a'), ord('z')+1)) +
              list(range(ord('A'), ord('Z')+1)) +
              list(range(ord('А'), ord('Я')+1)) +
              list(range(ord('а'), ord('я')+1)))

symbol = Counter(text)

filtered_symbol = {k: v for k, v in symbol.items() if k in alphabet}
sorted_symbol = sorted(filtered_symbol.items(), key=lambda item: (-item[1], item[0]))

with open('voyna-i-mir-analysis.txt', 'w', encoding='utf-8') as new_file:
    for k, v in sorted_symbol:
        new_file.write(f'Буква "{k}" встречается {v} раз\n')
import os
import random
import re

cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
with open(BOOK_FILE, encoding='utf-8') as book:
    words = re.findall(r'\w+', book.read().lower())


def random_word():
    return random.choice(words)

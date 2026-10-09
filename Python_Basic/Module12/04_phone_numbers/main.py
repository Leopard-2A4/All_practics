# TODO здесь писать код
import re

num_list = ['9999999999', '999999-999', '99999x9999']

for num in num_list:
    pattern = re.compile(r'\b[8-9]\d{9}\b')
    result = re.findall(pattern, num)
    if result:
       print('всё в порядке')
    else:
       print('не подходит')
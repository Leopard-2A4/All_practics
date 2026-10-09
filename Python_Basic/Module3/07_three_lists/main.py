# TODO здесь писать код
array_1 = [1, 5, 10, 20, 40, 80, 100]
array_2 = [6, 7, 20, 80, 100]
array_3 = [3, 4, 15, 20, 30, 70, 80, 120]

array_1 = set(array_1)
array_2 = set(array_2)
array_3 = set(array_3)

print('Элементы которые есть во всех списках: ',array_1.intersection(array_2, array_3))
print('Элементы которые есть только в первом списке: ',array_1.difference(array_2, array_3))
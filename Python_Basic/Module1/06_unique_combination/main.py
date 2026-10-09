# TODO здесь писать код
# Пример использования:
list1 = [1, 3, 5, 7, 9]
list2 = [2, 4, 5, 6, 8, 10]
merged = sorted(list((list1 + list2)))
for item in merged:
    if merged.count(item) > 1:
        merged.remove(item)
print(merged)
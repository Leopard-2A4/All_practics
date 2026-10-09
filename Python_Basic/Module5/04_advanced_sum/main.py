# TODO здесь писать код
def answer(sum_list, result):
    for item in sum_list:
        if isinstance(item, (list, tuple, set)):
            answer(item, result)
        elif isinstance(item, int):
            result.append(item)

sum_list = [[1, 2, [3]], [1], 3]
result = []
answer(sum_list, result)
print('Сумма:', sum(result))
nice_list = [1, 2, [3, 4], [[5, 6, 7], [8, 9, 10]],
             [[11, 12, 13], [14, 15], [16, 17, 18]]]

# TODO здесь писать код
def answer(nice_list,result):
    for item in nice_list:
        if isinstance(item, list):
           answer(item,result)
        elif isinstance(item, int):
           result.append(item)
    return result

result = []
answer(nice_list,result)
print(result)
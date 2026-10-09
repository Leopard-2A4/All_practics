# TODO здесь писать код
need_sort = [1,4,-3,0,10]
print('Изначальный список: ', need_sort)

for _ in range(len(need_sort)):
    for symbol in range(len(need_sort) - 1):
        if need_sort[symbol] > need_sort[symbol+1]:
            need_sort[symbol+1], need_sort[symbol] = need_sort[symbol], need_sort[symbol+1]

print('Отсортированный список: ',need_sort)
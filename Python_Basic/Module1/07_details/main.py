shop = [
        ['каретка', 1200],
        ['шатун', 1000],
        ['седло', 300],
        ['педаль', 100],
        ['седло', 1500],
        ['рама', 12000],
        ['обод', 2000],
        ['шатун', 200],
        ['седло', 2700]
]

# TODO здесь писать код
def answer (cost,count):
    for i in shop:
        if detail == i[0]:
            count = count + 1
            cost = cost + i[1]
    print('Количество деталей: ', count)
    print('Общая стоимость: ', cost)

detail = input('Название детали: ')
count_det = 0
price = 0

answer(price,count_det)
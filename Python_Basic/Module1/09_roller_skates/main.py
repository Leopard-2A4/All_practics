# TODO здесь писать код
def roller_skates(count):
    for i in range(count):
        print('Размер пары',i + 1 ,': ',end='')
        roller.append(int(input()))

def client(count):
    for i in range(count):
        print('Размер ноги человека ',i + 1, ': ',end='')
        humans.append(int(input()))

def answer(roll,people):
    who_can_buy_max = 0
    for one_roller in roll:
        for one_man in people:
           if one_man == one_roller:
              who_can_buy = people.count(one_man)
              if who_can_buy_max < who_can_buy:
                 who_can_buy_max = who_can_buy
    print('Наибольшее количество людей, которые могут взять ролики: ',who_can_buy_max)

count_of_roller = int(input('Количество роликов: '))
roller = []
roller_skates(count_of_roller)

count_of_humans = int(input('\nКоличество людей: '))
humans = []
client(count_of_humans)

answer(roller,humans)
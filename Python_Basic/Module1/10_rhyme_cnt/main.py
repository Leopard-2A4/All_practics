# TODO здесь писать код
count = int(input('Количество человек: '))
rhyme = int(input('Какое число в считалке? '))
print('Значит, выбывает каждый', rhyme, 'человек.')
people = list(range(1, count +1))
extra = 0

for i in range(count-1):
   print('\nТекущий круг людей', people)
   start = extra % len(people)
   extra = (start + rhyme - 1) % len(people)
   print('Начало счёта с номера', people[start])
   print('Выбывает человек под номером', people[extra])
   people.remove(people[extra])


print('\nОстался человек под номером', people[0])
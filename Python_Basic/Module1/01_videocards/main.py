# TODO здесь писать код
count_nvidia = int(input('Количество видеокарт: '))
list_of_nvidia = []

for n in range(count_nvidia):
    print('Видеокарта', n + 1,': ', end='')
    nvidia = int(input())
    list_of_nvidia.append(nvidia)
maximum = max(list(list_of_nvidia))
count_of_max = list_of_nvidia.count(maximum)

print('Старый список видеокарт: ',list_of_nvidia)

for _ in range(count_of_max):
    list_of_nvidia.remove(maximum)

print('Новый список видеокарт: ',list_of_nvidia)


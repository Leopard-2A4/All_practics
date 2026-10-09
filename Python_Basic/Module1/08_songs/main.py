violator_songs = [
    ['World in My Eyes', 4.86],
    ['Sweetest Perfection', 4.43],
    ['Personal Jesus', 4.56],
    ['Halo', 4.9],
    ['Waiting for the Night', 6.07],
    ['Enjoy the Silence', 4.20],
    ['Policy of Truth', 4.76],
    ['Blue Dress', 4.29],
    ['Clean', 5.83]
]

# TODO здесь писать код
count_of_songs = int(input('Сколько песен выбрать? '))
summ = 0
for count in range(count_of_songs):
    print('Название',count+1,'-й песни: ',end='')
    song = input()
    for part in violator_songs:
        if song == part[0]:
           summ += part[1]
print('Общее время звучания песен —',summ,'минуты')
violator_songs = {
    'World in My Eyes': 4.86,
    'Sweetest Perfection': 4.43,
    'Personal Jesus': 4.56,
    'Halo': 4.9,
    'Waiting for the Night': 6.07,
    'Enjoy the Silence': 4.20,
    'Policy of Truth': 4.76,
    'Blue Dress': 4.29,
    'Clean': 5.83
}

# TODO здесь писать код

count =int(input('Сколько песен выбрать? '))
time = 0

for i in range(1,count+1):

    print('Название',i,'-ой песни: ',end ='')
    song = input()

    if song in violator_songs:
       time += violator_songs[song]
    else:
       print('Ошибка подобной песни нет.')

print('Общее время звучания песен: ',time)
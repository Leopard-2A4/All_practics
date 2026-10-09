films = ['Крепкий орешек', 'Назад в будущее', 'Таксист',
         'Леон', 'Богемская рапсодия', 'Город грехов',
         'Мементо', 'Отступники', 'Деревня']
# TODO здесь писать код
def film_exist(new_movie, list_of_movie):
    for i_movie in list_of_movie:
        if i_movie == new_movie:
            return True
    return False

my_films = []
count_of_films = int(input('Сколько фильмов хотите добавить? '))
for _ in range(count_of_films):
    new_film = input('Введите название фильма: ')
    if film_exist(new_film, films):
       my_films.append(new_film)
    else:
        print('Ошибка: фильма',new_film,'у нас нет :(')
print('Ваш список любимых фильмов: ',end='')
for film in my_films:
    print(film,end=' ')
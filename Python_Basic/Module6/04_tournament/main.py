# TODO здесь писать код
def winners(first_list, second_list):
    for line in first_list:
        parts = line.split()
        if len(parts) >= 3:
            try:
                score = int(parts[2])
                if score > 80:
                    second_list.write(line + '\n')
            except ValueError:
                continue  # Пропускаем некорректные строки

first_list = open('first_tour.txt', 'r').read().splitlines()
second_list = open('second_tour.txt', 'w')

winners(first_list, second_list)
second_list.close()
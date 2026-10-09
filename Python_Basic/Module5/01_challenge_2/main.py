# TODO здесь писать код
def print_num(num,num_start):
    if num == num_start:
       return num
    num_start += 1
    print(num_start)
    return print_num(num,num_start)

number = int(input('Введите число: '))
start = 0
print_num(number,start)
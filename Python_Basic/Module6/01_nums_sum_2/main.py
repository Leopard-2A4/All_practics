# TODO здесь писать код
def find_sum(num_file):
    summa = 0
    for sym in num_file:
        if sym.isdigit():
           summa += int(sym)
    return summa

file = open('numbers.txt','r').read().split()
print(find_sum(file))
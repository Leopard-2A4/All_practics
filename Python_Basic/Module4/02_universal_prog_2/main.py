# TODO здесь писать код
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def crypto(iterable):
    return [item for index, item in enumerate(iterable) if is_prime(index)]

print(crypto([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
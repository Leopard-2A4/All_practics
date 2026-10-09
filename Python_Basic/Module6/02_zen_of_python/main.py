# TODO здесь писать код
def zen_reverse(zen_pithon):
    reverse = '\n'.join(zen_pithon[::-1])
    return reverse

file = open('zen.txt', 'r').read().splitlines()
print(zen_reverse(file))
# TODO здесь писать код
def tpl_sort(corteg):
    corteg_lst = list(corteg)
    for num in corteg_lst:
        if isinstance(num, float):
            print(corteg)
            return
    corteg_lst.sort()
    print(tuple(corteg_lst))

tpl = (6, 3, -1, 8, 4, 10, -5)
tpl_sort(tpl)
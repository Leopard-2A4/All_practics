# TODO здесь писать код
import os
from collections.abc import Iterable


def gen_files_path(path: str) -> Iterable[str]:
    """
    Функция - генератор. Рекурсивно проходит по всем каталогам,
    указанной директории, находит заданный каталог и генерирует
    пути файлов.
    @param path:
    @return:
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

root_variant_index_0 = os.path.abspath(os.sep)
current_variant_index_1 = os.path.join(os.getcwd())
need_variant_index_2 = os.path.join('..', 'Python_Basic')
need_variant_index_3 = os.path.join('..', 'Python_Basic', 'Module10')
your_variant = (root_variant_index_0, current_variant_index_1, need_variant_index_2, need_variant_index_3)

result = gen_files_path(
    path=your_variant[int(input('Введите индекс варианта '
    '(1-корень, 2-текущая директория, 3-Python_Basic, 4-Module10): '))-1])
for name in result:
    print(name)
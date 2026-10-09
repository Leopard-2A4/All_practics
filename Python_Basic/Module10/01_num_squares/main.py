# TODO здесь писать код
from typing import Iterator, Generator, List

class SquareIterator:
    """
    Итератор для генерации квадратов чисел от 1 до N.
    """

    def __init__(self, n: int) -> None:
        """
        Инициализирует итератор.
        :param n: Верхняя граница последовательности.
        """
        self.n: int = n
        self.current: int = 1

    def __iter__(self) -> 'SquareIterator':
        """
        Возвращает итератор.
        :return: Сам объект итератора.
        """
        return self

    def __next__(self) -> int:
        """
        Возвращает следующий квадрат числа.
        :return: Квадрат текущего числа.
        :raises StopIteration: Когда достигнута граница N.
        """
        if self.current > self.n:
            raise StopIteration
        square: int = self.current ** 2
        self.current += 1
        return square


def square_generator(n: int) -> Generator[int, None, None]:
    """
    Функция-генератор для генерации квадратов чисел от 1 до N.
    :param n: Верхняя граница последовательности.
    :yield: Квадрат числа от 1 до N.
    """
    for i in range(1, n + 1):
        yield i ** 2


def get_squares_list(n: int) -> List[int]:
    """
    Генерирует список квадратов чисел от 1 до N с помощью генераторного выражения.
    :param n: Верхняя граница последовательности.
    :return: Список квадратов чисел.
    """
    return list(i ** 2 for i in range(1, n + 1))


# Пример использования
def main() -> None:
    """
    Демонстрация всех трёх способов генерации квадратов.
    """
    n: int = int(input("Введите число N: "))

    print(f"\nКласс-итератор:")
    squares_iter: Iterator[int] = SquareIterator(n)
    for square in squares_iter:
        print(square, end=" ")
    print()

    print(f"\nФункция-генератор:")
    squares_gen: Generator[int, None, None] = square_generator(n)
    for square in squares_gen:
        print(square, end=" ")
    print()

    print(f"\nГенераторное выражение:")
    squares_list: List[int] = get_squares_list(n)
    print(squares_list)

main()
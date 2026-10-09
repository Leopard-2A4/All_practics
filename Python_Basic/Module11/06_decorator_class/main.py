# TODO здесь писать код
import time
import functools
from typing import Any, Callable


class LoggerDecorator:
    """
    Декоратор-класс для логирования аргументов, результатов и времени выполнения функции.
    """
    def __init__(self, func: Callable) -> None:
        """
        Инициализация декоратора.
        Args:
            func: Декорируемая функция.
        """
        functools.wraps(func)(self)
        self.func = func
        self.func_name = func.__name__

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Вызов декорированной функции с логированием.
        Args:
            *args: Позиционные аргументы функции.
            **kwargs: Именованные аргументы функции.
        Returns:
            Результат выполнения функции.
        """
        print(f"Вызов функции {self.func_name}")
        print(f"Аргументы: {args}, {kwargs}")

        start_time = time.time()

        try:
            result = self.func(*args, **kwargs)
            execution_time = time.time() - start_time

            print(f"Результат: {result}")
            print(f"Время выполнения: {execution_time} секунд")
            return result

        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Ошибка: {e}")
            print(f"Время до ошибки: {execution_time} секунд")
            raise

@LoggerDecorator
def complex_algorithm(arg1, arg2):
    # Здесь выполняется сложный алгоритм
    result = 0
    for i in range(arg1):
        for j in range(arg2):
            with open('test.txt', 'w', encoding='utf8') as file:
                file.write(str(i + j))
                result += i + j
    return result


# Пример вызова функции с применением декоратора
result = complex_algorithm(10, 50)
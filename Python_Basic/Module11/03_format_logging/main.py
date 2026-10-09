# TODO здесь писать код
import functools
import time
from datetime import datetime
from typing import Callable, Any, TypeVar, Type

T = TypeVar('T', bound='object')


def log_methods(date_format: str) -> Callable[[Type[T]], Type[T]]:
    """
    Декоратор класса для логирования всех методов (кроме магических).

    Args:
        date_format: Формат даты и времени для логирования (strftime).

    Returns:
        Декорированный класс с логированием методов.
    """

    def decorator(cls: Type[T]) -> Type[T]:
        # Получаем все методы класса (исключая магические)
        methods = {name: method for name, method in cls.__dict__.items()
                   if not name.startswith('__') and callable(method)}

        # Создаем новый класс с обёрнутыми методами
        class LoggedClass(cls):
            pass

        # Оборачиваем каждый метод
        for name, original_method in methods.items():
            @functools.wraps(original_method)
            def make_wrapper(method, method_name=name):
                def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
                    # Логирование начала
                    start_time = time.time()
                    dt_start = datetime.now().strftime(date_format)
                    print(f"Запускается '{type(self).__name__}.{method_name}'. "
                          f"Дата и время запуска: {dt_start}.")

                    try:
                        # Вызов оригинального метода
                        result = method(self, *args, **kwargs)
                        return result
                    finally:
                        # Логирование завершения (всегда выполняется)
                        end_time = time.time()
                        execution_time = end_time - start_time
                        print(f"Завершение '{type(self).__name__}.{method_name}', "
                              f"время работы = {execution_time:.3f} s.")

                return wrapper

            # Присваиваем обёрнутый метод
            setattr(LoggedClass, name, make_wrapper(original_method))

        return LoggedClass

    return decorator

@log_methods("b d Y — H:M:S")
class A:
    def test_sum_1(self) -> int:
        print('test sum 1')
        number = 100
        result = 0
        for _ in range(number + 1):
            result += sum([i_num ** 2 for i_num in range(10000)])

        return result

@log_methods("b d Y - H:M:S")
class B(A):
    def test_sum_1(self):
        super().test_sum_1()
        print("Наследник test sum 1")


    def test_sum_2(self):
        print("test sum 2")
        number = 200
        result = 0
        for _ in range(number + 1):
            result += sum([i_num ** 2 for i_num in range(10000)])

        return result

my_obj = B()
my_obj.test_sum_1()
my_obj.test_sum_2()
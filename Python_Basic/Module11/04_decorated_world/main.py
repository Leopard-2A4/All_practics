# TODO здесь писать код
from functools import wraps
from typing import Callable, Any, TypeVar



def decorator_with_args_for_any_decorator(decorator_func: Callable) -> Callable:
    """
    Декоратор для декораторов, позволяющий принимать произвольные аргументы.
    Args:
        decorator_func: Декоратор, который нужно сделать параметризованным.
    Returns:
        Функция, которая принимает аргументы для декоратора и возвращает декоратор.
    """

    @wraps(decorator_func)
    def decorator_maker(*args: Any, **kwargs: Any) -> Callable:
        """
        Функция, принимающая аргументы для оригинального декоратора.
        Args:
            *args: Позиционные аргументы для декоратора.
            **kwargs: Именованные аргументы для декоратора.
        Returns:
            Декоратор, готовый к применению к функции.
        """

        def decorator(func):
            """
            Фактический декоратор, применяющий оригинальный декоратор с аргументами.
            Args:
                func: Декорируемая функция.
            Returns:
                Обёрнутая функция.
            """
            return decorator_func(func, *args, **kwargs)

        return decorator
    return decorator_maker


@decorator_with_args_for_any_decorator
def decorated_decorator(func: Callable, *args, **kwargs) -> Callable:
    """
    Пример.
    Args:
        func: Декорируемая функция.
        *args: Произвольные позиционные аргументы.
        **kwargs: Произвольные именованные аргументы.
    Returns:
        Обёрнутая функция с логированием аргументов декоратора.
    """

    @wraps(func)
    def wrapper(*f_args, **f_kwargs):
        print(f"Декоратор вызван с аргументами: {args}, {kwargs}")
        return func(*f_args, **f_kwargs)

    return wrapper


@decorated_decorator(100, 'рублей', 200, 'друзей')
def decorated_function(text: str, num: int) -> None:
    """
    Пример декорируемой функции.
    Args:
        text: Текст для вывода.
        num: Число для вывода.
    """
    print("Привет", text, num)


decorated_function("Юзер", 101)
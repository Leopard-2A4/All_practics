# TODO здесь писать код
from typing import TypeVar, Callable, Any, Type
from functools import wraps

T = TypeVar('T', bound=Type)


def singleton(cls: Type[T]) -> Callable[..., T]:
    """
    Декоратор для реализации паттерна Singleton.
    Гарантирует создание только одного экземпляра класса,
    независимо от количества вызовов конструктора.
    Args:
        cls: Класс, который нужно сделать синглтоном.
    Returns:
        Функцию-фабрику, возвращающую единственный экземпляр класса.
    """
    instances: dict[Type[T], T] = {}

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        """
        Фабричная функция, возвращающая единственный экземпляр класса.
        Args:
            *args: Аргументы для __init__.
            **kwargs: Именованные аргументы для __init__.
        Returns:
            Единственный экземпляр класса cls.
        Note:
            Последующие вызовы с новыми аргументами игнорируют их,
            возвращая первый созданный экземпляр.
        """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]
    return get_instance

@singleton
class Example:
    pass

my_obj = Example()
my_another_obj = Example()

print(id(my_obj))
print(id(my_another_obj))

print(my_obj is my_another_obj)
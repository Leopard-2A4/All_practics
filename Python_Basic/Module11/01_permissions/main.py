# TODO здесь писать код
import functools
from typing import Callable, Any


def check_permission(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для проверки прав доступа пользователя.
    Args:
        name: Имя разрешения, необходимое для выполнения декорируемой функции.
    Returns:
        Декоратор, который оборачивает функцию проверкой прав доступа.
    Raises:
        PermissionError: Если требуемое разрешение отсутствует у пользователя.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Внутренний декоратор, оборачивающий функцию.
        Args:
            func: Декорируемая функция.
        Returns:
            Обёрнутая функция с проверкой прав.
        """

        @functools.wraps(func)
        def wrapped(*args,**kwargs):
            """
            Обёртка функции с проверкой прав доступа.
            Args:
                *args: Позиционные аргументы для оригинальной функции.
                **kwargs: Именованные аргументы для оригинальной функции.
            Returns:
                Результат выполнения оригинальной функции, если права есть.
            Raises:
                PermissionError: Если у пользователя нет необходимых прав.
            """
            if name in user_permissions:
                return func(*args, **kwargs)
            else:
                raise PermissionError(
                    f'у пользователя недостаточно прав, чтобы выполнить функцию {func.__name__}'
                )

        return wrapped
    return decorator
user_permissions = ['admin']

@check_permission('admin')
def delete_site():
    print('Удаляем сайт')

@check_permission('user_1')
def add_comment():
    print('Добавляем комментарий')

delete_site()
add_comment()
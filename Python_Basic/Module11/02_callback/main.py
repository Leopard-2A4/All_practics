# TODO здесь писать код
import functools
from typing import Callable, Any


routes: dict[str, Callable[..., Any]] = {}

def callback(path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор callback для регистрации обработчиков маршрутов.

    Args:
        path: Путь URL для регистрации обработчика (например, '//').

    Returns:
        Декоратор, который регистрирует функцию как обработчик маршрута.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Внутренний декоратор для регистрации функции.

        Args:
            func: Обработчик маршрута.

        Returns:
            Обёрнутая функция, зарегистрированная для указанного пути.
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обёртка обработчика маршрута.

            Returns:
                Результат выполнения зарегистрированной функции.
            """
            return func(*args, **kwargs)

        # Регистрируем обработчик в глобальном хранилище
        routes[path] = wrapper
        return wrapper

    return decorator


# Имитация объекта app с методом get()
class App:
    @classmethod
    def get(cls,path: str) -> Callable[..., Any] | None:
        """
        Получает обработчик для указанного пути.
        Args:
            path: Путь URL.
        Returns:
            Обработчик маршрута или None, если маршрут не найден.
        """
        return routes.get(path)


app = App()


# Пример использования
@callback('//')
def example() -> str:
    """
    Обработчик маршрута '//'.

    Returns:
        Ответ сервера 'OK'.
    """
    print('Пример функции, которая возвращает ответ сервера')
    return 'OK'


# Основной код (точно как в задаче)
route = app.get('//')
if route:
    response = route()
    print('Ответ:', response)
else:
    print('Такого пути нет')

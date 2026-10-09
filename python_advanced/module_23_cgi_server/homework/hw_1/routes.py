import json
import re
from typing import Callable, Dict, Tuple, Any


class SimpleWSGIApp:
    """Простое WSGI приложение, обрабатывающее HTTP‑запросы и возвращающее JSON."""

    def __init__(self):
        """
        Создаёт пустой список маршрутов.
        Каждый маршрут — это кортеж: (regex, имена_параметров, обработчик, разрешённые_методы).
        """
        self._routes = []

    def route(self, rule: str, methods=('GET',)) -> Callable:
        """
        Декоратор для регистрации обработчика по пути.

        Параметры:
            rule: строка вида "/hello", "/hello/<name>".
            methods: разрешённые HTTP‑методы, по умолчанию ('GET').

        Логика:
            1. Превращает строку rule в регулярное выражение.
            2. Сохраняет regex, имена параметров, функцию и список методов в self._routes.
        """
        pattern, names = self._compile_rule(rule)

        def decorator(func: Callable):
            # Создаём regex, который будет искать точное совпадение для этого пути.
            regex = re.compile(f"^{pattern}$")
            # Сохраняем маршрут.
            methods_set = set(m.upper() for m in methods)
            self._routes.append((regex, names, func, methods_set))
            return func  # возвращаем ту же функцию, просто добавляем её в список маршрутов

        return decorator

    def _compile_rule(self, rule: str) -> Tuple[str, Tuple[str, ...]]:
        """
        Преобразует строку вида "/hello/<name>" в регулярное выражение.

        Возвращает:
            pattern: строку регулярки, которую можно передать в re.compile.
            names: кортеж имён параметров, например ('name',).

        Пример:
            "/hello/<name>" -> r"/hello/(?P<name>[^/]+)"
        """
        # Разбиваем строку rule на части:
        #   /hello/<name> -> ['/hello/', '<name>']
        parts = re.split(r'(<[^>]+>)', rule)
        names = []
        out = []  # тут собираем куски регулярки

        for part in parts:
            if not part:
                continue

            # Если часть — это "<имя>", например "<name>".
            m = re.match(r'^<(.+)>$', part)
            if m:
                name = m.group(1)  # имя параметра, например 'name'
                names.append(name)
                # добавляем именованную группу: (?P<name>[^/]+)
                out.append(f"(?P<{name}>[^/]+)")
            else:
                # Экранируем обычные части, чтобы символы в пути (. ? $) не ломали регулярку.
                out.append(re.escape(part))

        pattern = ''.join(out)  # собираем регулярку в строку
        return pattern, tuple(names)

    def _match(self, path: str) -> Tuple[Callable, Dict[str, str], set] | Tuple[None, None, None]:
        """
        Пытается найти в зарегистрированных маршрутах подходящий для данного пути.

        Возвращает:
            handler: функция‑обработчик (или None).
            params: словарь параметров вида {"name": "artem"} или {} (или None).
            methods: set разрешённых методов или None.
        """
        for regex, names, handler, methods in self._routes:
            # Пытаемся применить регулярку к пути.
            m = regex.match(path)
            if m:
                # m.groupdict() — словарь с именованными группами, например {"name": "artem"}
                return handler, m.groupdict(), methods

        # Ничего не подошло.
        return None, None, None

    def _json_response(self, start_response: Callable, body: Any, status_code: int = 200) -> list:
        """
        Формирует HTTP‑ответ с JSON‑телом.

        Параметры:
            start_response: стандартная WSGI‑функция для отправки статуса и заголовков.
            body: любой объект (dict, list, str, ...), который будет сериализован в JSON.
            status_code: HTTP‑код, по умолчанию 200.

        Возвращает список байтов, который ожидает WSGI.
        """
        body_text = json.dumps(body, indent=4)  # в строку JSON
        body_bytes = body_text.encode('utf-8')  # в байты

        if status_code == 200:
            status = "200 OK"
        else:
            status = f"{status_code} NOT FOUND"

        headers = [
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Content-Length', str(len(body_bytes)))
        ]

        start_response(status, headers)
        return [body_bytes]  # WSGI‑ответ — это итерируемый объект байтов

    def __call__(self, environ: Dict, start_response: Callable) -> list:
        """
        Эта функция делает экземпляр класса вызываемым (WSGI application).

        Параметры:
            environ: словарь с информацией о запросе от WSGI‑сервера.
            start_response: функция для отправки статуса и заголовков.

        Возвращает:
            Список байтов — тело HTTP‑ответа.
        """
        # Пытаемся извлечь полный путь из запроса.
        raw = (environ.get('REQUEST_URI')
               or environ.get('RAW_URI')
               or environ.get('PATH_INFO', '/'))

        # Убираем часть после ? (query string).
        path = raw.split('?', 1)[0]

        # Ищем подходящий маршрут.
        handler, params, methods = self._match(path)

        if handler is None:
            # Маршрут не найден -> 404
            return self._json_response(start_response, {"error": "Not Found"}, status_code=404)

        # Получаем HTTP‑метод.
        method = environ.get('REQUEST_METHOD', 'GET').upper()

        # Если есть список разрешённых методов, проверяем, разрешён ли текущий.
        if methods and method not in methods:
            start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
            return [b'Method Not Allowed']

        try:
            # Вызываем обработчик с параметрами (или без).
            if params:
                result = handler(**params)
            else:
                result = handler()

            # Варианты, что может вернуть handler:
            if isinstance(result, (dict, list)):
                # Обычный Python‑объект — сериализуем в JSON.
                return self._json_response(start_response, result, status_code=200)

            elif isinstance(result, str):
                # Строка, которая уже JSON.
                body_bytes = result.encode('utf-8')
                start_response('200 OK', [
                    ('Content-Type', 'application/json; charset=utf-8'),
                    ('Content-Length', str(len(body_bytes)))
                ])
                return [body_bytes]

            else:
                # Всё остальное — просто сериализуем в JSON.
                return self._json_response(start_response, result, status_code=200)

        except Exception as e:
            # Любая ошибка в обработчике -> 500 Internal Server Error.
            return self._json_response(start_response,
                                       {"error": "Internal Server Error", "detail": str(e)},
                                       status_code=500)


app = SimpleWSGIApp()


@app.route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)


@app.route("/hello/<name>")
def say_hello_with_name(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)


application = app

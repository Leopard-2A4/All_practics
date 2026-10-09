# TODO здесь писать код
from typing import Any, Optional

class MyDict(dict):
    """
    Класс MyDict наследуется от стандартного dict и переопределяет метод get.
    Если ключ отсутствует, метод get возвращает 0 по умолчанию, а не None.
    """

    def get(self, key: Any, default: Optional[int] = 0) -> Any:
        """
        Возвращает значение по ключу, если ключ существует.
        Если ключ отсутствует, возвращает значение по умолчанию (0).

        :param key: Ключ, по которому ищется значение.
        :param default: Значение по умолчанию (по умолчанию 0).
        :return: Значение по ключу или значение по умолчанию.
        """
        return super().get(key, default)


# Пример использования
exampl = MyDict()
exampl['key'] = 'value'
exampl['key2'] = 'value2'
print(exampl['key'])  # value
print(exampl.get('key2'))  # value2
print(exampl.get('key3'))  # 0
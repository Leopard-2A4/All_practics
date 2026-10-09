# TODO здесь писать код
class Node:
    """
    Узел односвязного списка.
    Хранит данные и ссылку на следующий узел.
    """

    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """
    Односвязный список с поддержкой итерации.
    """

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data) -> None:
        """
        Добавляет элемент в конец списка.
        :param data: Данные для добавления.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def get(self, index: int):
        """
        Возвращает элемент по индексу.
        :param index: Индекс элемента (начиная с 0).
        :return: Данные элемента.
        :raises IndexError: Если индекс вне диапазона.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Индекс вне диапазона")

        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def remove(self, index: int) -> None:
        """
        Удаляет элемент по индексу.
        :param index: Индекс элемента для удаления.
        :raises IndexError: Если индекс вне диапазона.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Индекс вне диапазона")

        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            current.next = current.next
        self._size -= 1

    def __iter__(self):
        """
        Делает список итерируемым.
        """
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self) -> str:
        """
        Возвращает строковое представление списка.
        """
        if not self.head:
            return "[]"
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return f"[{' '.join(result)}]"

    def __len__(self) -> int:
        """
        Возвращает количество элементов в списке.
        """
        return self._size


# Пример использования
my_list = LinkedList()
my_list.append(10)
my_list.append(20)
my_list.append(30)

print('Текущий список:', my_list)
print('Получение третьего элемента:', my_list.get(2))
print('Удаление второго элемента.')
my_list.remove(1)
print('Новый список:', my_list)

# Дополнительная демонстрация итерации
print("\nИтерация по списку:")
for item in my_list:
    print(item)

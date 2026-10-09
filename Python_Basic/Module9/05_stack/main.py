# TODO здесь писать код
from typing import Dict, List

class TaskManager:
    """
    Класс для управления задачами.
    Хранит задачи в словаре, где ключ — приоритет, значение — список задач.
    Предоставляет методы для добавления, удаления и вывода задач.
    """

    def __init__(self) -> None:
        """
        Инициализирует пустой словарь для хранения задач.
        """
        self.tasks: Dict[int, List[str]] = {}

    def del_task(self, num: int) -> None:
        """
        Удаляет задачу по номеру (ключу).
        :param num: Номер задачи (ключ).
        """
        if num in self.tasks:
            del self.tasks[num]
            print(f"Задача с номером {num} удалена.")
        else:
            print(f"Задача с номером {num} не найдена.")

    def new_task(self, task: str, num: int) -> None:
        """
        Добавляет новую задачу с указанным номером.
        :param task: Текст задачи.
        :param num: Номер задачи (ключ).
        """
        if num in self.tasks:
            self.tasks[num].append(task)
        else:
            self.tasks[num] = [task]

    def print_tasks(self) -> None:
        """
        Выводит все задачи, отсортированные по приоритету в обратном порядке.
        """
        sorted_tasks = sorted(self.tasks.items(), reverse=True)
        for priority, task_list in sorted_tasks:
            print(f"{priority} — {'; '.join(task_list)}")

manager = TaskManager()
manager.new_task("сделать уборку", 4)
manager.new_task("помыть посуду", 4)
manager.new_task("отдохнуть", 1)
manager.new_task("поесть", 2)
manager.new_task("сдать ДЗ", 2)
manager.print_tasks()

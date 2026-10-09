import logging
import random
import threading
import time
import queue
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Task:
    """Задача с приоритетом и функцией для выполнения."""

    def __init__(self, priority: int, func: Callable, *args: Any):
        self.priority = priority
        self.func = func
        self.args = args

    def __lt__(self, other: 'Task') -> bool:
        return self.priority < other.priority

    def run(self):
        duration = self.func(*self.args)
        return duration


def sleep_task(seconds: float) -> float:
    time.sleep(seconds)
    return seconds


class Producer(threading.Thread):
    """Генерирует 10 задач в очередь."""

    def __init__(self, task_queue: queue.PriorityQueue):
        super().__init__(name='Producer')
        self.task_queue = task_queue

    def run(self):
        logger.info('Producer: Running')

        priorities = [0, 0, 1, 1, 2, 2, 3, 3, 4, 6]
        for priority in priorities:
            duration = random.random()
            task = Task(priority, sleep_task, duration)
            self.task_queue.put(task)

        logger.info('Producer: Done')


class Consumer(threading.Thread):
    """Исполняет задачи по приоритету."""

    def __init__(self, task_queue: queue.PriorityQueue):
        super().__init__(name='Consumer')
        self.task_queue = task_queue

    def run(self):
        logger.info('Consumer: Running')

        while not self.task_queue.empty():
            try:
                task = self.task_queue.get(timeout=0.1)
                duration = task.run()
                logger.info(f'>running Task(priority={task.priority}). \t sleep({duration:.10f})')
                self.task_queue.task_done()
            except queue.Empty:
                break

        self.task_queue.join()
        logger.info('Consumer: Done')


def main():
    task_queue = queue.PriorityQueue()

    producer = Producer(task_queue)
    consumer = Consumer(task_queue)

    producer.start()
    producer.join()

    consumer.start()
    consumer.join()


if __name__ == '__main__':
    main()
"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
from types import TracebackType
from typing import Type, Literal, IO, Optional
import sys


class Redirect:
    def __init__(self, stdout: Optional[IO] = None, stderr: Optional[IO] = None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self._original_stdout = None
        self._original_stderr = None

    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        if self.stdout is not None:
            sys.stdout = self.stdout

        if self.stderr is not None:
            sys.stderr = self.stderr

        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

        return None
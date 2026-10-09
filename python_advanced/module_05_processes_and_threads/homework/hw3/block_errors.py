"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""
from typing import Collection, Type, Literal
from types import TracebackType
from typing import TypeAlias

TracebackTypeOrNone: TypeAlias = "TracebackType | None"  # Альтернатива

class BlockErrors:
    def __init__(self, errors: Collection[Type[BaseException]]) -> None:
        self.errors = errors

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None  # Правильная аннотация
    ) -> Literal[True] | None:
        if exc_type is None:
            return None
        if issubclass(exc_type, tuple(self.errors)):
            return True
        return None

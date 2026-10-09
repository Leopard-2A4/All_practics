"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field, ValidationError


def number_length(min_length: int, max_length: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        value = field.data
        if value is None:
            return

        length = len(str(value))
        if not (min_length <= length <= max_length):
            if message:
                raise ValidationError(message)
            raise ValidationError(
                f'Длина должна быть от {min_length} до {max_length} символов. '
                f'Текущая длина: {length}'
            )

    return _number_length


class NumberLength:
    def __init__(self, min_length: int, max_length: int, message: Optional[str] = None):
        self.min_length = min_length
        self.max_length = max_length
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        value = field.data
        if value is None:
            return

        length = len(str(value))
        if not (self.min_length <= length <= self.max_length):
            if self.message:
                raise ValidationError(self.message)
            raise ValidationError(
                f'Длина должна быть от {self.min_length} до {self.max_length} символов. '
                f'Текущая длина: {length}'
            )

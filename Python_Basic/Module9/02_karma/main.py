# TODO здесь писать код
import random

class KillError(Exception):
    """Исключение: убийство."""
    pass

class DrunkError(Exception):
    """Исключение: пьянство."""
    pass

class CarCrashError(Exception):
    """Исключение: авария."""
    pass

class GluttonyError(Exception):
    """Исключение: обжорство."""
    pass

class DepressionError(Exception):
    """Исключение: депрессия."""
    pass

def one_day() -> int:
    """
    Возвращает случайное количество кармы от 1 до 7.
    С вероятностью 1 к 10 вызывает одно из исключений:
    KillError, DrunkError, CarCrashError, GluttonyError, DepressionError.
    :return: Количество кармы за день (целое число).
    :raises KillError, DrunkError, CarCrashError, GluttonyError, DepressionError:
             Исключения, связанные с негативными событиями.
    """
    karma: int = random.randint(1, 7)
    if random.randint(1, 10) == 1:
        error = random.choice([KillError, DrunkError, CarCrashError, GluttonyError, DepressionError])
        raise error()
    return karma

# Основная программа
KARMA_LEVEL: int = 500
karma: int = 0

with open('karma.log', 'w', encoding='utf-8') as log_file:
    while karma < KARMA_LEVEL:
        try:
            karma += one_day()
        except KillError as exc:
            log_file.write(f'KillError: {exc}\n')
        except DrunkError as exc:
            log_file.write(f'Drunk

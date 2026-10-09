import logging
from typing import Union, Callable
from operator import sub, mul, truediv, add

logger = logging.getLogger('utils')  # ✅ utils логгер (INFO+ в utils.log)

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logger.error("wrong operator type: %s", value)  # ✅ ERROR → utils.log
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("wrong operator value: %s", value)  # ✅ ERROR → utils.log
        raise ValueError("wrong operator value")

    logger.info("Operator converted: %s", value)  # ✅ INFO → utils.log

    return OPERATORS[value]

import sys
import logging
from utils import string_to_operator


def setup_logging_basic():
    """Конфигурирует логирование с basicConfig в stdout"""
    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)


def calc(args):
    logger = logging.getLogger(__name__)

    logger.info(f"Arguments: {args}")

    num_1_str, operator_str, num_2_str = args[0], args[1], args[2]

    try:
        num_1 = float(num_1_str)
        logger.debug(f"num_1: {num_1}")
    except ValueError as e:
        logger.error(f"Ошибка num_1 '{num_1_str}': {e}")
        return

    try:
        num_2 = float(num_2_str)
        logger.debug(f"num_2: {num_2}")
    except ValueError as e:
        logger.error(f"Ошибка num_2 '{num_2_str}': {e}")
        return

    operator_func = string_to_operator(operator_str)
    result = operator_func(num_1, num_2)

    logger.info(f"Result: {result}")
    print(f"{num_1} {operator_str} {num_2} = {result}")


if __name__ == '__main__':
    setup_logging_basic()
    args = sys.argv[1:] or ['2', '+', '3']
    calc(args)

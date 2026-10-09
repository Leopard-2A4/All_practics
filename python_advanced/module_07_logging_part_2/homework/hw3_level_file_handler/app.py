import sys
import logging
from utils import string_to_operator


class LevelFileHandler(logging.Handler):
    def __init__(self, base_filename: str):
        super().__init__()
        self.base_filename = base_filename

    def emit(self, record):
        if record.levelno == logging.DEBUG:
            filename = f"{self.base_filename}_debug.log"
        elif record.levelno == logging.INFO:
            filename = f"{self.base_filename}_info.log"
        elif record.levelno >= logging.WARNING:
            filename = f"{self.base_filename}_error.log"
        else:
            filename = f"{self.base_filename}_unknown.log"

        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"{self.format(record)}\n")
        except Exception:
            self.handleError(record)


def setup_logging():
    logger = logging.getLogger('calc')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console_handler)

    file_handler = LevelFileHandler('calc')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)

    return logger


def calc(args):
    logger = logging.getLogger('calc')

    logger.info("Arguments: %s", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.error("Error details: %s", e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2")
        logger.error("Error details: %s", e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.info("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == '__main__':
    logger = setup_logging()
    calc('2+3')

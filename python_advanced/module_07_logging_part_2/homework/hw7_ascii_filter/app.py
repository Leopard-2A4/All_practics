import sys
import logging.config  # ✅ Новый импорт
from utils import string_to_operator
from logging_config import dict_config  # ✅ Импорт конфигурации


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

    logging.config.dictConfig(dict_config)


    calc('2+3')

    logger = logging.getLogger('calc')
    logger.info("Тест ASCII: только латиница")
    logger.info("Тест не-ASCII: ÎŒØ∏‡°⁄·°€йцукен")
    logger.error("Кириллица: ошибка!")

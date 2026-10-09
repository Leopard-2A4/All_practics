## Задача 2. ОПП-конфигурация
### Что нужно сделать
Добавьте в приложение выше(hw1_add_logging) скопировав его в текущею папку, функцию, которая будет конфигурировать логирование с помощью `basicConfig`. Обработчик должен выводить логи в стандартный поток вывода (stdout). 

Также добавьте форматирование с помощью класса `Formatter` ко всем обработчикам в таком виде:

`уровень | логгер | время | номер строки | сообщение`

### Что оценивается
* Созданный обработчик выводит логи в stdout, а не в stderr.
* Форматирование происходит с помощью класса Formatter.
* import sys
from utils import string_to_operator
import logging
import logging.config
from module_07_logging_part_2.homework.hw2_config_function.config import dict_config

def calc(args):
    print("Arguments: ", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        print("Error while converting number 1")
        print(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        print("Error while converting number 2")
        print(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    print("Result: ", result)
    print(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc('2+3')
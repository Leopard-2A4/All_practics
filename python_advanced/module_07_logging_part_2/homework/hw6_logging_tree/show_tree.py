import logging.config
from logging_tree import printout
from logging_config import dict_config
import sys

logging.config.dictConfig(dict_config)

logging.getLogger('calc')
logging.getLogger('utils')
logging.getLogger('test.module')

printout()

import io
from contextlib import redirect_stdout

f = io.StringIO()
with redirect_stdout(f):
    printout()
tree_output = f.getvalue()

with open('logging_tree.txt', 'w', encoding='utf-8') as f:
    f.write("Дерево логгеров после настройки конфигурации:\n")
    f.write("=" * 50 + "\n\n")
    f.write(tree_output)
    f.write("\n\n" + "=" * 50 + "\n")
    f.write("Ожидаемый результат:\n")
    f.write("- root (WARNING)\n")
    f.write("- calc (DEBUG) с handlers: console, calc_level_files\n")
    f.write("- utils (INFO) с handler: utils_file (TimedRotatingFileHandler)\n")
    f.write("- test.module (унаследованные настройки)\n")

print("logging_tree.txt создан!")
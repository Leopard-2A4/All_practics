import logging.config
from dict_config import dict_config

# Загрузка конфигурации (идентична logging.config.fileConfig('logging_conf.ini'))
logging.config.dictConfig(dict_config)


root_logger = logging.getLogger()
root_logger.debug("Root DEBUG → logfile.log")
root_logger.warning("Root WARNING → консоль")

app_logger = logging.getLogger('appLogger')
app_logger.debug("appLogger DEBUG → logfile.log + НЕ консоль")
app_logger.info("appLogger INFO → logfile.log")

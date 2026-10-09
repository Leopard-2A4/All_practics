import logging.config
from logging.handlers import TimedRotatingFileHandler


def is_ascii(text: str) -> bool:
    """Проверяет, содержит ли строка только ASCII символы"""
    for char in text:
        if ord(char) > 127:
            return False
    return True


class AsciiFilter(logging.Filter):
    """Фильтр: пропускает только сообщения с ASCII символами"""

    def filter(self, record) -> bool:
        msg = str(record.getMessage())
        if not is_ascii(msg):
            return False

        for arg in getattr(record, 'args', []):
            if not is_ascii(str(arg)):
                return False

        return True


dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'filters': {
        'ascii_only': {
            '()': 'logging_config.AsciiFilter',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'filters': ['ascii_only'],
        },
        'calc_level_files': {
            '()': 'logging_config.LevelFileHandler',
            'base_filename': 'calc',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'filters': ['ascii_only'],
        },
        'utils_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'utils.log',
            'when': 'H',
            'interval': 10,
            'backupCount': 5,
            'formatter': 'detailed',
            'level': 'INFO',
            'filters': ['ascii_only'],
        }
    },
    'loggers': {
        'calc': {
            'handlers': ['console', 'calc_level_files'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'utils': {
            'handlers': ['utils_file'],
            'level': 'INFO',
            'propagate': False,
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': []
    }
}


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

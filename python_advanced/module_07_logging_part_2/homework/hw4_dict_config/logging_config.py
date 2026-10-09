import logging.config

dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'DEBUG',
        },
        'level_files': {
            '()': 'logging_config.LevelFileHandler',
            'base_filename': 'calc',
            'formatter': 'detailed',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'calc': {
            'handlers': ['console', 'level_files'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
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

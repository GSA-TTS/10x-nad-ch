import logging
from nad_ch.application.interfaces import Logger


class BasicLogger(Logger):
    def __init__(self, name=__name__, logger_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logger_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

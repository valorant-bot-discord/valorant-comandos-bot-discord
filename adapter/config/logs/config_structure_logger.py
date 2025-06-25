import logging
import sys

from adapter.config.logs.custom_json_formatter import CustomJsonFormatter


class ConfigStructureLogger:
    _instance = None

    def __new__(cls, *, log_to_file=False, file_path="app.log"):
        if cls._instance is None:
            cls._instance = super(ConfigStructureLogger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.logger = logging.getLogger("bot_discord_logger")

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(CustomJsonFormatter())
            self.logger.addHandler(handler)

    def info(self, *, code: str, message: str):
        self.logger._log(logging.INFO, msg=message, args=(), extra={"code": code})

    def warning(self, *, code: str, message: str):
        self.logger._log(logging.WARNING, msg=message, args=(), extra={"code": code})

    def error(self, *, code: str, message: str = None, throw: Exception = None):
        self.logger._log(logging.ERROR, msg=message, args=(), extra={"code": code, "throw": throw})

    def critical(self, *, code: str, message: str = None, throw: Exception = None):
        self.logger._log(logging.CRITICAL, msg=message, args=(), extra={"code": code, "throw": throw})

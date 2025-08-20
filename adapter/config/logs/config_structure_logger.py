import logging
import sys

from adapter.config.logs.custom_json_formatter import CustomJsonFormatter


class ConfigStructureLogger:
    _instance = None

    def __new__(cls, *, log_to_file=False, file_path="app.log"):
        if cls._instance is None:
            cls._instance = super(ConfigStructureLogger, cls).__new__(cls)
            cls._instance._log_to_file_arg = log_to_file
            cls._instance._file_path_arg = file_path
        return cls._instance

    def __init__(self, *, log_to_file=False, file_path="app.log"):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger("bot_discord_logger")
            self.logger.setLevel(logging.INFO)

            if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(CustomJsonFormatter())
                self.logger.addHandler(console_handler)

            effective_log_to_file = getattr(self, '_log_to_file_arg', log_to_file)
            effective_file_path = getattr(self, '_file_path_arg', file_path)

            if effective_log_to_file and not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
                try:
                    file_handler = logging.FileHandler(effective_file_path)
                    file_handler.setFormatter(CustomJsonFormatter())
                    self.logger.addHandler(file_handler)
                except Exception as e:
                    print(f"Erro ao configurar o FileHandler: {e}")

    def info(self, *, code: str, message: str, payload=None):
        self.logger._log(logging.INFO, msg=message, args=(), extra={"code": code, "payload": payload})

    def warning(self, *, code: str, message: str, payload=None):
        self.logger._log(logging.WARNING, msg=message, args=(), extra={"code": code, "payload": payload})

    def error(self, *, code: str, message: str = None, throw: Exception = None, payload=None):
        self.logger._log(logging.ERROR, msg=message, args=(), extra={"code": code, "throw": throw, "payload": payload})

    def critical(self, *, code: str, message: str = None, throw: Exception = None, payload=None):
        self.logger._log(logging.CRITICAL, msg=message, args=(),
                         extra={"code": code, "throw": throw, "payload": payload})

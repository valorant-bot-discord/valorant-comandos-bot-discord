import logging
import json
import sys
import traceback
from datetime import datetime


class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "ApplicationName": "bot_discord",
            "Code": getattr(record, "code", "sem-codigo"),
            "Message": record.getMessage(),
            "Datetime": datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M:%S"),
            "Severity": record.levelname
        }

        if record.levelname in ("ERROR", "CRITICAL") and hasattr(record, "throw") and record.throw:
            log_data["Throw"] = record.throw if isinstance(record.throw, str) else "".join(
                traceback.format_exception(None, record.throw, record.throw.__traceback__)
            )

        return json.dumps(log_data, ensure_ascii=False)


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

    def info(self, *, code, message):
        self.logger._log(logging.INFO, message, args=(), extra={"code": code})

    def warning(self, *, code, message):
        self.logger._log(logging.WARNING, message, args=(), extra={"code": code})

    def error(self, *, code: str, message: str, throw: Exception = None):
        self.logger._log(logging.ERROR, message, args=(), extra={"code": code, "throw": throw})

    def critical(self, *, code: str, message: str, throw: Exception = None):
        self.logger._log(logging.CRITICAL, message, args=(), extra={"code": code, "throw": throw})

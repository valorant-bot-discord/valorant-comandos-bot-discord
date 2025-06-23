import json
import traceback
import logging
from datetime import datetime

from adapter.config.inicializacao_config import config
from adapter.constantes import DATETIME_FORMAT
from adapter.exception.log_exceptions import LoggerErrorException
from adapter.utils.logger_utils import extract_throw_info, get_relative_path


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            log_data = {
                "ApplicationName": config.APPLICATION_NAME,
                "Code": getattr(record, "code", "sem-codigo"),
                "Message": record.getMessage(),
                "Path": get_relative_path(record.pathname, record.lineno),
                "Datetime": datetime.fromtimestamp(record.created).strftime(DATETIME_FORMAT),
                "Severity": record.levelname
            }

            if record.levelname in ("ERROR", "CRITICAL") and hasattr(record, "throw") and record.throw:
                log_data["Throw"] = self._format_throw_field(record.throw)
            return json.dumps(log_data, ensure_ascii=False)
        except Exception as ex:
            fallback_log = {
                "ApplicationName": config.APPLICATION_NAME,
                "Code": "sem-codigo",
                "Message": "Erro ao formatar log",
                "Severity": "CRITICAL",
                "Datetime": datetime.now().strftime(DATETIME_FORMAT),
                "Error": str(ex)
            }
            return json.dumps(fallback_log, ensure_ascii=False)

    @staticmethod
    def _format_throw_field(throw) -> dict:
        try:
            if isinstance(throw, Exception):
                tb = throw.__traceback__
                traceback_info = "".join(traceback.format_exception(type(throw), throw, tb))
                return extract_throw_info(throw, traceback_info)
            return extract_throw_info(throw, "Indisponível (não é um objeto de exceção)")
        except Exception as ex:
            return extract_throw_info(LoggerErrorException(ex), "Indisponível")

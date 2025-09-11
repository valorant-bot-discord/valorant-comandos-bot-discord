import json
import traceback
import logging
from datetime import datetime

from adapter.config.inicializacao_config import config
from adapter.config.logs.transaction_context import transaction_context
from adapter.constantes import DATETIME_FORMAT
from adapter.decoradores.remove_null_keys import remove_null_keys
from adapter.exception.log_exceptions import LoggerErrorException


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        transaction_id = transaction_context.get_id()
        try:
            log_data = self._build_log_data(record, transaction_id)
            return json.dumps(log_data, ensure_ascii=False)

        except Exception as ex:
            fallback_log = self._build_fallback_log(transaction_id, ex)
            return json.dumps(fallback_log, ensure_ascii=False)

    @remove_null_keys
    def _build_log_data(self, record: logging.LogRecord, transaction_id: str) -> dict:
        log_data = {
            "ApplicationName": config.application_name,
            "Code": getattr(record, "code", "sem-codigo"),
            "TransactionId": transaction_id,
            "Message": record.getMessage(),
            "Datetime": datetime.fromtimestamp(record.created).strftime(DATETIME_FORMAT),
            "Severity": record.levelname,
        }

        if hasattr(record, "payload") and record.payload is not None:
            log_data["Payload"] = record.payload

        if record.levelname in ("ERROR", "CRITICAL") and hasattr(record, "throw") and record.throw:
            log_data["Throw"] = self._format_throw_field(record.throw)

        return log_data

    @remove_null_keys
    def _build_fallback_log(self, transaction_id: str, ex: Exception) -> dict:
        return {
            "ApplicationName": config.application_name,
            "Code": "sem-codigo",
            "TransactionId": transaction_id,
            "Message": "Erro ao formatar log",
            "Severity": "CRITICAL",
            "Datetime": datetime.now().strftime(DATETIME_FORMAT),
            "Error": str(ex)
        }

    def _format_throw_field(self, throw) -> dict:
        try:
            if isinstance(throw, Exception):
                tb = throw.__traceback__
                traceback_info = "".join(traceback.format_exception(type(throw), throw, tb))
                return self._extract_throw_info(throw, traceback_info)
            return self._extract_throw_info(throw, "Indisponível (não é um objeto de exceção)")
        except Exception as ex:
            return self._extract_throw_info(LoggerErrorException(ex), "Indisponível")

    @staticmethod
    def _extract_throw_info(throw, traceback_info):
        return {
            "Type": type(throw).__name__,
            "Message": str(throw),
            "Traceback": traceback_info
        }

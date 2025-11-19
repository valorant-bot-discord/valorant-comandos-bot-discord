import uuid
import contextvars
from typing import Optional


class TransactionContext:
    _transaction_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("transaction_id", default=None)

    @classmethod
    def start_new(cls) -> str:
        transaction_id = str(uuid.uuid4())
        cls._transaction_var.set(transaction_id)
        return transaction_id

    @classmethod
    def set_id(cls, transaction_id: Optional[str]) -> None:
        cls._transaction_var.set(transaction_id)

    @classmethod
    def get_id(cls) -> Optional[str]:
        return cls._transaction_var.get()

transaction_context = TransactionContext()
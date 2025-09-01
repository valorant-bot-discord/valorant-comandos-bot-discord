import contextvars
import uuid


class TransactionContext:
    _transaction_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar('transaction_id', default=None)

    @classmethod
    def start_new(cls):
        cls._transaction_id_var.set(str(uuid.uuid4()))

    @classmethod
    def get_id(cls) -> str | None:
        return cls._transaction_id_var.get()

    @classmethod
    def set_id(cls, transaction_id: str):
        cls._transaction_id_var.set(transaction_id)


transaction_context = TransactionContext()

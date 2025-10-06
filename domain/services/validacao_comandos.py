from abc import ABC, abstractmethod


class ValidacaoComandos(ABC):

    @abstractmethod
    async def validar_autorizacao(self, mensagem, bot) -> bool:
        pass

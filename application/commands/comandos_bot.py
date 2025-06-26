from abc import ABC, abstractmethod


class ComandosBase(ABC):
    @abstractmethod
    async def registro_comando(self):
        pass

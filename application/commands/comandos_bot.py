from abc import ABC, abstractmethod


class ComandosBase(ABC):
    @abstractmethod
    def registro_comando(self):
        pass

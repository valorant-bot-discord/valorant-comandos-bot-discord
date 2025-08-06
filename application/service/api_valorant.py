from abc import ABC, abstractmethod

from domain.entity.agente import Agente


class ApiValorant(ABC):
    @abstractmethod
    def consultar_agentes(self) -> list[Agente] | None:
        pass

import requests

from adapter.config.logs.config_structure_logger import ConfigStructureLogger
from adapter.constantes import API_VALORANT
from application.service.api_valorant import ApiValorant
from domain.entity.agente import Agente

LOG_CODE = "consulta-infos-agentes"
logger = ConfigStructureLogger()


class ApiValorantImpl(ApiValorant):
    def consultar_agentes(self) -> list[Agente] | None:
        agentes = []
        try:
            response = requests.get(f"{API_VALORANT}/agents", timeout=0.5)

            for agent in response.json()["data"]:
                if agent.get("isPlayableCharacter"):
                    agente = Agente(
                        nome=agent.get("displayName"),
                        funcao=agent.get("role", {}).get("displayName") if agent.get("role") else None,
                    )
                    agentes.append(agente)
            return agentes
        except requests.RequestException as ex:
            logger.error(code=LOG_CODE, message="Erro na requisição HTTP", throw=ex)
            return None

        except Exception as ex:
            logger.error(code=LOG_CODE, message="Erro inesperado", throw=ex)
            return None

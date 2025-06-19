import requests

from adapter.config.logs.logger_config import ConfigStructureLogger
from adapter.constantes import API_VALORANT
from domain.entity.agente import Agente

LOG_CODE = "consulta-infos-agentes"
logger = ConfigStructureLogger()

def obter_agentes() -> list[Agente] | None:
    agentes = []
    try:
        response = requests.get(API_VALORANT)

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
        logger.error(code=LOG_CODE, message="Erro ao processar agentes", throw=ex)
        return None
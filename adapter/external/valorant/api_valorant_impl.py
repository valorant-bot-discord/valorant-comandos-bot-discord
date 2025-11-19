import threading

import requests
from cachetools import TTLCache, cached

from adapter.config.inicializacao_config import config
from adapter.config.logs.config_structure_logger import logger
from adapter.constantes import API_VALORANT
from application.service.api_valorant import ApiValorant
from domain.entity.agente import Agente

LOG_CODE = "consulta-infos-agentes"
cache_agentes = TTLCache(maxsize=1, ttl=config.cache_ttl_agentes)


class ApiValorantImpl(ApiValorant):
    def consultar_agentes(self) -> list[Agente] | None:
        agentes_em_cache = cache_agentes.get("lista_agentes_valorant")
        if agentes_em_cache is not None:
            logger.info(code=LOG_CODE, message="Agentes encontrados no cache.")
            return agentes_em_cache

        logger.info(code=LOG_CODE, message="Cache de agentes vazio buscando agentes na API externa.")
        try:
            agentes = []
            response = requests.get(f"{API_VALORANT}/agents", timeout=2.0, params={"language": "pt-BR"})
            response.raise_for_status()

            for agent in response.json().get("data", []):
                if agent.get("isPlayableCharacter"):
                    agentes.append(Agente(
                        nome=agent.get("displayName"),
                        funcao=agent.get("role", {}).get("displayName") if agent.get("role") else None,
                    ))

            # protege a escrita caso haja múltiplas threads
            with threading.Lock():
                cache_agentes["lista_agentes_valorant"] = agentes

            return agentes
        except requests.RequestException as ex:
            logger.error(code=LOG_CODE, message="Erro na requisição HTTP", throw=ex)
            return None

        except Exception as ex:
            logger.error(code=LOG_CODE, message="Erro inesperado", throw=ex)
            return None

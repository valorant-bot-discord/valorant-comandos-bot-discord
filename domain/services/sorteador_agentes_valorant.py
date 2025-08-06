import random

from adapter.external.valorant.api_valorant_impl import ApiValorantImpl
from domain.entity.agente import Agente
from domain.entity.jogadores import Jogador


class SorteadorDeAgentesValorant:
    def __init__(self):
        self.api_valorant = ApiValorantImpl()

    def sortear(self, jogadores: list[Jogador]) -> dict[Jogador, Agente]:
        agentes = self.api_valorant.consultar_agentes()
        if not agentes or len(agentes) < len(jogadores):
            raise ValueError(
                f"Não há agentes suficientes disponíveis para o sorteio. Quantidade máxima: {len(agentes)}. Você selecionou: {len(jogadores)}")

        random.shuffle(jogadores)
        agentes_sorteados = random.sample(agentes, len(jogadores))

        return dict(zip(jogadores, agentes_sorteados))

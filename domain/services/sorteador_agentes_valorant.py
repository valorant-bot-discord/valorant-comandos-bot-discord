import random

from adapter.external.valorant.agentes_disponiveis import obter_agentes
from domain.entity.agente import Agente
from domain.entity.jogadores import Jogador


class SorteadorDeAgentesValorant:

    @staticmethod
    def sortear(jogadores: list[Jogador]) -> dict[Jogador, Agente]:
        agentes = obter_agentes()
        if not agentes or len(agentes) < len(jogadores):
            raise ValueError("Não há agentes suficientes disponíveis para o sorteio.")

        random.shuffle(jogadores)
        agentes_sorteados = random.sample(agentes, len(jogadores))

        return dict(zip(jogadores, agentes_sorteados))

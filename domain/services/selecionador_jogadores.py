from typing import List, Set

from domain.entity.jogadores import Jogador


class SelecionadorJogadores:
    def __init__(self, jogadores: List[Jogador]):
        self.jogadores = jogadores
        self.selecionados_ids: Set[int] = set()

    def selecionar(self, jogador_id: int):
        self.selecionados_ids.add(jogador_id)

    def desselecionar(self, jogador_id: int):
        self.selecionados_ids.discard(jogador_id)

    def alternar_selecao(self, jogador_id: int):
        if jogador_id in self.selecionados_ids:
            self.desselecionar(jogador_id)
        else:
            self.selecionar(jogador_id)

    def esta_selecionado(self, jogador_id: int) -> bool:
        return jogador_id in self.selecionados_ids

    def tem_selecionados(self) -> bool:
        return len(self.selecionados_ids) > 0

    def obter_selecionados(self) -> List[Jogador]:
        return [jogador for jogador in self.jogadores if jogador.id_role in self.selecionados_ids]

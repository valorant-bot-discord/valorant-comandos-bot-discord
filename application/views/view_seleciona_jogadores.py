from discord.ui import View, Button
from discord import ButtonStyle, Interaction

from application.constantes import WAIT_FOR_MESSAGE_TIMEOUT, JOGADORES_POR_PAGINA
from domain.services.selecionador_jogadores import SelecionadorJogadores
from domain.services.sorteador_agentes_valorant import SorteadorDeAgentesValorant
from adapter.config.logs.config_structure_logger import ConfigStructureLogger
from utils.discord_view_utils import handle_view_timeout

logger = ConfigStructureLogger()
LOG_CODE = "cria-view-selecionador-jogadores"


class ViewSelecionaJogadores(View):
    def __init__(self, jogadores, ctx, pagina_atual=0, selecionador_jogadores=None):
        super().__init__(timeout=WAIT_FOR_MESSAGE_TIMEOUT)
        self.ctx = ctx
        self.selecionador_jogadores = selecionador_jogadores or SelecionadorJogadores(jogadores)
        self.selecionador_agentes = SorteadorDeAgentesValorant()
        self.message = None
        self.jogadores = jogadores
        self.pagina_atual = pagina_atual

        self.total_paginas = (len(jogadores) + JOGADORES_POR_PAGINA - 1) // JOGADORES_POR_PAGINA
        self._criar_botoes_pagina()

    def criar_callback(self, botao: Button, jogador_id: int):
        async def callback(interaction: Interaction):
            try:
                self.selecionador_jogadores.alternar_selecao(jogador_id)
                if self.selecionador_jogadores.esta_selecionado(jogador_id):
                    botao.style = ButtonStyle.success
                    botao.label = f"✅ {botao.label.strip('✅ ').strip()}"
                else:
                    botao.style = ButtonStyle.grey
                    botao.label = botao.label.strip('✅ ').strip()
                await interaction.response.edit_message(content="", view=self)
            except Exception as ex:
                message = ex.args[0] if ex.args else "Erro inesperado ao alternar seleção."
                logger.error(code=LOG_CODE, message=message, throw=ex)
                await interaction.response.send_message(
                    "Erro ao alternar seleção. Tente novamente ou contate o responsável pelo bot.",
                    ephemeral=True)

        return callback

    def _criar_botoes_pagina(self):
        inicio = self.pagina_atual * JOGADORES_POR_PAGINA
        fim = inicio + JOGADORES_POR_PAGINA
        for jogador in self.jogadores[inicio:fim]:
            if self.selecionador_jogadores.esta_selecionado(jogador.id_role):
                style = ButtonStyle.success
                label = f"✅ {jogador.nome}"
            else:
                style = ButtonStyle.grey
                label = jogador.nome
            botao = Button(label=label, style=style, custom_id=f"jogador_{jogador.id_role}")
            botao.callback = self.criar_callback(botao, jogador.id_role)
            self.add_item(botao)

        botao_sortear = Button(label="Sortear Agentes", style=ButtonStyle.blurple, custom_id="sortear")
        botao_sortear.callback = self.sortear_agentes
        self.add_item(botao_sortear)

        if self.pagina_atual > 0:
            anterior = Button(label="Anterior", style=ButtonStyle.red, custom_id="Anterior")
            anterior.callback = self.pagina_anterior
            self.add_item(anterior)

        if self.pagina_atual < self.total_paginas - 1:
            proximo = Button(label="Próximo", style=ButtonStyle.red, custom_id="Próximo")
            proximo.callback = self.pagina_proxima
            self.add_item(proximo)

    async def pagina_anterior(self, interaction: Interaction):
        if self.pagina_atual == 0:
            return
        nova_view = ViewSelecionaJogadores(
            self.jogadores,
            self.ctx,
            pagina_atual=self.pagina_atual - 1,
            selecionador_jogadores=self.selecionador_jogadores
        )
        nova_view.message = self.message
        await interaction.response.edit_message(content="", view=nova_view)

    async def pagina_proxima(self, interaction: Interaction):
        if self.pagina_atual >= self.total_paginas - 1:
            return
        nova_view = ViewSelecionaJogadores(
            self.jogadores,
            self.ctx,
            pagina_atual=self.pagina_atual + 1,
            selecionador_jogadores=self.selecionador_jogadores
        )
        nova_view.message = self.message
        await interaction.response.edit_message(content="", view=nova_view)

    async def sortear_agentes(self, interaction):
        jogadores_selecionados = self.selecionador_jogadores.obter_selecionados()
        if not jogadores_selecionados:
            await interaction.response.send_message(
                "Selecione pelo menos um jogador antes de sortear os agentes!", ephemeral=True
            )
            return
        try:
            resultado = SorteadorDeAgentesValorant.sortear(jogadores=jogadores_selecionados)
            mensagem = "\n".join(
                f"{jogador.nome} → {agente.nome} ({agente.funcao})" for jogador, agente in resultado.items())
            await interaction.response.send_message(
                f"Sorteio finalizado: \n{mensagem}",
                ephemeral=False
            )
        except ValueError as ex:
            message = ex.args[0] if ex.args else "Erro inesperado ao sortear agentes."
            logger.error(code=LOG_CODE, message=message, throw=ex)
            await interaction.response.send_message(
                "Erro ao sortear agentes. Tente novamente ou contate o responsável pelo bot.",
                ephemeral=True
            )

    async def on_timeout(self):
        await handle_view_timeout(self, self.message)

from discord.ui import View, Button
from discord import ButtonStyle, Interaction

from application.constantes import WAIT_FOR_MESSAGE_TIMEOUT
from domain.services.selecionador_jogadores import SelecionadorJogadores
from domain.services.sorteador_agentes_valorant import SorteadorDeAgentesValorant
from adapter.config.logs.logger_config import ConfigStructureLogger
from utils.discord_view_utils import handle_view_timeout

logger = ConfigStructureLogger()


class ViewSelectorJogadores(View):
    def __init__(self, jogadores, ctx):
        super().__init__(timeout=WAIT_FOR_MESSAGE_TIMEOUT)
        self.ctx = ctx
        self.selecionador = SelecionadorJogadores(jogadores)
        self.message = None

        for jogador in jogadores:
            botao = Button(label=jogador.nome, style=ButtonStyle.secondary, custom_id=str(jogador.id))
            botao.callback = self.criar_callback(botao, jogador.id)
            self.add_item(botao)

        botao_sortear = Button(label="Sortear Agentes", style=ButtonStyle.primary)
        botao_sortear.callback = self.sortear_agentes
        self.add_item(botao_sortear)

    def criar_callback(self, botao: Button, jogador_id: int):
        async def callback(interaction: Interaction):
            try:
                self.selecionador.alternar_selecao(jogador_id)
                if self.selecionador.esta_selecionado(jogador_id):
                    botao.style = ButtonStyle.success
                    botao.label = f"✅ {botao.label.strip('✅ ').strip()}"
                else:
                    botao.style = ButtonStyle.secondary
                    botao.label = botao.label.strip('✅ ').strip()

                texto_selecionados = "Jogadores selecionados:\n"
                if self.selecionador.tem_selecionados():
                    texto_selecionados += "\n".join(
                        f"✅ {j.nome}" for j in self.selecionador.obter_selecionados()
                    )
                else:
                    texto_selecionados = "Nenhum jogador selecionado."

                await interaction.response.edit_message(content="", view=self)

            except Exception as e:
                logger.error(code="erro-selecao-jogador", message="Erro ao alternar seleção", throw=e)
                await interaction.response.send_message("Erro ao atualizar seleção.", ephemeral=True)

        return callback

    async def sortear_agentes(self, interaction: Interaction):
        if not self.selecionador.tem_selecionados():
            await interaction.response.send_message("Selecione pelo menos um jogador.", ephemeral=True)
            logger.warning(code="sortear-sem-jogadores", message="Tentativa de sortear sem jogadores selecionados")
            return

        selecionados = self.selecionador.obter_selecionados()

        resultado = SorteadorDeAgentesValorant().sortear(selecionados)

        texto = "\n".join([f"{j.nome} → {a.nome} ({a.funcao})" for j, a in resultado.items()])
        await interaction.response.send_message(f"Sorteio finalizado:\n{texto}")

    async def on_timeout(self):
        await handle_view_timeout(self, self.message)

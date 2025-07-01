from discord.ui import View, Button
from discord import ButtonStyle, Interaction

from application.constantes import WAIT_FOR_MESSAGE_TIMEOUT
from domain.services.selecionador_jogadores import SelecionadorJogadores
from domain.services.sorteador_agentes_valorant import SorteadorDeAgentesValorant
from adapter.config.logs.config_structure_logger import ConfigStructureLogger
from utils.discord_view_utils import handle_view_timeout

logger = ConfigStructureLogger()
LOG_CODE = "cria-view-selecionador-jogadores"


# TODO "tratar erro quando for mais de 24 jogadores"

class ViewSelecionaJogadores(View):
    def __init__(self, jogadores, ctx):
        super().__init__(timeout=WAIT_FOR_MESSAGE_TIMEOUT)
        self.ctx = ctx
        self.selecionador_jogadores = SelecionadorJogadores(jogadores)
        self.selecionador_agentes = SorteadorDeAgentesValorant()
        self.message = None

        for jogador in jogadores:
            botao = Button(label=jogador.nome, style=ButtonStyle.grey, custom_id=str(jogador.id_role))
            botao.callback = self.criar_callback(botao, jogador.id_role)
            self.add_item(botao)

        botao_sortear = Button(label="Sortear Agentes", style=ButtonStyle.blurple)
        botao_sortear.callback = self.sortear_agentes
        self.add_item(botao_sortear)

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

                texto_selecionados = "Jogadores selecionados:\n"
                if self.selecionador_jogadores.tem_selecionados():
                    texto_selecionados += "\n".join(
                        f"✅ {jogador.nome}" for jogador in self.selecionador_jogadores.obter_selecionados()
                    )

                await interaction.response.edit_message(content="", view=self)

            except Exception as ex:
                message = ex.args[0] if ex.args else "Erro ao alternar seleção."
                logger.error(code=LOG_CODE, message=message, throw=ex)
                await interaction.response.send_message("Erro ao alternar seleção.", ephemeral=True)

        return callback

    async def sortear_agentes(self, interaction: Interaction):
        if not self.selecionador_jogadores.tem_selecionados():
            await interaction.response.send_message("Selecione pelo menos um jogador.", ephemeral=True)
            logger.warning(code=LOG_CODE, message="Tentativa de sortear sem jogadores selecionados")
            return

        selecionados = self.selecionador_jogadores.obter_selecionados()

        resultado = self.selecionador_agentes.sortear(selecionados)

        texto = "\n".join(
            [f"{jogador.nome} → {agente.nome} ({agente.funcao})" for jogador, agente in resultado.items()])
        await interaction.response.send_message(f"Sorteio finalizado:\n{texto}")

    async def on_timeout(self):
        await handle_view_timeout(self, self.message)

import discord
from discord import DiscordException
from discord.ext import commands

from adapter.config.logs.config_structure_logger import ConfigStructureLogger
from discord.ext.commands import Context

from adapter.dataprovider.discord_informacoes import DiscordInformacoes
from application.commands.comandos_bot import ComandosBase
from application.views.view_seleciona_jogadores import ViewSelecionaJogadores

logger = ConfigStructureLogger()
LOG_CODE = "sorteia-agentes-para-jogadores"


class SortearAgentesJogadoresUseCase(ComandosBase):
    def __init__(self, bot: commands.Bot, ctx: Context):
        self.bot = bot
        self.ctx = ctx
        self.discord_informacoes = DiscordInformacoes()

    async def registro_comando(self):
        try:
            canal = self.ctx.channel
            membros = self.discord_informacoes.listar_membros_canal(canal)

            view = ViewSelecionaJogadores(membros, self.ctx)
            message = await self.ctx.send("Selecione os jogadores:", view=view)
            view.message = message
        except DiscordException as ex:
            logger.error(code=LOG_CODE, message="Erro no Discord", throw=ex)
        except discord.Forbidden as ex:
            logger.error(code=LOG_CODE, message="Permissões insuficientes para enviar mensagem no canal atual",
                         throw=ex)
        except Exception as ex:
            logger.error(code=LOG_CODE, message="Erro inesperado", throw=ex)
            raise

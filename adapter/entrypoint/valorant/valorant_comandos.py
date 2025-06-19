from adapter.config.logs.logger_config import ConfigStructureLogger
from adapter.dataprovider.discord_informacoes import DiscordInformacoes
from application.commands.comandos_bot import ComandosBase
from discord.ext import commands
from discord.ext.commands import Context
from application.views.view_selector_jogadores import ViewSelectorJogadores

logger = ConfigStructureLogger()
LOG_CODE = "comando-valorant"


class Valorant(ComandosBase):
    def __init__(self, bot: commands.Bot, ctx: Context):
        self.bot = bot
        self.ctx = ctx

    async def registro_comando(self):
        canal = self.ctx.channel
        membros = DiscordInformacoes.listar_membros_canal(canal)

        view = ViewSelectorJogadores(membros, self.ctx)
        await self.ctx.send("Selecione os jogadores que vão participar:", view=view)

from discord.ext.commands import Context

from adapter.config.bot_config import create_bot
from adapter.config.decoradores import valida_comandos_entrada
from adapter.config.inicializacao_config import config
from adapter.config.logs.config_structure_logger import ConfigStructureLogger
from application.usecase.sortear_agentes_jogadores_usecase import SortearAgentesJogadoresUseCase

LOG_CODE = "executa-comando-iniciar-bot"
bot = create_bot()
logger = ConfigStructureLogger()


@bot.event
async def on_ready() -> None:
    try:
        servidores = ', '.join([guild.name for guild in bot.guilds])
        logger.info(code=LOG_CODE, message=f"Bot iniciado nos servidores: {servidores}")
    except Exception as ex:
        logger.error(code=LOG_CODE, message="Erro ao iniciar o bot", throw=ex)
        raise


@bot.command(name='valorant')
@valida_comandos_entrada
async def valorant(ctx: Context) -> None:
    await SortearAgentesJogadoresUseCase(bot, ctx).registro_comando()


if __name__ == "__main__":
    bot.run(config.TOKEN_BOT)

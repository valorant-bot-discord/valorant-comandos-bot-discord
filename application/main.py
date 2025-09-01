import sys

from discord.ext.commands import Context

from adapter.config.bot_config import create_bot
from adapter.config.decoradores import valida_comandos_entrada
from adapter.config.inicializacao_config import config
from adapter.config.logs.config_structure_logger import ConfigStructureLogger
from application.usecase.sortear_agentes_jogadores_usecase import SortearAgentesJogadoresUseCase
from domain.entity.servidor_discord import servidor_discord

LOG_CODE = "executa-comando-iniciar-bot"
bot = create_bot()
logger = ConfigStructureLogger()


@bot.event
async def on_ready() -> None:
    try:
        payload = [servidor_discord.to_dict(g) for g in bot.guilds]
        logger.info(code=LOG_CODE, message="Iniciando bot com sucesso.", payload=payload)

    except Exception as ex:
        logger.error(code=LOG_CODE, message="Erro ao iniciar o bot", throw=ex)
        raise


@bot.event
async def on_guild_join(guild) -> None:
    try:
        logger.info(code=LOG_CODE, message=f"Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
    except Exception as ex:
        logger.error(code=LOG_CODE, message=f"Erro ao registrar entrada no servidor {guild.name}", throw=ex)


@bot.command(name='valorant')
@valida_comandos_entrada
async def valorant(ctx: Context) -> None:
    await SortearAgentesJogadoresUseCase(bot, ctx).registro_comando()


if __name__ == "__main__":
    try:
        bot.run(config.token_bot)
    except Exception as ex:
        logger.critical(code=LOG_CODE, message="Erro crítico na inicialização", throw=ex)
        sys.exit(1)

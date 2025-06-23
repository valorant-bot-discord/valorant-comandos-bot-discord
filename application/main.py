from discord.ext.commands import Context

from adapter.config.bot_config import create_bot
from adapter.config.inicializacao_config import config
from application.constantes import AUTHORIZED_SERVER_ID
from discord import Message
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


@bot.event
async def on_message(message: Message) -> None:
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    server_id = getattr(message.guild, 'id', None)

    if message.guild and str(server_id) == AUTHORIZED_SERVER_ID:
        await bot.process_commands(message)
    else:
        logger.warning(code=LOG_CODE, message=f"Acesso não autorizado do servidor {server_id}")
        await message.channel.send("Este servidor não tem permissão para usar o bot.")


@bot.command(name='valorant')
async def valorant(ctx: Context) -> None:
    await SortearAgentesJogadoresUseCase(bot, ctx).registro_comando()


if __name__ == "__main__":
    bot.run(config.TOKEN_BOT)

import sys

from discord.ext import commands
from discord.ext.commands import Context

from adapter.config.bot_config import create_bot
from adapter.config.logs.transaction_context import transaction_context
from application.decoradores.valida_comandos_entrada import valida_comandos_entrada
from adapter.config.inicializacao_config import config
from application.usecase.sortear_agentes_jogadores_usecase import SortearAgentesJogadoresUseCase, logger
from domain.entity.servidor_discord import servidor_discord

LOG_CODE = "executa-comando-iniciar-bot"
bot = create_bot()


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


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    transaction_context.start_new()
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return

    transaction_id = transaction_context.get_id()
    error_message = f"Ocorreu um erro inesperado. Para suporte, informe o código: {transaction_id}"
    logger.error(code=LOG_CODE, message=f"Erro no comando de entrada", throw=error)
    await ctx.send(error_message)


@bot.command(name='valorant', aliases=['Valorant', 'VALORANT', 'vava', 'Vava', 'VAVA'])
@valida_comandos_entrada
async def valorant(ctx: Context) -> None:
    await SortearAgentesJogadoresUseCase(bot, ctx).registro_comando()


if __name__ == "__main__":
    try:
        bot.run(config.token_bot)
    except Exception as ex:
        logger.critical(code=LOG_CODE, message="Erro crítico na inicialização", throw=ex)
        sys.exit(1)

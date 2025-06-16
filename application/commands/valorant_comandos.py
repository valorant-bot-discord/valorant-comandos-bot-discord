import asyncio
import random

from adapter.config.bot_config import create_bot
from adapter.config.input_banned import message_forbbiden
from adapter.config.logs.logger_config import ConfigStructureLogger
from adapter.external.valorant.agentes_disponiveis import obter_agentes
from application.constantes import WAIT_FOR_MESSAGE_TIMEOUT
import discord
from discord.ext import commands
from discord.ext.commands import Context

logger = ConfigStructureLogger()
LOG_CODE = "comando-valorant"


class Valorant:
    def __init__(self, bot: commands.Bot, ctx: Context):
        self.bot = bot
        self.ctx = ctx

    async def registro_comando(self):
        logger.info(code=LOG_CODE,
                    message=f"Mensagem recebida de {self.ctx.author} no servidor {self.ctx.guild.name}")

        await self.ctx.send("Por favor, digite os nomes dos jogadores separados por vírgula:")

        def check(message: discord.Message) -> bool:
            return message.author == self.ctx.author and message.channel == self.ctx.channel

        try:
            nomes_msg = await self.bot.wait_for("message", check=check, timeout=WAIT_FOR_MESSAGE_TIMEOUT)
            conteudo = nomes_msg.content.strip()

            nomes = [nome.strip() for nome in conteudo.split(",") if nome.strip()]
            if not nomes:
                await self.ctx.send("Nenhum nome válido fornecido.")
                return

            proibido, mensagem = message_forbbiden(nomes)
            if proibido:
                await self.ctx.send(f"Nome proibido detectado: {mensagem}")
                return

            agentes = obter_agentes()
            max_jogadores = len(agentes)
            if len(nomes) > max_jogadores:
                await self.ctx.send(f"O MM Bot suporta até {max_jogadores} jogadores.")
                return

            agentes_sorteados = random.sample(agentes, len(nomes))
            for nome, agente in zip(nomes, agentes_sorteados):
                await self.ctx.send(f"{nome.title()}: {agente.nome} - {agente.funcao}")

        except asyncio.TimeoutError as ex:
            logger.error(code=LOG_CODE, message=f"Tempo limite excedido", throw=ex)
            await self.ctx.send("Tempo limite excedido. Por favor, tente novamente.")

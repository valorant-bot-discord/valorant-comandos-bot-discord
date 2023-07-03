from config.input_banned import message_forbbiden
from config.bot_config import create_bot
from config.config import BotConfig
from util.agents import agents
from datetime import datetime
import asyncio
import random

config = BotConfig()
bot = create_bot()
agents = agents()



@bot.event
async def on_ready():
    print(f"Entramos como {bot.user} nos servidores {', ' .join([guild.name for guild in bot.guilds])}. Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild and str(message.guild.id) == config.TOKEN_SERVER:
        await bot.process_commands(message)
    else:
        await message.channel.send("Esse servidor não tem permissão para usar o bot.")


@bot.command(name="valorant")
async def valorant(ctx):
    await ctx.send(f"Por favor, digite os nomes dos jogadores separados por vírgula.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        nomes_msg = await bot.wait_for("message", check=check, timeout=60)
        if nomes_msg.content == "!" or nomes_msg.content == "!valorant":
            await ctx.send("Nome inválido.")
            return

        nomes = nomes_msg.content.split(",")
        resultado, mensagem = message_forbbiden(nomes)
        if resultado:
            await ctx.send(mensagem)
            return

        agents_aux = []
        if len(nomes) <= len(agents):
            for nome in nomes:
                agent_name = random.choice(agents)
                while agent_name in agents_aux:
                    agent_name = random.choice(agents)

                agents_aux.append(agent_name)
                await ctx.send(f"{nome.title()}: {agent_name}")
        else:
            await ctx.send(f"MM Bot suporta até {len(agents)} pessoas")

    except asyncio.TimeoutError:
        await ctx.send("Tempo limite excedido. Por favor, tente novamente.")



bot.run(config.TOKEN_BOT)

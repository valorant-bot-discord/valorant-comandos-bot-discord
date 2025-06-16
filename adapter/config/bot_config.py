from discord.ext import commands
import discord


def create_bot():
    intents = discord.Intents.default()
    intents.guilds = True
    bot = commands.Bot("!", intents=intents)
    return bot

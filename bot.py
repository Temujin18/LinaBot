import os
import re

import discord
from discord.ext import commands
from discord.ext.commands.errors import (
    ExtensionAlreadyLoaded,
    ExtensionNotFound,
    ExtensionNotLoaded,
)
from dotenv import load_dotenv

load_dotenv()
token = os.environ["TOKEN"]
prefix = "!"

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Bot is running.")


@bot.command(name="br")
async def broadcast(ctx, message: str):
    for guild in bot.guilds:
        if guild == ctx.guild:
            continue
        for channel in guild.channels:
            if channel.name == "general":
                await channel.send(f"Message: {message} \nFrom: {ctx.guild.name}")


@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} has been loaded.")
    except ExtensionAlreadyLoaded as e:
        await ctx.send(e)
    except ExtensionNotFound as e:
        await ctx.send(e)


@bot.command()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} has been unloaded.")
    except ExtensionNotLoaded as e:
        await ctx.send(e)


bot.run(token)
import os
import re

import discord
from discord.ext import commands
from discord.ext.commands.errors import (
    ExtensionAlreadyLoaded,
    ExtensionNotFound,
)
from dotenv import load_dotenv

load_dotenv()
token = os.environ["TOKEN"]
prefix = "!"

bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Bot is running.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel):  # catch DMs to bot
        await message.channel.send("Thanks for the DM!")
        return
    elif message.content == "raise-exception":
        raise discord.DiscordException

    await bot.process_commands(message)


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
    except ExtensionNotFound as e:
        await ctx.send(e)


bot.run(token)
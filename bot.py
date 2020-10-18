import discord
from dotenv import load_dotenv
from discord.ext import commands
from transformers import TFAutoModelWithLMHead, AutoTokenizer
import os
import re


load_dotenv()
token = os.environ['TOKEN']
prefix = '!'

bot = commands.Bot(command_prefix=prefix)
model = TFAutoModelWithLMHead.from_pretrained("t5-base")
tokenizer = AutoTokenizer.from_pretrained("t5-base")

@bot.event
async def on_ready():
    print('Bot is running.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel): #catch DMs to bot
        await message.channel.send('Thanks for the DM!')
        return
    elif message.content == 'raise-exception':
        raise discord.DiscordException

    await bot.process_commands(message)

@bot.command(name='br')
async def broadcast(ctx, message: str):
    for guild in bot.guilds:
        if guild == ctx.guild:
            continue
        for channel in guild.channels:
            if(channel.name == 'general'):
                await channel.send(f'Message: {message} \nFrom: {ctx.guild.name}')

@bot.command(name='smrz')
async def summarize(ctx):
    hist = await ctx.channel.history(limit=5).flatten()
    messages = [message.content for message in hist if not message.content.startswith(prefix) and message.author != bot.user]
    inputs = tokenizer.encode("summarize: " + ''.join(messages), return_tensors="tf", max_length=512)
    outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs[0])
    await ctx.send(summary)

bot.run(token)
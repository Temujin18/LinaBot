import discord
from discord.ext import commands


class LoveQuiz(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(LoveQuiz(client))
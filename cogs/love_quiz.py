import discord
from discord.ext import commands


class LoveQuiz(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return

        if isinstance(ctx.channel, discord.channel.DMChannel):  # catch DMs to bot
            await ctx.channel.send("Thanks for the DM!")
            return
        elif ctx.content == "raise-exception":
            raise discord.DiscordException

        await self.client.process_commands(ctx)


def setup(client):
    client.add_cog(LoveQuiz(client))
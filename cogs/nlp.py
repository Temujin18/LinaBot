import discord
from discord.ext import commands
from transformers import AutoTokenizer, TFAutoModelWithLMHead

model = TFAutoModelWithLMHead.from_pretrained("t5-base")
tokenizer = AutoTokenizer.from_pretrained("t5-base")


class NLP(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def summarize(self, ctx):
        hist = await ctx.channel.history(limit=5).flatten()
        messages = [
            message.content
            for message in hist
            if not message.content.startswith(prefix) and message.author != client.user
        ]
        inputs = tokenizer.encode(
            "summarize: " + "".join(messages), return_tensors="tf", max_length=512
        )
        outputs = model.generate(
            inputs,
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )
        summary = tokenizer.decode(outputs[0])
        await ctx.send(summary)


def setup(client):
    client.add_cog(NLP(client))
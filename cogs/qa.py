"""
Q&A functions for the discord bot
"""

import discord
from discord.ext import commands
import os


class QA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.env = os.environ

    @commands.command(description="Ask a question for everyone to respond")
    async def question(self, ctx, *, question):
        emb = discord.Embed(
            title=f"New question from {ctx.author}",
            description=question,
            color=discord.Color.blue(),
        )
        chid = int(self.env.get("Q_A_CHANNEL"))
        ch = self.bot.get_channel(chid)
        message = await ch.send(embed=emb)
        thread = await message.create_thread(name="Answers")
        await thread.send(
            embed=discord.Embed(
                title="Answers",
                description="Answer to " + ctx.author.mention,
                color=discord.Color.brand_green(),
            )
        )
        await ctx.send("Succesfully asked the question")


async def setup(bot: commands.Bot):
    await bot.add_cog(QA(bot))

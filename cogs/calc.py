import discord
from discord.ext import commands
from math import *


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calc")
    async def calc(self, ctx, *math):
        mat = " ".join(math)
        to_remove = ["self", '"', "'", "import", "prototype", "proto"]
        print(dir(self))
        for a in to_remove:
            if a in mat:
                print(mat + " : " + str(ctx.author))
                return await ctx.send(
                    f'{ctx.author.mention}, d not use keywoards that may be problematic! The """Operation""" will not solve'
                )
        print(eval(mat))
        await ctx.send(f"Solution of {mat}: {eval(mat)}")


def setup(bot):
    # bot.add_cog(Calculator(bot))
    pass

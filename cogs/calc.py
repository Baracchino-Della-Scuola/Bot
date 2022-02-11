import discord
from discord.ext import commands
from math import *
class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def calc(self, ctx, *math):
        mat = " ".join(math)
        print(eval(mat))
        await ctx.send(f"Solution of {mat}: {eval(mat)}")

def setup(bot):
    bot.add_cog(Calculator(bot))
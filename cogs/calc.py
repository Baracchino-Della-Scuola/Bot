from discord.ext import commands
from math import *
import re
import functools


def get_math(mat):
    """Retrieve results from python"""
    return eval(mat)


class Calculator(commands.Cog):
    """Discord.py cog to make complex math operations."""

    def __init__(self, bot):
        self.bot = bot

    def sanitize(self, mat):
        """Sanitize input with the best-in-class algorithm to prevent abuse"""
        to_remove = ["self", '"', "'", "import", "prototype", "proto"]

        for a in to_remove:
            if a in mat:
                return False
        if re.match(r'[__builtins__]+', mat):
            return False
        return True

    @commands.command(name="calc")
    async def calc(self, ctx, *math):
        mat = " ".join(math)

        if not self.sanitize(mat):
            return await ctx.send(f'{ctx.author.mention}, do not use keywoards that may be problematic! The """Operation""" will not solve')

        executor = functools.partial(get_math, mat)
        # This avoids blocking long functions which usually causes crashing
        res = await self.bot.loop.run_in_executor(None, executor)
        await ctx.send(f"Solution of {mat}: {res}")


def setup(bot):
    bot.add_cog(Calculator(bot))
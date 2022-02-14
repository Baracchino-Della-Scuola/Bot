import discord
from discord.ext import commands
import random
import hashlib
from string import *


class Api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="api")
    async def apikey(self, ctx):
        c = await self.bot.connection.cursor()
        await c.execute(f"SELECT * from apikeys WHERE user = {ctx.author.id}")
        r = await c.fetchall()
        if len(r) == 0:
            chars = ""
            for a in range(12):
                chars += f"{random.choice(ascii_uppercase+ascii_lowercase+'0123456789'+'!£$%/=')}"
            string = f"{ctx.author.name}-{ctx.author.id}-{chars}"
            byts = string.encode()
            encoded = hashlib.sha256(byts).hexdigest()
            await ctx.author.send(encoded)
            await c.execute(
                f"INSERT into apikeys VALUES ('{ctx.author.id}', '{encoded}')"
            )
            return
        await ctx.author.send(r[0][1])


def setup(bot):
    bot.add_cog(Api(bot))

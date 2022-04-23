import discord
from discord.ext import commands
import aiohttp
from typing import Union

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def lyrics(self, ctx, song:Union[str, discord.User]):
        ses = aiohttp.ClientSession()
        song = song.replace(' ', '%20')
        async with ses.get("https://some-random-api.ml/lyrics?title={}".format(song)) as r:
            data = await r.json()
        await ses.close()
        try:
            if data["error"]:
                return await ctx.send("No lyrics found for {}".format(song))
        except:    pass
        
        emb = discord.Embed(title=f"Lyrics for {data['title']} by {data['author']}", description=data['lyrics'], color=0x00ff00)
        emb.set_thumbnail(url=data['thumbnail']['genius'])
        await ctx.send(embed=emb)

async def setup(bot):
    await bot.add_cog(Lyrics(bot))
        
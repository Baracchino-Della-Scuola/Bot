import discord 
from discord.ext import commands
from io import *
import requests
from typing import *
from petpetgif import petpet as petpetgif
import aiohttp, random
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pat")
    async def pet(self, ctx, image: discord.Member=None):
        
        if type(image) == discord.member.Member:
            image = await image.avatar.read() # retrieve the image bytes
        else:
            image = await ctx.author.avatar.read()

        source = BytesIO(image) # file-like container to hold the emoji in memory
        dest = BytesIO() # container to store the petpet gif in memory
        petpetgif.make(source, dest)
        dest.seek(0) # set the file pointer back to the beginning so it doesn't upload a blank file.
        await ctx.send(file=discord.File(dest, filename=f"{image[0]}-petpet.gif"))
    @commands.command()
    async def passed(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://some-random-api.ml/canvas/passed?avatar=" + user.avatar.url)
        else:
            r = requests.get("https://some-random-api.ml/canvas/passed?avatar=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="passed.png"))
    

    @commands.command()
    async def comunism(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://some-random-api.ml/canvas/comrade?avatar=" + user.avatar.url)
        else:
            r = requests.get("https://some-random-api.ml/canvas/comrade?avatar=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="comunism.png"))
    
    @commands.command()
    async def jail(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://some-random-api.ml/canvas/jail?avatar=" + user.avatar.url)
        else:
            r = requests.get("https://some-random-api.ml/canvas/jail?avatar=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="jail.png"))
    @commands.command()
    async def rip(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://vacefron.nl/api/grave?user=" + user.avatar.url)
        else:
            r = requests.get("https://vacefron.nl/api/grave?user=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="rip.png"))
    
    @commands.command()
    async def emergency(self, ctx, text):
        

        r = requests.get("https://vacefron.nl/api/emergencymeeting?text=" + text.replace(" ", "%20"))
       
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="emergency.png"))
    @commands.command(aliases=["porn"])
    async def nsfw(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send("You cant ask me this in a non-NSFW channel!")
            return
        embed = discord.Embed(title="🔥 | Hot ", description="🌶️ | Want some *high quality content*?", color=discord.Color.blue())
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
            await cs.close()
    
    @commands.command()
    async def gay(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://some-random-api.ml/canvas/gay?avatar=" + user.avatar.url)
        else:
            r = requests.get("https://some-random-api.ml/canvas/gay?avatar=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="lgbtqpro+.png"))
    
    
    
    @commands.command()
    async def wasted(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://some-random-api.ml/canvas/wasted?avatar=" + user.avatar.url)
        else:
            r = requests.get("https://some-random-api.ml/canvas/wasted?avatar=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="wasted.png"))
    
    
    @commands.command()
    async def triggered(self, ctx, user:discord.User=None):
        if user:

            r = requests.get("https://some-random-api.ml/canvas/triggered?avatar=" + user.avatar.url)
        else:
            r = requests.get("https://some-random-api.ml/canvas/triggered?avatar=" + ctx.author.avatar.url)
        
        file_obj = BytesIO(r.content)
        await ctx.send(file=discord.File(fp=file_obj, filename="triggered.gif"))



def setup(bot):
    bot.add_cog(Misc(bot))
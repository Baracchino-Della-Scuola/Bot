import discord
from discord.ext import commands
import json


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.con = bot.connection

    @commands.group(
        name="tag",
        aliases=["t", "tags"],
        invoke_without_command=True,
        description="List tags",
    )
    async def tag(self, ctx, name=None):

        cur = await self.con.cursor()
        
        tags = ""
        if name is None:
            await cur.execute("SELECT * from tags")
            data = await cur.fetchall()
            for a in data:
                print(a)
                tags += "**" + a[0] + "**: " + "\n"
            emb = discord.Embed(
                title="Tags", description=tags, color=discord.Color.brand_green()
            )
            await ctx.send(embed=emb)
        else:
            print("OOOOF")
            await cur.execute(f"SELECT * from tags WHERE name = '{name}'")
            data = await cur.fetchall()
            for a in data:
                
                
                emb = discord.Embed(
                        title=f"Tag {name}",
                        description=a[1],
                        color=discord.Color.brand_green(),
                )
                await ctx.send(embed=emb)
                return

    @tag.command(name="add", aliases=["create"], description="Create a tag")
    async def add(self, ctx, name, *, content):
        cur = await self.bot.connection.cursor()
        await cur.execute(f"INSERT into tags VALUES ('{name}', '{content}')")
        await ctx.send(f"Tag {name} has been created.")

def setup(bot):
    bot.add_cog(Tags(bot))

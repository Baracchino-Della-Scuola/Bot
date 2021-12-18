import discord
from discord.ext import commands
import json

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="tag", aliases=["t", "tags"], invoke_without_command=True)
    async def tag(self, ctx, name=None):
        

        file = open("data/tags.json", "r")
        data = json.load(file)
        file.close()
        tags = ""
        if name is None:
            for a in data:
                print(a)
                tags += "[" + a[2] +"] **" + a[0] + "**: " + "\n"
            emb = discord.Embed(title="Tags", description=tags, color=discord.Color.brand_green())
            await ctx.send(embed=emb)
        else:
            for a in data:
                if a[0] == name:
                    emb = discord.Embed(title=f"Tag {name}", description=a[1], color=discord.Color.brand_green())
                    await ctx.send(embed=emb)
                    return

        

    @tag.command(name="add", aliases=["create"])
    async def add(self, ctx, name, *, content):
        f = open("data/tags.json", "r")
        data = json.load(f)
        f.close()
        f = open("data/tags.json", "w")
        data.append([name, content, ctx.author.mention, f"{ctx.author.id}"])
        f.write(json.dumps(data))
        f.close()
        await ctx.send(f"Tag {name} has been created.")
    
    @tag.command(name="delete", aliases=["remove"])
    async def delete(self, ctx, name):
        f = open("data/tags.json", "r")
        data = json.load(f)
        f.close()
        f = open("data/tags.json", "w")
        for a in data:
            if a[0] == name:
                if not a[3] == f"{ctx.author.id}":
                    if not self.bot.get_user(a[3]) in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:
                        return await ctx.send("You can't delete a tag you didn't create.")
                    return await ctx.send("You can't delete a tag you didn't create.")
                data.remove(a)
        f.write(json.dumps(data))
        f.write("[]")
        f.close()
        await ctx.send(f"Tag {name} has been deleted.")

def setup(bot):
    bot.add_cog(Tags(bot))

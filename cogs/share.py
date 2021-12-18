import discord
from discord.ext import commands
import requests, os
import urllib.request
import subprocess



class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff_chat = self.bot.get_channel(907937553343209472)
    
    @commands.command(name="purge")
    async def purge_all(self, ctx):
        if ctx.author in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:
            for a in os.listdir("files"):
                os.remove("files/" + a)
                await ctx.send("Deleted " + a)
            await ctx.send("All files have been deleted from the system.")
            await self.staff_chat.send(f"{ctx.author.mention} has deleted all files from the system.")
        else:
            await ctx.send("You do not have permission to use this command.")
            return

    @commands.command(name="share")
    async def share(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.send("Please attach a file to share.")
            return
        
        file = ctx.message.attachments[0]
        f = open(f"files/{file.filename}", "wb")
        res = requests.get(file.url)
        f.write(res.content)
        f.close()

        await ctx.send(f"File {file.filename} has been saved in our database!")
        c = self.bot.get_channel(int(838728591238758411))
        await c.send(f"{ctx.author.mention} has shared a file: {file.filename}. Do `.download {file.filename}` to download it.")


        await self.staff_chat.send(f"{ctx.author.mention} has shared a file: {file.filename}.")
    
    @commands.command(name="download")
    async def download(self, ctx, filename):
        if not os.path.isfile(f"files/{filename}"):
            await ctx.send("File not found.")
            return
        

        await ctx.author.send(f"Here is your **{filename}**:", file=discord.File(f"files/{filename}"))
        await self.staff_chat.send(f"{ctx.author.mention} has downloaded **{filename}**.")
        await ctx.send("File sent in DMs!")
    
    @commands.command(name="list")
    async def list(self, ctx):
        files = os.listdir("./files")
        await ctx.send(f"Files stored with us: {', '.join(files)}")
    
    @commands.command(name="staff")
    async def staff(self, ctx):
        desc = "Here is a list of staff members:\n"
        for member in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:

            desc += f"{member.mention}\n"
        emb = discord.Embed(title="Staff", description=desc)
        await ctx.send(embed=emb)
    
    @commands.command()
    async def delete(self, ctx, filename):
        await ctx.defer(complete_hidden=True)
        if not ctx.author in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:
            await ctx.send('You are not a staff member of "Il Baracchino Della Scuola".')
            return
        if not os.path.isfile(f"files/{filename}"):
            await ctx.send("File not found.")
            return
        
        c = self.bot.get_channel(int(838728591238758411))

        

        os.remove(f"files/{filename}")
        await ctx.send(f"File {filename} has been deleted.")
        await c.send(f"File {filename} no longer exists. Say thanks to {ctx.author.mention}!")
        await self.staff_chat.send(f"{ctx.author.mention} has deleted a file: {filename}.")
    
    @commands.command(name="presence")
    async def presence(self, ctx, *, text):
        if not ctx.author in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:
            await ctx.send('You are not a staff member of "Il Baracchino Della Scuola".')
            return
        #await self.staff_chat.send(f"{ctx.author.mention} has changed the bot's presence to: {text}.")
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.send("Presence changed to "+text+'.')
    
    @commands.command()
    async def restart(self, ctx):
        if not ctx.author in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:
            await ctx.send('You are not a staff member of "Il Baracchino Della Scuola".')
            return
        await ctx.send("Restarting...")
        await self.staff_chat.send(f"{ctx.author.mention} has restarted the bot.")
        subprocess.call("python3 main.py", shell=True)
        self.bot.close()
    @commands.command(name="rename")
    async def rename(self, ctx, filename, newname):
        if not ctx.author in self.bot.get_guild(838727867428765766).get_role(884453174839230464).members:
            await ctx.send('You are not a staff member of "Il Baracchino Della Scuola".')
            return
        if not os.path.isfile(f"files/{filename}"):
            await ctx.send("File not found.")
            return
        
        c = self.bot.get_channel(int(838728591238758411))


        

        os.rename(f"files/{filename}", f"files/{newname}")
        await c.send(f"Now you can download {filename} with .download {newname}")
        await ctx.send(f"File {filename} has been renamed to {newname}.")
        await self.c.send(f"{ctx.author.mention} renamed {filename} to {newname}.")
        
        

def setup(bot):
    bot.add_cog(Share(bot))
        

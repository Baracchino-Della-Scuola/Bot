import discord
from discord.ext import commands
import requests, os
import json
import subprocess
import random
import dotenv


class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff_chat = self.bot.get_channel(int(os.environ["STAFF_CHAT"]))
        dotenv.load_dotenv(".env")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.db = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.connection = bot.connection

        self.conection = None

    @commands.command()
    async def settings(self, ctx, key, value):
        f = open("settings.json", "r")
        jsonf = json.loads(f.read())
        f.close()
        jsonf[key] = value
        f = open("settings.json", "w")
        f.write(json.dumps(jsonf))
        await ctx.send("updated settings")

    @commands.command(
        name="share",
        alias=["send", "sendfile", "sendfiles", "upload", "uploadfile"],
        description="Upload a file",
    )
    async def share(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.send("Please attach a file to share.")
            return

        file = ctx.message.attachments[0]
        c = self.bot.get_channel(int(838728591238758411))

        f = open("data/files/" + file.filename, "wb")
        r = requests.get(file.url)
        f.write(r.content)
        f.close()

        await ctx.send(f"File {file.filename} has been saved in our database!")

        await self.staff_chat.send(
            f"{ctx.author.mention} has shared a file: {file.filename}."
        )

    @commands.command(
        name="download",
        alias=["get", "getfile", "getfiles"],
        description="Download a file",
    )
    async def download(self, ctx, filename):
        if os.path.exists("data/files/" + filename):
            await ctx.author.send(file=discord.File("data/files/" + filename))

        else:
            await ctx.send("File not found. Try with a different file")
            await self.staff_chat.send(
                f"{ctx.author.mention} has attempted to download a file that does not exist."
            )
            return
        await self.staff_chat.send(
            f"{ctx.author.mention} has downloaded **{filename}**."
        )
        await ctx.send("File sent in DMs!")

    @commands.command()
    async def randomize(self, ctx, presence: int = None):
        if presence:
            await self.bot.change_presence(
                activity=discord.Game(
                    name=[
                        "Copyrush 2022",
                        "Games at school",
                        "Destroy the school",
                        "Fake the test",
                        "CopyRush 2022 at school",
                        "Copyrush 2022 in DAD",
                        "#LaScuolaèDAD",
                        "#DADistheway",
                        "DAD > *",
                        "Mario Kart con i banchi a rotelle",
                    ][presence]
                )
            )
            return await ctx.send(":white_check_mark:")

        await ctx.send(":white_check_mark:")
        await self.bot.change_presence(
            activity=discord.Game(
                name=random.choice(
                    [
                        "Copyrush 2022",
                        "Games at school",
                        "Destroy the school",
                        "Fake the test",
                        "CopyRush 2022 at school",
                        "Copyrush 2022 in DAD",
                        "#LaScuolaèDAD",
                        "#DADistheway",
                        "DAD > *",
                        "Mario Kart con i banchi a rotelle",
                    ]
                )
            )
        )

    @commands.command(
        name="list",
        alias=["listfiles", "getfiles"],
        description="List all files stored with us",
    )
    async def list(self, ctx):
        total = "\n".join(os.listdir("data/files/"))
        emb = discord.Embed(
            title="Files", description=total, color=discord.Color.blue()
        )
        await ctx.send(embed=emb)

    @commands.command(name="staff", alias=["team", "staffteam"])
    async def staff(self, ctx):
        desc = "Here is a list of staff members:\n"
        for member in (
            self.bot.get_guild(838727867428765766).get_role(884453174839230464).members
        ):
            desc += f"{member.mention}\n"
        emb = discord.Embed(title="Staff", description=desc)
        await ctx.send(embed=emb)

    @commands.command(alias=["del", "remove", "rm"], descriiption="Delete a file")
    async def delete(self, ctx, filename):
        # await ctx.defer(complete_hidden=True)
        if (
            not ctx.author
            in self.bot.get_guild(838727867428765766)
            .get_role(884453174839230464)
            .members
        ):
            await ctx.send(
                'You are not a staff member of "Il Baracchino Della Scuola".'
            )
            return

        c = self.bot.get_channel(int(838728591238758411))

        os.remove("data/files/" + filename)
        await c.send(
            f"File {filename} no longer exists. Say thanks to {ctx.author.mention}!"
        )
        await self.staff_chat.send(
            f"{ctx.author.mention} has deleted a file: {filename}."
        )

    @commands.command(
        name="presence", alias=["status"], description="Change the bot's presence"
    )
    async def presence(self, ctx, *, text):
        if (
            not ctx.author
            in self.bot.get_guild(838727867428765766)
            .get_role(884453174839230464)
            .members
        ):
            await ctx.send(
                'You are not a staff member of "Il Baracchino Della Scuola".'
            )
            return
        await self.staff_chat.send(
            f"{ctx.author.mention} has changed the bot's presence to: {text}."
        )
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.send("Presence changed to " + text + ".")

    @commands.command(alias=["reboot"], description="Reboot the bot")
    async def restart(self, ctx):
        if (
            not ctx.author
            in self.bot.get_guild(838727867428765766)
            .get_role(884453174839230464)
            .members
        ):
            await ctx.send(
                'You are not a staff member of "Il Baracchino Della Scuola".'
            )
            return
        await ctx.send("Restarting...")
        await self.staff_chat.send(f"{ctx.author.mention} has restarted the bot.")
        subprocess.call("python3 main.py", shell=True)
        self.bot.close()

    @commands.command(name="rename", alias=["ren"], description="Rename a file")
    async def rename(self, ctx, filename, newname):
        if (
            not ctx.author
            in self.bot.get_guild(838727867428765766)
            .get_role(884453174839230464)
            .members
        ):
            await ctx.send(
                'You are not a staff member of "Il Baracchino Della Scuola".'
            )
            return

        c = self.bot.get_channel(int(838728591238758411))

        os.rename("data/files/" + filename, "data/files/" + newname)
        await c.send(f"Now you can download {filename} with .download {newname}")
        await ctx.send(f"File {filename} has been renamed to {newname}.")
        await c.send(f"{ctx.author.mention} renamed {filename} to {newname}.")


async def setup(bot):
    await bot.add_cog(Share(bot))

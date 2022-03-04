import discord
from discord.ext import commands
import time, json, os
from datetime import datetime
from discord.utils import utcnow
from datetime import timedelta


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        f = open("settings.json")
        self.settings = json.load(f)
        f.close()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        try:
            await user.send(
                f"😢 | You have been kicked from {ctx.guild.name} for reason {reason}"
            )
        except:
            pass
        ch = self.bot.get_channel(int(os.environ["STAFF_CHAT"]))
        await ch.send(f"{user} has been kicked with reason {reason}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, user: discord.Member, *, args):
        reason = "Muted by " + ctx.author.name
        data = args.split(" ")
        print(args)
        minutes = 0
        seconds = 0
        hours = 0
        days = 0

        print(data)
        for a in data:

            if a.endswith("m"):
                minutes = int(a[:-1])
            if a.endswith("s"):
                seconds = int(a[:-1])
            if a.endswith("d"):
                days = int(a[:-1])
            if a.endswith("h"):
                hours = int(a[:-1])

        timeout_until = utcnow() + timedelta(
            minutes=minutes, seconds=seconds, days=days, hours=hours
        )
        await user.edit(timeout_until=timeout_until)
        await user.send(
            f"U have been muted for {days} days {hours} hours {minutes} minutes {seconds} seconds"
        )
        await ctx.send(f"{user.mention} muted!")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, user: discord.Member):
        await user.edit(timeout_until=None)
        await ctx.send(f"{user} unmuted.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        try:
            await user.send(
                f"😢 | You have been banned from {ctx.guild.name} for reason {reason}"
            )
        except:
            pass
        ch = self.bot.get_channel(int(os.environ["STAFF_CHAT"]))
        await ch.send(f"{user} has been banned with reason {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.User, *reason):
        cur = await self.bot.connection.cursor()
        print(reason)
        await cur.execute(
            f"INSERT into warns (user, reason, moderator) VALUES ('{user.id}', '{' '.join(list(reason))}', '{ctx.author.id}')"
        )
        await ctx.send("I warned " + str(user))

    @commands.command()
    async def warnings(self, ctx, user: discord.User):
        cur = await self.bot.connection.cursor()
        await cur.execute(f"SELECT * from warns WHERE user = '{user.id}'")
        r = await cur.fetchall()
        warns = ""
        for a in r:
            warns += (
                f"Warned by {self.bot.get_user(int(a[2])).mention}. Reason: {a[1]}\n"
            )
        emb = discord.Embed(
            title=f"{user}'s infractions",
            description=warns,
            color=discord.Color.green(),
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def purge(self, ctx, limit: int = 2):

        await ctx.channel.purge(limit=limit + 1)
        time.sleep(1)
        await ctx.send(f"Deleted {limit} messages", delete_after=2)


def setup(bot):
    bot.add_cog(Moderation(bot))

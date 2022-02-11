import discord
from discord.ext import commands
import time, json, os


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

import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *args):
        args = list(args)
        print(args)
        question = args[0]
        numbers = [
            "regional_indicator_a",
            "regional_indicator_b",
            "regional_indicator_c",
            "regional_indicator_d",
            "regional_indicator_e",
            "regional_indicator_f",
            "regional_indicator_g",
            "regional_indicator_h",
            "regional_indicator_i",
        ]
        reacts = [
            "\U0001f1e6",
            "\U0001f1e7",
            "\U0001f1e8",
            "\U0001f1e9",
            "\U0001f1ea",
            "\U0001f1eb",
            "\U0001f1ec",
            "\U0001f1ed",
            "\U0001f1ee",
        ]
        emb = discord.Embed(
            title=f"Poll by {ctx.author}",
            description=question,
            color=discord.Color.green(),
        )

        if len(args) > 1:
            quests = args
            del quests[0]
            print(quests)
            if len(quests) > 9:
                return await ctx.send("You added too much choices! Bruh...")
            for a, item in enumerate(quests):
                emb.add_field(name="Choice", value=f":{numbers[a]}: : {item}")
        else:
            quests = [1, 2]
            reacts = ["\U0001f44d", "\U0001f44e"]

        m = await ctx.send(embed=emb)

        for a in range(len(quests)):
            await m.add_reaction(reacts[a])


async def setup(bot):
    await bot.add_cog(Poll(bot))

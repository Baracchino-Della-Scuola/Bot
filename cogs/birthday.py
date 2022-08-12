import discord
import requests, os
from discord.ext import commands
from datetime import datetime


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://discord.com/api/v9/"
        self.bot_token = os.environ.get("token")
        print(os.environ)
        print(os.environ.get("token"))

    @commands.command()
    async def birthday(self, ctx):
        questions = ["When is your birthday? (MM-DD)", "Are you sure? [Y/n]"]
        answers = []
        for a in questions:
            await ctx.send(a)

            def check(m):
                return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

            quest = await self.bot.wait_for("message", check=check)
            answers.append(quest.content)

        year_current = int(datetime.now().strftime("%Y"))
        year_next = year_current + 1
        month_current = int(datetime.now().strftime("%m"))
        day_current = int(datetime.now().strftime("%d"))
        print(month_current)
        print(day_current)
        dates = answers[0].split("-")
        dates[0] = int(dates[0])
        dates[1] = int(dates[1])

        def month():
            if month_current > dates[0]:
                print(1)
                return year_next
            if month_current == dates[0]:
                print(2)
                if day_current >= dates[1]:
                    print(3)
                    return year_next

            return year_current

        date = f"{month()}-" + answers[0] + "T00:00:00+0000"

        print(dates)
        valid = ""
        json_data = {
            "channel_id": "838727867428765770",
            "name": f"Compleanno di {ctx.author.name}",
            "privacy_level": "2",
            "entity_type": "2",
            "scheduled_start_time": date,
        }
        r = requests.post(
            self.api_url + f"/guilds/{ctx.guild.id}/scheduled-events",
            json=json_data,
            headers={"Authorization": "Bot " + self.bot_token},
        )
        print(r.text)


async def setup(bot):
    await bot.add_cog(Birthdays(bot))

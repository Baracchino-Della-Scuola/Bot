import discord, os
from discord.ext import commands
import traceback
import dotenv
import sys

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all())

    for a in os.listdir("./cogs"):
        if a.endswith(".py"):
            try:
                self.load_extension(f"cogs.{a[:-3]}")
                print("Loaded "+a)
            except:
                traceback.print_exc()

    async def on_ready(self):
        print(f"I logged in as {bot.user.tag}")

dotenv.load_dotenv(dotenv_path=".env")
if len(sys.args >= 3):
    token = sys.args[2]
else:
    token = None
bot.run(token or os.environ["token"])
import discord, urllib, jishaku, os, traceback, dotenv
from discord.ext import commands
import random
dotenv.load_dotenv(dotenv_path=".env")
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all(), slash_commands=True)
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):

                print("Trying to load " + cog)
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                    print("Loaded " + cog)
                except Exception as e:
                    print(f"Failed to load {cog}")
                    traceback.print_exc()
        self.load_extension("jishaku")

        
        
        
    async def on_ready(self):
        
        print("Bot is ready!")
        c = self.get_channel(907937553343209472)
        await c.send("Bot launched! Now you can start copying")
        await self.change_presence(activity=discord.Game(name=random.choice(["Copy rush 2021", "Games at school", "Destroy the school", "Fake the test", "Copy Rush 2021 at school"])))


Bot().run(os.environ["token"])
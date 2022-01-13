import discord, urllib, jishaku, os, traceback, dotenv
from discord.ext import commands
import random
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.


dotenv.load_dotenv(dotenv_path=".env")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".", intents=discord.Intents.all(), slash_commands=True
        )

        self.load_extension("jishaku")
        menu = DefaultMenu(
            page_left="\U000025c0",
            page_right="\U000025b6",
            remove="\U0001f6d1",
            active_time=500,
        )

        # Custom ending note
        ending_note = f"(C) 2021 Il BaracchinoDella Scuola"

        self.help_command = PrettyHelp(menu=menu, ending_note=ending_note)

    async def on_ready(self):
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):

                print("Trying to load " + cog)
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                    print("Loaded " + cog)
                except Exception as e:
                    print(f"Failed to load {cog}")
                    traceback.print_exc()

        print("Bot is ready!")
        c = self.get_channel(907937553343209472)
        await c.send("Bot launched! Now you can start copying")
        await self.change_presence(
            activity=discord.Game(
                name=random.choice(
                    [
                        "Copy rush 2021",
                        "Games at school",
                        "Destroy the school",
                        "Fake the test",
                        "Copy Rush 2021 at school",
                    ]
                )
            )
        )


Bot().run(os.environ["token"])

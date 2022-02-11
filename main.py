import discord, urllib, jishaku, os, traceback, dotenv
from discord.ext import commands
import random
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp
import asyncio
import aiomysql


dotenv.load_dotenv(dotenv_path=".env")


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True
        super().__init__(
            command_prefix=os.environ.get("PREFIX"),
            intents=intents,
            slash_commands=True,
        )

        # Custom ending note
        ending_note = f"(C) 2022 Il BaracchinoDella Scuola"

    async def on_ready(self):
        print("Running. Printing wd")
        os.system("pwd")
        self.staff_chat = self.get_channel(907937553343209472)
        dotenv.load_dotenv(".env")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.db = os.getenv("DB_NAME")
        self.user_name = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.connection = await aiomysql.connect(
            autocommit=True,
            host=self.host,
            port=int(self.port),
            db=self.db,
            user=self.user_name,
            password=self.password,
        )
        print("Connected to MySQL")

        self.load_extension("jishaku")
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
                        "Copy rush 2022",
                        "Games at school",
                        "Destroy the school",
                        "Fake the test",
                        "Copy Rush 2022 at school",
                        "Copy rush 2022 in DAD",
                        "#LaScuolaèDAD",
                        "#DADistheway",
                        "DAD > *",
                        "mario kart sui banchi a rotelle" "scuola in presenza < *",
                    ]
                )
            )
        )


Bot().run(os.environ["token"])

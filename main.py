import discord
import urllib
import jishaku
import os
import traceback
import dotenv
from discord.ext import commands
import random

import asyncio
import aiomysql
import psutil
import subprocess

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
        try:
            self.connection = await aiomysql.connect(
                autocommit=True,
                host=self.host,
                port=int(self.port),
                db=self.db,
                user=self.user_name,
                password=self.password,
            )
            print("Connected to MySQL")
        except:
            print("No sql for you, sorry")

        for a in os.listdir("./cogs"):

            try:
                if a.endswith(".py"):

                    await self.load_extension("cogs." + a[:-3])
                    print(f"Loading {a[:-3]}.py")

            except Exception as e:
                print(f"Unable to load {a}\n{e}")
                print(traceback.format_exc())

        await self.load_extension("jishaku")

        print("Bot is ready!")

        c = self.get_channel(907937553343209472)
        await c.send("Bot launched! Now you can start copying")
        await self.change_presence(
            activity=discord.Game(
                name=random.choice(
                    [
                        "CopyRush 2022",
                        "Games at school",
                        "Destroy the school",
                        "Fake the test",
                        "CopyRush 2022 at school",
                        "CopyRush 2022 in DAD",
                        "#LaScuolaèDAD",
                        "#DADistheway",
                        "DAD > *",
                        "mario kart sui banchi a rotelle",
                        "scuola in presenza < *",
                        "hacking the school",
                        "listening to music at school",
                    ]
                )
            )
        )


Bot().run(os.environ["token"])

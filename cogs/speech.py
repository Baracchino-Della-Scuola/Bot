import speech_recognition as sr
import discord
from discord.ext import commands
from io import BytesIO
import aiohttp
import traceback
from aiogtts import aiogTTS
import functools
from tempfile import TemporaryFile
import io

r = sr.Recognizer()


class Speech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tts = aiogTTS()

    async def to_bytes(self, url):
        async with bot.session.get(url) as r:
            res = await r.read()
            return res

    async def to_text(self, file):
        blocking = functools.partial(self.to_text_, file)
        res = await self.bot.loop.run_in_executor(None, blocking)
        return res

    @commands.command(aliases=["tts"])
    async def text_to_speech(self, ctx, *, message):
        "Transform a text to a speech!"

        temp = TemporaryFile()
        await self.tts.write_to_fp(fp=temp, text=message, lang="it")
        temp.seek(0)
        f = discord.File(fp=io.BytesIO(temp.read()), filename="tts.mp3")
        await ctx.send(ctx.author.mention, file=f)


def setup(bot):
    bot.add_cog(Speech(bot))

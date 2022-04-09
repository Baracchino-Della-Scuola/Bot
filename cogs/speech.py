import discord
from discord.ext import commands
from io import BytesIO
import aiohttp
import traceback
from aiogtts import aiogTTS
import functools
from tempfile import TemporaryFile
import io
import asyncio


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

    @commands.command()
    async def saytts(self, ctx, *, text):
        temp = BytesIO()

        tts = await self.tts.save(text, "tts.mp3", lang="it")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(voice_channel)
        else:
            vc = await voice_channel.connect()
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=guild
        )

        # ctx.voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)
        ffmpeg_options = {"options": "-vn"}
        if not voice_client.is_playing():
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio("tts.mp3", **ffmpeg_options)
            )

            voice_client.play(
                source, after=lambda e: print("Player error: %s" % e) if e else None
            )
            while vc.is_playing():
                await asyncio.sleep(0.1)
            await vc.disconnect()


async def setup(bot):
    await bot.add_cog(Speech(bot))

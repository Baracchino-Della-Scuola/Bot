import discord
from discord.ext import commands, tasks


class Dance(commands.Cog):
    @tasks.loop(seconds=1)
    async def dance_loop(voice_client, query):
        if voice_client.is_connected():
            if not voice_client.is_playing():
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                voice_client.play(
                    source, after=lambda e: print("Player error: %s" % e) if e else None
                )
        else:
            dance_loop.stop()

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def djoin(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel where I can DANCE"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def dance(self, ctx):
        """DANCE DANCE DANCE"""

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.bot.voices[str(ctx.guild.id)] = ctx.author.id
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_connected():
            try:
                user_id = self.bot.voices[str(ctx.guild.id)]
                user = ctx.guild.get_member(user_id)
                if user.id != ctx.author.id:
                    emb = discord.Embed(
                        description=f"You are not the party dj! {user.mention} is!",
                        colour=discord.Colour.red(),
                    )
                    await ctx.send(embed=emb)
                else:
                    ctx.voice_client.stop()
            except KeyError:
                self.bot.voices[str(ctx.guild.id)] = ctx.author.id
                ctx.voice_client.stop()

        query = "tts"

        if not ".mp3" in query:
            query += ".mp3"

        v = ctx.voice_client

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        v.play(source, after=lambda e: print("Player error: %s" % e) if e else None)

        emb = discord.Embed(colour=discord.Colour.blurple(), title="DANCE DANCE DANCE")
        await ctx.send(embed=emb)

        self.dance_loop.start(v, query)

    @commands.command()
    async def dvolume(self, ctx, volume: int):
        """Changes the DANCE's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100

        emb = discord.Embed(
            description="Changed volume to `{}%`".format(volume),
            colour=discord.Colour.blurple(),
        )
        await ctx.send(embed=emb)

    @commands.command()
    async def dstop(self, ctx):
        """Stop dancing"""

        if ctx.voice_client is None:
            emb = discord.Embed(
                description="I'm not dancing!", colour=discord.Colour.red()
            )
            await ctx.send(embed=emb)
        elif ctx.voice_client.is_playing():
            try:
                user_id = self.bot.voices[str(ctx.guild.id)]
                user = ctx.guild.get_member(user_id)
                if user.id != ctx.author.id:
                    emb = discord.Embed(
                        description=f"You are not the party dj! {user.mention} is!",
                        colour=discord.Colour.red(),
                    )
                    return await ctx.send(embed=emb)
                else:
                    ctx.voice_client.stop()
                    self.bot.voices.pop(str(ctx.guild.id))
            except KeyError:
                ctx.voice_client.stop()

        await ctx.voice_client.disconnect()

        emb = discord.Embed(
            description="no more dance", colour=discord.Colour.blurple()
        )
        await ctx.send(embed=emb)


async def setup(bot):
    await bot.add_cog(Dance(bot))

import discord
from discord.ext import commands
import json
from discord.utils import get
from datetime import datetime


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.emoji.name)
        user = self.bot.get_user(payload.user_id)
        guild = self.bot.get_guild(payload.guild_id)
        staff_chat = self.bot.get_channel(907937553343209472)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        if payload.user_id == self.bot.user.id:
            return
        if payload.emoji.name == "📩":
            staff_chat = self.bot.get_channel(907937553343209472)
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
            await reaction.remove(payload.member)
            user = self.bot.get_user(payload.user_id)
            guild = self.bot.get_guild(payload.guild_id)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                ),
            }
            ch = await guild.create_text_channel(
                "ticket-{}".format(user), overwrites=overwrites
            )
            await staff_chat.send(
                f"{user.mention} has opened a ticket in {ch.mention} <@&884453174839230464>"
            )
            mes = await ch.send(
                f"Hi {user.mention}!\n\nYou have opened a ticket.\n\nPlease wait for a staff member to respond. In the meantime explain what is your question.... \nClick 🔒 to close the ticket"
            )
            await mes.add_reaction("🔒")
            await mes.pin()
            cur = await self.bot.connection.cursor()
            await cur.execute(
                f"INSERT into tickets (ch, user) VALUES ('{ch.id}', '{user.id}')"
            )
            await self.bot.connection.commit()
        elif payload.emoji.name == "🔒":
            ch = channel
            cur = await self.bot.connection.cursor()
            await cur.execute(f"SELECT * from tickets WHERE ch = '{ch.id}'")
            r = await cur.fetchall()
            print(r)
            try:
                await self.bot.get_user(int(r[0][1])).send(
                    f"Your ticket has been closed by {self.bot.get_user(payload.user_id).mention}."
                )
                await ch.delete()
            except:
                print("No ticket found")
        elif payload.emoji.name == "📰":
            if message.id == 931505716630536232:
                member = guild.get_member(user.id)
                await member.add_roles(guild.get_role(931502468196597793))

        elif payload.emoji.name == "🗞️":
            if message.id == 931505716630536232:
                member = guild.get_member(user.id)
                await member.add_roles(guild.get_role(931503398807810099))
        elif payload.emoji.name == "⭐":
            f = open("data/stars.json", "r")
            data = f.read()
            if f"{message.id}" in data:
                return f.close()
            f.close()
            f = open("data/stars.json", "w")
            data = json.loads(data)

            starch = self.bot.get_channel(934056385870712862)
            reaction = get(message.reactions, emoji=payload.emoji.name)
            if reaction and reaction.count >= 1:
                data.append(f"{message.id}")
                f.write(json.dumps(data))
                f.close()
                emb = discord.Embed(
                    title=f"⭐ | {message.author}",
                    description=message.content,
                    color=discord.Color.yellow(),
                    url=f"{message.jump_url}",
                )
                if len(message.attachments) > 0:
                    emb.set_thumbnail(url=message.attachments[0].url)
                emb.set_author(icon_url=message.author.avatar, name=f"{message.author}")

                await starch.send(embed=emb)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print(payload.emoji.name)
        user = self.bot.get_user(payload.user_id)
        guild = self.bot.get_guild(payload.guild_id)
        staff_chat = self.bot.get_channel(907937553343209472)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if payload.emoji.name == "📰":
            if message.id == 931505716630536232:
                member = guild.get_member(user.id)
                await member.remove_roles(guild.get_role(931502468196597793))

        elif payload.emoji.name == "🗞️":
            if message.id == 931505716630536232:
                member = guild.get_member(user.id)
                await member.remove_roles(guild.get_role(931503398807810099))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in [
            884439873891729418,
            930777257239273492,
            924987009691418634,
            922904176961417257,
            884440046294429706,
            921009915802288178,
        ]:
            await message.add_reaction("\U0001f44d")
            await message.add_reaction("\U0001f44e")
            thread = await message.create_thread(name="Discussione")
            emb = discord.Embed(
                title=f"Discussione sul messaggio di {message.author}",
                description=f"Parla di ciò che ha detto {message.author.mention}",
            )
            emb.color = discord.Color.brand_green()
            emb.set_author(
                name=f"{message.author.name}#{message.author.discriminator}",
                icon_url=message.author.avatar.url,
            )
            await thread.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Entrato")
        emb = discord.Embed(
            title=f"{member} è entrato!",
            description=f'Ciao {member.mention}, qui ci occupiamo di "scuola".',
            color=discord.Color.brand_green(),
        )
        emb.set_thumbnail(url="https://i.imgur.com/R1KuVAG.png")
        emb.set_author(name=member, icon_url=member.avatar)
        emb.timestamp = datetime.now()
        ch = self.bot.get_channel(838727867428765769)
        await ch.send(embed=emb)
    
    @commands.Cog.listener()
    async def on_member_leave(self, member):
        print("Uscito")
        emb = discord.Embed(
            title=f"{member} è uscito!",
            description=f'Speriamo che {member.mention} torni.',
            color=discord.Color.brand_green(),
        )
        emb.set_thumbnail(url="https://i.imgur.com/R1KuVAG.png")
        emb.set_author(name=member, icon_url=member.avatar)
        emb.timestamp = datetime.now()
        ch = self.bot.get_channel(838727867428765769)
        await ch.send(embed=emb)


def setup(bot):
    bot.add_cog(Events(bot))

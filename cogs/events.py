import discord
from discord.ext import commands
import json

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload.emoji.name)
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
                    read_messages=True, send_messages=True)
            }
            ch = await guild.create_text_channel('ticket-{}'.format(user), overwrites=overwrites)
            await staff_chat.send(f"{user.mention} has opened a ticket in {ch.mention} <@&884453174839230464>")
            mes = await ch.send(f"Hi {user.mention}!\n\nYou have opened a ticket.\n\nPlease wait for a staff member to respond. In the meantime explain what is your question.... \nClick 🔒 to close the ticket")
            await mes.add_reaction("🔒")
            await mes.pin()
            f = open("data/tickets.json", "r")
            data = json.load(f)
            data.append([ch.id, user.id])
            print(data)
            f.close()
            f = open("data/tickets.json", "w")
            f.write(json.dumps(data))
            f.close()
        elif payload.emoji.name == "🔒":
            f = open("data/tickets.json", "r")
            data = json.load(f)
            f.close()
            for a in data:
                if a[0] == payload.channel_id:
                    data.remove(a)
                    ch = self.bot.get_channel(payload.channel_id)
                    await ch.delete()
                    f = open("data/tickets.json", "w")
                    f.write(json.dumps(data))
                    f.close()
                    await self.bot.get_channel(907937553343209472).send(f"{self.bot.get_user(a[1]).mention} has closed their ticket.")
                    await self.bot.get_user(a[1]).send(f"Your ticket has been closed by {self.bot.get_user(payload.user_id).mention}.")
        elif payload.emoji.name == "✅":
            f = open("data/files.json", "r")
            data = json.load(f)
            f.close()
            print("==========================")
            print(data)
            print("==========================")
            try:
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                user = self.bot.get_user(payload.user_id)
                embed = message.embeds[0]
                print(embed.fields)
                embed = message.embeds[0]
                embed.color = discord.Color.green()
                embed.set_footer(text="This file has been approved by {}".format(user))
                upload = data[embed.title]
                print(int(upload[1]))
                print(payload.message_id)
                if int(upload[1]) == payload.message_id:
                    print("1")
                    if channel == self.bot.get_channel(907937553343209472):
                        if upload[2] == "pending":
                            upload[2] = "approved"
                            f = open("data/files.json", "w")
                            f.write(json.dumps(data))
                            f.close()
                            print(embed.color)
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            guy = self.bot.get_user(int(upload[3]))
                            await guy.send(f"Your file has been approved by {user.mention}.")
                            c = self.bot.get_channel(int(838728591238758411))
                            await c.send(f"{self.bot.get_user(int(upload[3]))} has shared a file: {embed.title}. Do `.download {embed.title}` to download it.")
            except:
                import traceback
                traceback.print_exc()
        elif payload.emoji.name == "❌":
            f = open("data/files.json", "r")
            data = json.load(f)
            f.close()
            print("==========================")
            print(data)
            print("==========================")
            try:
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                user = self.bot.get_user(payload.user_id)
                embed = message.embeds[0]
                print(embed.fields)
                embed = message.embeds[0]
                embed.color = discord.Color.red()
                embed.set_footer(text=f"This file has been rejected by {user}.")
                upload = data[embed.title]
                print(int(upload[1]))
                print(payload.message_id)
                if int(upload[1]) == payload.message_id:
                    print("1")
                    
                    print("2")
                    if channel == self.bot.get_channel(907937553343209472):
                        print("3")
                        if upload[2] == "pending":
                            print("4")
                            upload[2] = "deined"
                            f = open("data/files.json", "w")
                            f.write(json.dumps(data))
                            f.close()
                            print(embed.color)
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            guy = self.bot.get_user(int(upload[3]))
                            await guy.send(f"Your file has been approved by {user.mention}.")
            except:
                import traceback
                traceback.print_exc()


            




def setup(bot):
    bot.add_cog(Events(bot))
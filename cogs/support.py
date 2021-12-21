import discord
from discord.ext import commands


class Counter(discord.ui.View):
    @discord.ui.button(label='Open', style=discord.ButtonStyle.primary)
    async def openticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.repl('Opening', complete_hidden=True)
        member = interaction.author
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.guild.create_text_channel('ticket-{}'.format(interaction.author), overwrites=overwrites)
        await interaction.channel.send('Ticket opened in #ticket-{}'.format(interaction.author), complete_hidden=True)
        

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="support", aliases=["tickets", "ticket"], description="Open a support ticket")
    @commands.is_owner()
    async def support(self, ctx):
        m = await ctx.send("Open a ticket here!")
        await m.add_reaction("📩")



    
def setup(bot):
    bot.add_cog(Support(bot))

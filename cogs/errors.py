import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.ConversionError):
            pass
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.PrivateMessageOnly):
                pass
            elif isinstance(error, commands.NoPrivateMessage):
                pass
            elif isinstance(error, commands.CheckAnyFailure):
                pass
            elif isinstance(error, commands.NotOwner):
                pass
            elif isinstance(error, commands.MissingPermissions):
                pass
            elif isinstance(error, commands.BotMissingPermissions):
                pass
            elif isinstance(error, commands.MissingRole):
                pass
            elif isinstance(error, commands.BotMissingRole):
                pass
            elif isinstance(error, commands.MissingAnyRole):
                pass
            elif isinstance(error, commands.BotMissingAnyRole):
                pass
            elif isinstance(error, commands.NSFWChannelRequired):
                pass
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.DisabledCommand):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            pass
        elif isinstance(error, commands.UserInputError):
            if isinstance(error, commands.MissingRequiredArgument):
                pass
            elif isinstance(error, commands.ArgumentParsingError):
                if isinstance(error, commands.UnexpectedQuoteError):

                    await ctx.send("Invalid quotes!")
                elif isinstance(error, commands.InvalidEndOfQuotedStringError):
                    await ctx.send("I don't understand this syntax")
                elif isinstance(error, commands.ExpectedClosingQuoteError):
                    await ctx.send("I don't understand this syntax")
            elif isinstance(error, commands.BadArgument):
                if isinstance(error, commands.MessageNotFound):
                    await ctx.send("What message?")
                elif isinstance(error, commands.MemberNotFound):
                    await ctx.send("Member not cached or unexisting")
                elif isinstance(error, commands.GuildNotFound):
                    await ctx.send("404 server not found")
                elif isinstance(error, commands.UserNotFound):
                    await ctx.send("User not cached or unexisting")
                elif isinstance(error, commands.ChannelNotFound):
                    await ctx.send("[NUCLEAR ERROR] This channel does not exist")
                elif isinstance(error, commands.ChannelNotReadable):
                    await ctx.send("I'm blind, I dont read that!")
                elif isinstance(error, commands.BadColourArgument):
                    await ctx.send("What the heck is this color")
                elif isinstance(error, commands.RoleNotFound):
                    await ctx.send("This role does not exist")
                elif isinstance(error, commands.BadInviteArgument):
                    await ctx.send("I am not invited  to that party!")
                elif isinstance(error, commands.EmojiNotFound):

                    await ctx.send("What emoji?")
                elif isinstance(error, commands.PartialEmojiConversionFailure):
                    await ctx.send("This emoji has too low data")
                elif isinstance(error, commands.BadBoolArgument):
                    await ctx.send("I cant convert to 0 or 1")
            elif isinstance(error, commands.TooManyArguments):
                await ctx.send("Too much data, explosion risk 101%")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You are too fast! Wait {round(error.retry_after, 2)} seconds"
            )
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Too much concorrents")
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(
                f"You are too fast! Wait {round(error.retry_after, 2)} seconds"
            )
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Too much concorrents")
        elif isinstance(error, commands.ExtensionError):
            if isinstance(error, commands.ExtensionAlreadyLoaded):
                print("[EXTENSIONS] Extension already loaded.")
            elif isinstance(error, commands.ExtensionNotLoaded):
                print("[EXTENSIONS] Extension not loaded.")
            elif isinstance(error, commands.NoEntryPointError):
                print("[EXTENSIONS] no setup in extension.")
            elif isinstance(error, commands.ExtensionFailed):
                print("[EXTENSIONS] extension failed.")
            elif isinstance(error, commands.ExtensionNotFound):
                print("[EXTENSIONS] extension not found.")
        elif isinstance(error, commands.CommandRegistrationError):
            print("[COMMANDS] error while registering command.")
        raise error


def setup(bot):
    bot.add_cog(Errors(bot))

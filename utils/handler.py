import discord
import traceback
import sys
from discord.ext import commands
url = "https://cdn.discordapp.com/attachments/800381129223831592/814762083220324392/tuxpi.com.1613127751-removebg-preview.png"
website = "https://modbot.studio"
red = 0xF04747
green = 0x43B581
orange = 0xFAA61A


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = commands.CommandNotFound
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down!", description=f"Command is on cooldown, try again in {error.retry_after:.2f}s.", color=orange)
            em.set_author(name="modbot", icon_url=url, url=website)
            await ctx.send(embed=em)

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
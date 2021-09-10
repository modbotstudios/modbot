import statcord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv("../.env")


class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = os.getenv("STATCORD")
        self.api = statcord.Client(self.bot, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatcordPost(bot))

import dbl
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv("../.env")


class TopGG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv('DBL')
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=15)
    async def update_stats(self):
        """This function runs every 5 minutes to automatically update your server count."""
        await self.bot.wait_until_ready()

        try:
            server_count = len(self.bot.guilds)
            await self.dblpy.post_guild_count(server_count)
            print('Posted server count ({})'.format(server_count))

        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(TopGG(bot))

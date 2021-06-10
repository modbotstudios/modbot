from discord.ext import commands, tasks
import dbl, os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')

class TopGG(commands.Cog):
    """
    This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 5 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4MDY5NzEzMDkwOTMwMjgwNSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA3NTI3MTA3fQ.KxpOrdARt0fBfEBPeM9gtCO_CtGhI5o-_MCAKDgjf6Q' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=5)
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

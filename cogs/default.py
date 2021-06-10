from discord.ext import commands
import datetime, time, discord
class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Hidden means it won't show up on the default help.

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Load a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
        


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')




    @commands.command(name='names', aliases=['guilds'], hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx):
        activeservers = self.bot.guilds
        for guild in activeservers:
            user = self.bot.get_user(776713998682292274)
            await user.send(guild.name)
    


    @commands.command(name='servers', hidden=True)
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send(f"I'm in {len(self.bot.guilds)} servers!")
   

    





def setup(bot):
    bot.add_cog(OwnerCog(bot))

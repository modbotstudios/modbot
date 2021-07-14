import asyncio
import datetime
import os
import time

import discord
import pymongo
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

import short
from keep_alive import keep_alive

url = "https://cdn.discordapp.com/attachments/800381129223831592/814762083220324392/tuxpi.com.1613127751-removebg-preview.png"  # -> This is the URL of all the embeds' thumbnails.
website = "https://modbot.studio"
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
red = 0xF04747
green = 0x43B581
orange = 0xFAA61A
client = pymongo.MongoClient(str(os.getenv("URL")))
mydb = client["mydatabase"]
prefixes = mydb["guild"]
warns = mydb["warns"]
embedVar = ""
css1 = ''
addedword = False


def get_prefix(bot, message):
    if not message.guild:
        return '/'
    else:
        a = prefixes.find_one({"_id": str(message.guild.id)})
        return a["prefix"]


@tasks.loop(seconds=300)
async def change_status():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="/help in {} servers!".format(len(bot.guilds))))


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
bot.launch_time = datetime.datetime.now()
print("Deleting default help command.....")
bot.remove_command('help')
extensions = ['cogs.default', 'cogs.stats', 'cogs.music', 'cogs.log']  # 'cogs.post'
print("Loading extensions.....")
if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
print("All the extensions were loaded.")
print("Waiting for bot to be ready......")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="/help in {} servers!".format(len(bot.guilds))))
    print("Ready")
    print("Logged in as {}".format(bot.user.name))
    print("----------")
    print("Using discord.py version", discord.__version__)
    print(f"ID: {bot.user.id}")
    print(f"Full username: {bot.user}")
    print("----------")
    change_status.start()


@bot.event
async def on_guild_remove(guild):
    try:
        query = {"_id": str(guild.id)}
        prefixes.delete_one(query)
    except Exception as e:
        print(e)


emptylist = []


@bot.event
async def on_guild_join(guild):
    default = {"_id": str(guild.id), "prefix": "/", "filter": True, "whitelist": emptylist, "language": 'en',
               "welcomeMessage": False, "goodbyeMessage": False,
               "wMessage": 'Hey {{user}}, welcome to {{server}}! :wave:',
               "gMessage": 'Noooooo! {{user}} left the server! :weary_face:', "wChannel": 'empty', "gChannel": 'empty',
               "badWords": emptylist, "infractions": emptylist}
    prefixes.insert_one(default)
    embed = discord.Embed(title="Thanks for adding me to your server!",
                          description="I hope I could help you to make this server a better place!")
    embed.set_author(name="modbot", url=website, icon_url=url)
    embed.add_field(name="Get started", value="To view all my commands simply chat /help. ", inline=True)
    embed.add_field(name="Get help",
                    value="If you need more help you can join the support server by [this link](https://discord.gg/N94NXsVNQg). To report ",
                    inline=True)
    embed.add_field(name="Donations",
                    value="We really appreciate donation to support our developement and hosting!! Donate by [joining our support server](https://discord.gg/N94NXsVNQg) and sending \"donate\" in general, thank you!!!",
                    inline=False)
    embed.set_footer(text="To report any issue [join our support server](https://discord.gg/N94NXsVNQg).")
    try:
        await guild.text_channels[0].send(embed=embed)
    except:
        try:
            await guild.text_channels[1].send(embed=embed)
        except:
            try:
                await guild.text_channels[2].send(embed=embed)
            except:
                try:
                    await guild.text_channels[3].send(embed=embed)
                except:
                    try:
                        await guild.text_channels[4].send(embed=embed)
                    except:
                        try:
                            await guild.text_channels[5].send(embed=embed)
                        except:
                            try:
                                await guild.text_channels[6].send(embed=embed)
                            except:
                                pass


@bot.command()
async def suggest(ctx, *, suggestion):
    channel = bot.get_channel(811979160968888351)
    await channel.send(f"{ctx.author} suggested '{suggestion}'")


@bot.command()
async def uptime(ctx):
    delta_uptime = datetime.datetime.now() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Yeah!",
                    value=f"My uptime is {days}d, {hours}h, {minutes}m, {seconds}s.",
                    inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    page = {}
    if not ctx.message.guild:
        pre = '/'
    else:
        a = prefixes.find_one({"_id": str(ctx.guild.id)})
        pre = a["prefix"]
    page['1'] = discord.Embed(title='Help page 1/4', color=green)
    page['1'].add_field(name=f"`TIP`",
                        value=f"You can use our [dashboard](https://dash.modbot.studio) (dash.modbot.studio) to customize modbot easily.",
                        inline=False)
    page['1'].add_field(name=f"{pre}play",
                        value=f"Play a song! Just join a voice channel and type \"{pre}play <song name>\"! ",
                        inline=False)
    page['1'].add_field(name=f"{pre}stop",
                        value=f"Stop the current playing song.",
                        inline=False)
    page['1'].add_field(name=f"{pre}loop",
                        value="Loops the current playing song.",
                        inline=False)
    page['1'].add_field(name=f"{pre}skip",
                        value=
                        f"Vote to skip to the next song in the queue. The requester can skip without voting.",
                        inline=False)
    page['1'].add_field(name=f"{pre}now",
                        value=
                        f"Display current playing song.",
                        inline=False)
    page['1'].add_field(name=f"{pre}volume",
                        value=f"Sets the player volume. Use \"{pre}volume <value>\". ",
                        inline=False)
    page['1'].add_field(name=f"{pre}queue",
                        value=
                        f"Display the player queue.",
                        inline=False)
    page['2'] = discord.Embed(title='Help page 2/4', color=green)
    page['2'].add_field(name=f"{pre}addword",
                        value=f"Add a custom swear word to your server! Simple type '{pre}addword <word>' changing word to the desired word.",
                        inline=False)
    page['2'].add_field(name=f"{pre}rmword",
                        value=f"Remove a custom swear word from your server's custom badwords! Simple type '{pre}rmword <word>' changing word to the desired word. You can only remove custom words. If you need to remove a default word just [join the support server](https://discord.gg/N94NXsVNQg) and ping the Developer or the Staff roles.",
                        inline=False)
    page['2'].add_field(name=f"{pre}prefix",
                        value="Select your custom prefix! Just type \"/prefix <your new prefix>\" changing your new prefix to the desired prefix. If you forgot the prefix simply ping me.",
                        inline=False)
    page['2'].add_field(name=f"{pre}whitelist",
                        value=
                        f"Simply whitelist an user from the swear words filter. To use this command type \"{pre}whitelist @user_mention\". You can whitelist an unlimited amount of members!",
                        inline=False)
    page['2'].add_field(name=f"{pre}blacklist",
                        value=
                        f"Simply blacklist an user to the swear words filter. To use this command type \"{pre}blacklist @user_mention\". All members are blacklisted by default.",
                        inline=False)
    page['2'].add_field(name=f"{pre}filter",
                        value=f"Simply turn ON/OFF the swear word filter, type \"{pre}filter <on/off>\".",
                        inline=False)
    page['2'].add_field(name=f"{pre}kick",
                        value=
                        f"Kick a member, use \"{pre}kick @user_mention <optional reason>\".",
                        inline=False)

    page['3'] = discord.Embed(title='Help page 3/4', color=green)
    page['3'].add_field(name=f"{pre}infractions",
                        value=
                        f"Check how many infractions an user has! Use '{pre}infractions @user_ping'",
                        inline=False)
    page['3'].add_field(name=f"{pre}clearall",
                        value=
                        f"Clear all the infractions for an user. Use '{pre}clearall @user_ping'",
                        inline=False)
    page['3'].add_field(name=f"{pre}ban",
                        value=f"Ban a member, use \"{pre}ban @user_mention <optional reason>\".",
                        inline=False)
    page['3'].add_field(name=f"{pre}unban",
                        value=f"Unban a member, use \"{pre}unban member_username#XXXX\".",
                        inline=False)
    page['3'].add_field(name=f"{pre}mute",
                        value=
                        f"Mute an user. To use this command create a \"Muted\" role without the \"Send messages\" permission. Then type \"{pre}mute @user_mention\".",
                        inline=False)
    page['3'].add_field(name=f"{pre}unmute",
                        value=
                        f"Unmute an user. To use this command you have to mute the user first and type \"{pre}unmute @user_mention\".",
                        inline=False)
    page['3'].add_field(name=f"{pre}new",
                        value=
                        f"Create a new text channel. Use \"{pre}new name of the channel\". Discord willl automatically convert whitespaces into \"-\"",
                        inline=False)
    page['3'].add_field(name=f"{pre}delete",
                        value=
                        f"Delete a text or a voice channel. You can also use /rm. For use this command just type \"{pre}rm channel-name\".",
                        inline=False)

    page['4'] = discord.Embed(title='Help page 4/4', color=green)
    page['4'].add_field(name=f"{pre}suggest",
                        value=
                        f"Suugest a new feature or report a bug to the developers! Use \"{pre}suggest <your suggestion>\". We accept any kind of idea, thank you for helping us!",
                        inline=False)
    page['4'].add_field(name=f"{pre}short",
                        value=f"Short an url! Simply use '{pre}short <url to short>'",
                        inline=False)
    page['4'].add_field(name=f"{pre}invite",
                        value=
                        "Create an instant invite to your server. Note that the generated invite will never expire and it will have unlimited uses.",
                        inline=False)
    page['4'].add_field(name=f"{pre}info",
                        value=f"Get the join date of a member, use \"{pre}info @user_mention\".",
                        inline=False)
    page['4'].add_field(name=f"{pre}purge",
                        value=
                        f"Purge as many messages as you want, use \"{pre}purge <numer of messages to delete>\"",
                        inline=False)
    page['4'].add_field(name=f"{pre}uptime",
                        value=
                        "Check the bot uptime.",
                        inline=False)
    page['4'].add_field(name=f"{pre}ping",
                        value="Check the bot's ping",
                        inline=False)
    page['4'].add_field(name="More Info",
                        value=
                        f"You can get more info about modbot on https://modbot.studio. To contact the team directly [join the support server](https://discord.gg/N94NXsVNQg).")

    number = 1
    pagination = await ctx.send(embed=page[str(number)])
    await pagination.add_reaction('⏪')
    await pagination.add_reaction('⬅️')
    await pagination.add_reaction('⏹')
    await pagination.add_reaction('➡️')
    await pagination.add_reaction('⏩')

    def check(reaction, user):
        return reaction.emoji in ['⬅️', '➡️', '⏹', '⏩', '⏪'] and user == ctx.author

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=600, check=check)
        except asyncio.TimeoutError:
            await pagination.delete()
            break
        else:
            if reaction.emoji == '➡️':
                number += 1
                try:
                    await reaction.remove(ctx.author)
                except:
                    pass
                try:
                    await pagination.edit(embed=page[str(number)])
                except KeyError:
                    number = 1
                    await pagination.edit(embed=page[str(number)])
            elif reaction.emoji == '⬅️':
                number -= 1
                try:
                    await reaction.remove(ctx.author)
                except:
                    pass
                try:
                    await pagination.edit(embed=page[str(number)])
                except KeyError:
                    number = 4
                    await pagination.edit(embed=page[str(number)])
            elif reaction.emoji == '⏹':
                try:
                    await pagination.clear_reactions()
                except:
                    pass
                break
            elif reaction.emoji == '⏩':
                number = 4
                try:
                    await reaction.remove(ctx.author)
                except:
                    pass
                try:
                    await pagination.edit(embed=page[str(number)])
                except KeyError:
                    number = 4
                    await pagination.edit(embed=page[str(number)])
            elif reaction.emoji == '⏪':
                number = 1
                try:
                    await reaction.remove(ctx.author)
                except:
                    pass
                try:
                    await pagination.edit(embed=page[str(number)])
                except KeyError:
                    number = 4
                    await pagination.edit(embed=page[str(number)])


## Accept command  ##
@bot.command(pass_context=True)
@commands.has_permissions(send_messages=True)
async def accept(message):
    user = message.message.author
    role = 'Verified'
    try:
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        await message.channel.purge(limit=1)
    except Exception as e:
        await message.send(
            'Cannot assign role. Error: ' + str(e))
        print('Cannot assign role. Error: ' + str(e))


## Ban command ##
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    check = False
    for i in member.roles:
        if i in ctx.author.roles[1:]:
            check = True
    if check is True:
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name=":x:", value="I can't ban members with a role that is higher than mine!", inline=True)
        await ctx.send(embed=embed)
    else:
        await member.ban(reason=reason)
        embed = discord.Embed(color=orange)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name=":lock:", value=f"{member.mention} was banned by {ctx.author.mention}!", inline=True)
        await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again pinging the member to ban!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to ban a member! You need the Ban members permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found", value=f"{ctx.author.mention}, please tell me a member to ban!",
                        inline=True)
        await ctx.send(embed=embed)


## Unban command ##
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(color=green)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name=":unlock:", value=f"{member} was unbanned by {ctx.author.mention}!",
                            inline=True)
            await ctx.send(embed=embed)
            break
        else:
            embed = discord.Embed(color=green)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name=":x:", value=f"{member} could not be found in the list of banned users!",
                            inline=True)
            await ctx.send(embed=embed)
            break


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again typing the username and the discriminator of the user to unban!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to unban a member! You need the Ban members permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found", value=f"{ctx.author.mention}, please tell me a member to unban!",
                        inline=True)
        await ctx.send(embed=embed)


## Kick command ##
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    check = False
    for i in member.roles:
        if i in ctx.author.roles[1:]:
            check = True
    if check is True:
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name=":x:", value="I can't kick moderator/admins!", inline=True)
        await ctx.send(embed=embed)
    else:
        await member.kick(reason=reason)
        embed = discord.Embed(color=orange)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name=":lock:", value=f"{member.mention} was kicked by {ctx.author.mention}!", inline=True)
        await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again pinging the member to kick!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to kick a member! You need the Kick members permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found", value=f"{ctx.author.mention}, please tell me a member to kick!",
                        inline=True)
        await ctx.send(embed=embed)


## Info command ##
@bot.command(aliases=['profile'])
async def info(ctx, member: discord.Member):
    embed = discord.Embed(color=red)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Info",
                    value=f"{member.mention} joined the server at {member.joined_at}",
                    inline=True)
    await ctx.send(embed=embed)


@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again pinging the member to check!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found", value=f"{ctx.author.mention}, please tell me a member to check!",
                        inline=True)
        await ctx.send(embed=embed)


## Short command ##
@bot.command(name='short')
async def short_url(ctx, *, url):
    a = short.shorten(str(url))
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"{ctx.author.mention}, your url was shorened! Copy it --> {a}",
                    inline=True)
    await ctx.send(embed=embed)


## Clean command ##
@bot.command(pass_context=True, aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit1: int):
    limit = limit1 + 1
    await ctx.channel.purge(limit=limit)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website, icon_url=url)
    embed.add_field(name="Done!", value=f"Purged {limit1} messages!", inline=True)
    await ctx.send(embed=embed)
    await ctx.message.delete()


@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Bad value",
                        value=f"{ctx.author.mention}, you typed a bad number of messages to delete! Retry!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to purge the chat! You need the Manage messages permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="No amount given!",
                        value=f"{ctx.author.mention}, please tell me an amount of messages to delete!",
                        inline=True)
        await ctx.send(embed=embed)


## Mute command ##
@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await member.add_roles(discord.utils.get(member.guild.roles, name='Muted'))
    embed = discord.Embed(title="User Muted!",
                          description=f"**{member}** was muted by **{ctx.message.author}**!",
                          color=orange)
    await ctx.send(embed=embed)


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("ERROR 403! You don't have enough permissions to do it!"
                       )
    if isinstance(error, commands.BadArgument):
        await ctx.send("ERROR 400! You passed me a bad member to mute!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR 400! Tell me the member to mute!")


## Unmute command ##
@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
    await user.remove_roles(discord.utils.get(user.guild.roles, name='Muted'))
    embed = discord.Embed(title="User Unmuted!",
                          description=f"**{user}** was unmuted by **{ctx.message.author}**!",
                          color=green)
    await ctx.send(embed=embed)


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("ERROR 403! You don't have enough permissions to do it!"
                       )
    if isinstance(error, commands.BadArgument):
        await ctx.send("ERROR 400! You passed me a bad member to unmute!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR 400! Tell me the member to unmute!")


## New text channel command ##
@bot.command(aliases=['new_txt', 'text'])
async def new_text_channel(ctx, *, name):
    guild = ctx.message.guild
    await guild.create_text_channel(name)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"Successfully created the \"{name}\" channel!", inline=True)
    await ctx.send(embed=embed)


@new_text_channel.error
async def new_text_channel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to create a channel! You need the Manage channels permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="No name given",
                        value=f"{ctx.author.mention}, please tell me a name for the new channel!", inline=True)
        await ctx.send(embed=embed)


## New channel command ##
@bot.command(aliases=['new_voice', 'voice'])
async def new_voice_channel(ctx, *, name):
    guild = ctx.message.guild
    await guild.create_voice_channel(name)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"Successfully created the \"{name}\" channel!", inline=True)
    await ctx.send(embed=embed)


@new_voice_channel.error
async def new_voice_channel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to create a channel! You need the Manage channels permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="No name given",
                        value=f"{ctx.author.mention}, please tell me a name for the new channel!", inline=True)
        await ctx.send(embed=embed)


## Ping command ##
@bot.command()
async def ping(ctx):
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name=":ping_pong:", value=f"{ctx.author.mention}, my ping is {round(bot.latency * 1000)}ms!",
                    inline=True)
    await ctx.send(embed=embed)


## Refresh command ##
@bot.command(name='refresh', hidden=True)
@commands.is_owner()
async def refresh(ctx):
    msg = await ctx.send("Refreshing my status...")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="/help in {} servers!".format(len(bot.guilds))))
    time.sleep(1)
    await msg.edit(content="Ok, i refreshed my status. I'm in {} servers.".
                   format(len(bot.guilds)))


## Upgrade command ##
@bot.command(name='upgrade', hidden=True)
@commands.is_owner()
async def upgrade(ctx):
    await ctx.send("Under upgrade mode toggled.")
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="for upgrade......"))


## Invite command ##
@bot.command()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age=0)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"This is your invite link: {str(link)}", inline=True)
    await ctx.send(embed=embed)


## Status command ##
@bot.command()
@commands.is_owner()
async def status(ctx):
    embedVar = discord.Embed(title="Bot Info", color=green)
    embedVar.set_thumbnail(url=bot.user.avatar_url)
    embedVar.add_field(
        name="Owner:", value='<@776713998682292274>', inline=False)
    embedVar.add_field(name="Name:", value=bot.user.name, inline=False)
    embedVar.add_field(name="ID:", value=bot.user.id, inline=False)
    embedVar.add_field(
        name="Ping:", value=f'{round(bot.latency * 1000)}ms', inline=False)
    embedVar.add_field(
        name="Total Servers in:",
        value=f"{len(bot.guilds)} servers",
        inline=False)
    await ctx.send(embed=embedVar)


## Prefix command ##
@bot.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix):
    query = {"_id": str(ctx.guild.id)}
    new = {"$set": {"prefix": str(prefix)}}
    prefixes.update_one(query, new)
    await ctx.send(f'Prefix changed to {prefix}')


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to change the prefix! You need the Manage server permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Invalid prefix", value=f"{ctx.author.mention}, please tell me a prefix to set!",
                        inline=True)
        await ctx.send(embed=embed)


## Whitelist command ##
@bot.command()
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    query = {"_id": str(ctx.guild.id)}
    new = {"$push": {"whitelist": str(member.id)}}
    prefixes.update_one(query, new)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"{member.mention} has got whitelisted!", inline=True)
    await ctx.send(embed=embed)


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again pinging the member to whitelist!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to whitelist a member! You need the Administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, please tell me a member to whitelist!", inline=True)
        await ctx.send(embed=embed)


## Blacklist command ##
@bot.command()
@commands.has_permissions(administrator=True)
async def blacklist(ctx, member: discord.Member = None):
    try:
        query = {'_id': str(ctx.guild.id)}
        new = {"$pull": {"whitelist": str(member.id)}}
        prefixes.update_one(query, new)
    except:
        pass
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"{member.mention} has got blacklisted!", inline=True)
    await ctx.send(embed=embed)


@blacklist.error
async def blacklist_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again pinging the member to blacklist!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to blacklist a member! You need the Administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, please tell me a member to blacklist!", inline=True)
        await ctx.send(embed=embed)


## Filter command ##
@bot.command(name='set-swear', aliases=['filter'])
@commands.has_permissions(manage_guild=True)
async def set(ctx, *, arg: str):
    if arg.lower() == "off":
        try:
            query = {"_id": str(ctx.guild.id)}
            new = {"$set": {"filter": False}}
            prefixes.update_one(query, new)
            embed = discord.Embed(color=green)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name="Done!", value="The filter is now setted off!", inline=True)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=red)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name=":x:",
                            value=f"{ctx.author.mention}, the filter is already disabled in this server!",
                            inline=True)
            await ctx.send(embed=embed)
    if arg.lower() == "on":
        try:
            query = {"_id": str(ctx.guild.id)}
            new = {"$set": {"filter": True}}
            prefixes.update_one(query, new)
            embed = discord.Embed(color=green)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name="Done!", value="The filter is now setted on!", inline=True)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=red)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name=":x:",
                            value=f"{ctx.author.mention}, the filter is already enabled in this server!",
                            inline=True)
            await ctx.send(embed=embed)


@set.error
async def set_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Inavlid option",
                        value=f"{ctx.author.mention}, please choose a valid option (on/off)!", inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to disable the filter! You need the Administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Invalid option", value=f"{ctx.author.mention}, please tell me what to do (on/off)!",
                        inline=True)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def log(ctx, channel: str):
    channel = channel.replace("<#", "")
    channel = channel.replace(">", "")
    query = {"_id": str(ctx.guild.id)}
    new = {"$set": {"lChannel": str(channel)}}
    prefixes.update_one(query, new)
    embed = discord.Embed(color=green)
    embed.set_author(name="modbot", url=website,
                     icon_url=url)
    embed.add_field(name="Done!", value=f"Log channel was set!",
                    inline=True)
    await ctx.send(embed=embed)


@set.error
async def set_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Inavlid channel",
                        value=f"{ctx.author.mention}, please mention a real channel!", inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to disable the filter! You need the Administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Invalid channel", value=f"{ctx.author.mention}, please tell me a channel to set!",
                        inline=True)
        await ctx.send(embed=embed)

@bot.event
async def on_message(m: discord.Message) -> None:
    ctx = await bot.get_context(m)
    a = prefixes.find_one({"_id": str(m.guild.id)})
    chid = a["lChannel"]

    if ctx.valid:
        return await bot.process_commands(m)
    else:
        try:
            if m.mentions[0] == bot.user:
                if not m.is_system():
                    if not m.author.bot:
                        if not m.guild:
                            await m.channel.send('My prefix in DM is `/`')
                        else:
                            try:
                                a = prefixes.find_one({"_id": str(m.guild.id)})
                                pre = a["prefix"]
                            except:
                                pass
                            await m.channel.send(f'My prefix in {ctx.guild.name} is: `{pre}`')
        except:
            pass
        if m.guild:
            if m.author.id != bot.user.id:
                if not m.author.bot:
                    if not m.guild:
                        pre = '/'
                    else:
                        a = prefixes.find_one({"_id": str(m.guild.id)})
                        pre = a["prefix"]
                    if a["filter"] is True:
                        with open('db/badwords.txt', 'r') as f:
                            badwords = f.read()
                        if prefixes.find(
                                {"_id": str(m.guild.id), "whitelist": {"$all": [str(m.author.id)]}}).count() > 0: return
                        if m.content.startswith('e'): return
                        if m.attachments: return
                        if m.is_system(): return
                        with open('db/badwords.txt', 'r') as f:
                            words = f.read()
                            badwords = words.split()
                        for words in badwords:
                            global addedword
                            global css1
                            list1 = m.content.lower().split(' ')

                            def check():
                                if prefixes.find({"_id": str(m.guild.id), "badWords": {"$all": [list1]}}).count() > 0:
                                    return True
                                else:
                                    return False

                            msg = m.content.lower().split(' ')
                            if words in msg or check() is True:
                                css1 = ""
                                if m.author.guild_permissions.administrator or m.author.guild_permissions.manage_guild or m.author.guild_permissions.manage_messages:
                                    await m.delete()
                                    await m.channel.send(
                                        f"I can't warn you because you're an admin! Type '{pre}whitelist {m.author.mention}' to add you in the whitelist. ")
                                    pass
                                else:
                                    await m.reply(f'You got a warn into the {m.guild.name} server {m.author.mention}!')
                                    await m.delete()
                                    if not warns.find(
                                            {'_id': str(m.guild.id), str(m.author.id): 1}).count() > 0 and warns.find(
                                        {'_id': str(m.guild.id), str(m.author.id): 2}).count() == 0 and warns.find(
                                        {'_id': str(m.guild.id), str(m.author.id): 3}).count() == 0:
                                        query = {"_id": str(m.guild.id)}
                                        new = {"$set": {str(m.author.id): 1}}
                                        try:
                                            query1 = {"_id": str(m.guild.id), str(m.author.id): 1}
                                            warns.insert_one(query1)
                                        except:
                                            warns.update_one(query, new)
                                    else:
                                        if not warns.find({'_id': str(m.guild.id),
                                                           str(m.author.id): 2}).count() > 0 and warns.find(
                                            {'_id': str(m.guild.id), str(m.author.id): 1}).count() == 0:
                                            query = {"_id": str(m.guild.id)}
                                            new = {"$set": {str(m.author.id): 2}}
                                            warns.update_one(query, new)
                                        else:
                                            if not warns.find(
                                                    {'_id': str(m.guild.id), str(m.author.id): 3}).count() > 0:
                                                query = {"_id": str(m.guild.id)}
                                                new = {"$set": {str(m.author.id): 3}}
                                                warns.update_one(query, new)
                                                await m.author.ban()
                                                user = bot.get_user(m.author.id)
                                                await user.send(f'You just got banned from {m.guild.name}.')
                                                query = {"_id": str(m.guild.id)}
                                                delete = {"$unset": {str(m.author.id): 3}}
                                                warns.update_one(query, delete)


## Add word command ##
@bot.command(aliases=['new-word', 'ban-word'])
@commands.has_permissions(administrator=True)
async def addword(ctx, *, word):
    if ctx.guild:
        query = {"_id": str(ctx.guild.id)}
        new = {"$push": {"badWords": str(word)}}
        prefixes.update_one(query, new)
        embed = discord.Embed(color=green)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Done!",
                        value=f"Ok, I've added \"{word}\" to this server's blacklist!",
                        inline=True)
        await ctx.send(embed=embed)


@addword.error
async def addword_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to add a swear word! You need the administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Invalid word", value=f"{ctx.author.mention}, please tell me a word to blacklist!",
                        inline=True)
        await ctx.send(embed=embed)


## REMOVE BANNED WORD ##
@bot.command(aliases=['rm-word', 'consent-word'])
@commands.has_permissions(administrator=True)
async def rmword(ctx, *, word):
    if ctx.guild:
        start = {"_id": str(ctx.guild.id)}
        query = {"$pull": {"badWords": str(word)}}
        prefixes.update_one(start, query)
        embed = discord.Embed(color=green)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Done!",
                        value=f"Ok, I've removed \"{word}\" from this server's blacklist!",
                        inline=True)
        await ctx.send(embed=embed)


@rmword.error
async def rmword_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to remove a word from the blacklist! You need the administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Invalid word", value=f"{ctx.author.mention}, please tell me a word to whitelist!",
                        inline=True)
        await ctx.send(embed=embed)


@bot.command(aliases=['warns'])
async def infractions(ctx, member: discord.Member):
    if ctx.guild:
        try:
            a = warns.find_one({"_id": str(ctx.guild.id)})
            b = a[str(member.id)]
            embed = discord.Embed(color=orange)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name="Warns", value=f"{member.mention} has {b} warns.",
                            inline=True)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=green)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name="Warns", value=f"{member.mention} has no warns!",
                            inline=True)
            await ctx.send(embed=embed)


@infractions.error
async def infractions_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you told me! Try again pinging the member to check!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found", value=f"{ctx.author.mention}, please tell me a member to check!",
                        inline=True)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clearall(ctx, member: discord.Member):
    if ctx.guild:
        try:
            query = {"_id": str(ctx.guild.id)}
            new = {"$unset": {str(member.id): 1}}
            warns.update_one(query, new)
            embed = discord.Embed(color=green)
            embed.set_author(name="modbot", url=website,
                             icon_url=url)
            embed.add_field(name="Done!",
                            value=f"All warns of {member.mention} where cleared!",
                            inline=True)
            await ctx.send(embed=embed)
        except:
            try:
                query = {"_id": str(ctx.guild.id)}
                new = {"$unset": {str(member.id): 2}}
                warns.update_one(query, new)
                embed = discord.Embed(color=green)
                embed.set_author(name="modbot", url=website,
                                 icon_url=url)
                embed.add_field(name="Done!",
                                value=f"All warns of {member.mention} where cleared!",
                                inline=True)
                await ctx.send(embed=embed)
            except:
                try:
                    query = {"_id": str(ctx.guild.id)}
                    new = {"$unset": {str(member.id): 3}}
                    warns.update_one(query, new)
                    embed = discord.Embed(color=green)
                    embed.set_author(name="modbot", url=website,
                                     icon_url=url)
                    embed.add_field(name="Done!",
                                    value=f"All warns for {member.mention} where cleared!",
                                    inline=True)
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(color=green)
                    embed.set_author(name="modbot", url=website,
                                     icon_url=url)
                    embed.add_field(name=":x:",
                                    value=f"{member.mention} has no wanrs!",
                                    inline=True)
                    await ctx.send(embed=embed)


@clearall.error
async def clearall_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found",
                        value=f"{ctx.author.mention}, i could not found the member you tell me! Try again pinging the member to clear!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Missing permissions",
                        value=f"{ctx.author.mention}, you don't have enough permissions to clear a member! You need the Administrator permission to use this command!",
                        inline=True)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=red)
        embed.set_author(name="modbot", url=website,
                         icon_url=url)
        embed.add_field(name="Member not found", value=f"{ctx.author.mention}, please tell me a member to clear!",
                        inline=True)
        await ctx.send(embed=embed)


def run(**kwargs):
    if kwargs["webserver"]:
        keep_alive()
        bot.run(kwargs["auth"])
    else:
        bot.run(kwargs["auth"])


run(webserver=True, auth=token)

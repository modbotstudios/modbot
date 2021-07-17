import asyncio
import datetime
import os

import discord
import pymongo
from discord.ext import commands
from dotenv import load_dotenv

red = 0xF04747
green = 0x43B581
orange = 0xFAA61A
url = "https://cdn.discordapp.com/attachments/800381129223831592/814762083220324392/tuxpi.com.1613127751-removebg-preview.png"  # -> This is the URL of all the embeds' thumbnails.
website = "https://modbot.studio"
load_dotenv("../.env")
client = pymongo.MongoClient(str(os.getenv("URL")))
mydb = client["mydatabase"]
prefixes = mydb["guild"]


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        a = prefixes.find_one({"_id": str(member.guild.id)})
        chid = a["lChannel"]
        channel = self.bot.get_channel(int(chid))
        e = discord.Embed(color=green, timestamp=datetime.datetime.utcnow())
        e.set_author(name=f"modbot", url=url, icon_url=url)
        e.add_field(name=":wave:", value=f"{member.mention} ({member}) just joined.",
                    inline=True)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_ban(self, gld, usr):
        await asyncio.sleep(0.5)
        found_entry = None
        a = prefixes.find_one({"_id": str(gld.id)})
        chid = a["lChannel"]
        channel = self.bot.get_channel(int(chid))
        async for entry in gld.audit_logs(limit=50, action=discord.AuditLogAction.ban,
                                          after=datetime.datetime.utcnow() - datetime.timedelta(seconds=15),
                                          oldest_first=False):
            if entry.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=10):
                continue
            if entry.target.id == usr.id:
                found_entry = entry
                break
        if not found_entry:
            return
        e = discord.Embed(color=red, timestamp=datetime.datetime.utcnow())
        e.set_author(name=f"modbot", url=url, icon_url=url)
        e.add_field(name=":lock:", value=f"{usr.mention} ({usr}) was banned.\nModerator: {found_entry.user.mention}",
                    inline=True)
        e.add_field(name="Target", value=f"<@{str(usr.id)}> ({str(usr)})", inline=True)
        e.add_field(name="Moderator", value=f"<@{str(found_entry.user.id)}> ({str(found_entry.user)})", inline=True)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_unban(self, gld, usr):
        await asyncio.sleep(0.5)
        found_entry = None
        a = prefixes.find_one({"_id": str(gld.id)})
        chid = a["lChannel"]
        channel = self.bot.get_channel(int(chid))
        async for entry in gld.audit_logs(limit=50, action=discord.AuditLogAction.unban,
                                          after=datetime.datetime.utcnow() - datetime.timedelta(seconds=15),
                                          oldest_first=False):
            if entry.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=10):
                continue
            if entry.target.id == usr.id:
                found_entry = entry
                break
        if not found_entry:
            return
        e = discord.Embed(color=green, timestamp=datetime.datetime.utcnow())
        e.set_author(name=f"modbot", url=url, icon_url=url)
        e.add_field(name=":unlock:",
                    value=f"{usr.mention} ({usr}) was unbanned.\nModerator: {found_entry.user.mention}",
                    inline=True)
        e.add_field(name="Target", value=f"<@{str(usr.id)}> ({str(usr)})", inline=True)
        e.add_field(name="Moderator", value=f"<@{str(found_entry.user.id)}> ({str(found_entry.user)})", inline=True)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_remove(self, usr):
        a = prefixes.find_one({"_id": str(usr.guild.id)})
        chid = a["lChannel"]
        channel = self.bot.get_channel(int(chid))
        await asyncio.sleep(0.5)
        found_entry = None
        async for entry in usr.guild.audit_logs(limit=50, action=discord.AuditLogAction.kick,
                                                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=10),
                                                oldest_first=False):  # 10 to prevent join-kick-join-leave false-positives
            if entry.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=10):
                try:
                    e = discord.Embed(color=orange, timestamp=datetime.datetime.utcnow())
                    e.set_author(name=f"modbot", url=url, icon_url=url)
                    e.add_field(name=":hammer:",
                                value=f"{usr.mention} was kicked.\nModerator: {found_entry.user.mention}",
                                inline=True)
                    e.add_field(name="Target", value=f"<@{str(usr.id)}> ({str(usr)})", inline=True)
                    e.add_field(name="Moderator", value=f"<@{str(found_entry.user.id)}> ({str(found_entry.user)})",
                                inline=True)
                    await channel.send(embed=e)
                except:
                        e = discord.Embed(color=red, timestamp=datetime.datetime.utcnow())
                        e.set_author(name=f"modbot", url=url, icon_url=url)
                        e.add_field(name=":wave:", value=f"{usr.mention} ({usr}) just left.",
                                    inline=True)
                        await channel.send(embed=e)
            if entry.target.id == usr.id:
                found_entry = entry
                break

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        a = prefixes.find_one({"_id": str(before.guild.id)})
        chid = a["lChannel"]
        channel = self.bot.get_channel(int(chid))
        if before.roles == after.roles:
            return
        muted_role = discord.utils.get(after.guild.roles, name="Muted")
        if not muted_role:
            return
        if muted_role in after.roles and not muted_role in before.roles:
            if after.joined_at > (datetime.datetime.utcnow() - datetime.timedelta(seconds=10)):  # join persist mute
                return
            await asyncio.sleep(0.5)  # wait for audit log
            found_entry = None
            async for entry in after.guild.audit_logs(limit=50, action=discord.AuditLogAction.member_role_update,
                                                      after=datetime.datetime.utcnow() - datetime.timedelta(seconds=15),
                                                      oldest_first=False):
                if entry.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=10):
                    continue
                if entry.target.id == after.id and not muted_role in entry.before.roles and muted_role in entry.after.roles:
                    found_entry = entry
                    break
            if not found_entry:
                return
            e = discord.Embed(color=orange, timestamp=datetime.datetime.utcnow())
            e.set_author(name=f"modbot", url=url, icon_url=url)
            e.add_field(name=":lock:", value=f"{after.mention} was muted.\nModerator: {found_entry.user.mention}",
                        inline=True)
            e.add_field(name="Target", value=f"<@{str(after.id)}> ({str(after)})", inline=True)
            e.add_field(name="Moderator", value=f"<@{str(found_entry.user.id)}> ({str(found_entry.user)})", inline=True)
            await channel.send(embed=e)
        elif muted_role not in after.roles and muted_role in before.roles:
            if after.joined_at > (datetime.datetime.utcnow() - datetime.timedelta(seconds=10)):  # join persist unmute
                return
            await asyncio.sleep(0.5)
            found_entry = None
            async for entry in after.guild.audit_logs(limit=50, action=discord.AuditLogAction.member_role_update,
                                                      after=datetime.datetime.utcnow() - datetime.timedelta(seconds=15),
                                                      oldest_first=False):
                if entry.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=10):
                    continue
                if entry.target.id == after.id and muted_role in entry.before.roles and not muted_role in entry.after.roles:
                    found_entry = entry
                    break
            if not found_entry:
                return
            e = discord.Embed(color=green, timestamp=datetime.datetime.utcnow())
            e.set_author(name=f"modbot", url=url, icon_url=url)
            e.add_field(name=":unlock:", value=f"{after.mention} was unmuted.\nModerator: {found_entry.user.mention}",
                        inline=True)
            e.add_field(name="Target", value=f"<@{str(after.id)}> ({str(after)})", inline=True)
            e.add_field(name="Moderator", value=f"<@{str(found_entry.user.mention)}> ({str(found_entry.user)})",
                        inline=True)
            await channel.send(embed=e)


def setup(bot):
    bot.add_cog(Log(bot))

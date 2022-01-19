import discord
from discord.ext import commands

def on_ready(bot):
    print("{0.user} пришел на сервера".format(bot))

async def reaction_add(bot, event, emoji_roles):
    emoji = event.emoji
    user = event.member
    if bot.user == user:
        return
    if emoji_roles[emoji.id] is not None:
        role = discord.utils.get(user.guild.roles, name=emoji_roles[emoji.id])
        await user.add_roles(role)

async def reaction_delete(bot, event, emoji_roles):
    guild = bot.get_guild(event.guild_id)
    member = guild.get_member(event.user_id)
    if bot.user == member:
        return
    emoji = event.emoji
    if emoji_roles[emoji.id] is not None:
        role = discord.utils.get(member.guild.roles, name=emoji_roles[emoji.id])
        await member.remove_roles(role)
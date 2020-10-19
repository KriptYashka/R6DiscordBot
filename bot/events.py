from module.module import *
from jager import bot

@bot.event
async def on_ready():
    print("{0.user} пришел на сервера".format(bot))


@bot.event
async def on_member_join(member):
    server = member.guild
    role = discord.utils.get(server.roles, name="Новичок")
    await member.add_roles(role)


@bot.event
async def on_raw_reaction_add(event):
    emoji = event.emoji
    user = event.member
    if bot.user == user:
        return
    if emoji_roles[emoji.id] is not None:
        role = discord.utils.get(user.guild.roles, name=emoji_roles[emoji.id])
        await user.add_roles(role)


@bot.event
async def on_raw_reaction_remove(event):
    emoji = event.emoji
    guild = bot.get_guild(event.guild_id)
    member = guild.get_member(event.user_id)

    if bot.user == member:
        return
    if emoji_roles[emoji.id] is not None:
        role = discord.utils.get(member.guild.roles, name=emoji_roles[emoji.id])
        await member.remove_roles(role)
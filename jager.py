import asyncio
import random
import time
import discord
from discord.ext import commands
import re

import view.talk
from view import phrases as phrases
import view.events as jager_event
import view.cmd as jager_cmd
import view.season_events as jager_season

# TOKEN = 'Your token'
# email = "Your email"
# password = "Your Password"
TOKEN = "NzAwMzUyMTg3MjE3MjE1NTU5.Xph" + "rzQ.XUCyt7slrQLM8NBoDAWmvXVfvfw"  # Чтобы не переделывать токен
prefix = "Ягер "
bot = commands.Bot(command_prefix=prefix)

# emoji_roles = {756609869326581840: 'Apex Legends', 756609380593434654: 'Dota 2',
#                756609572172595380: 'Counter-Strike', 700596539499872256: 'R6', 701007348730167346: 'PUBG',
#                756611247889317918: 'Valorant', 761243822716878859: 'Imposter'}

"""   Стандартные события   """


@bot.event
async def on_ready():
    jager_event.on_ready(bot)


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Разведчик")
    await member.add_roles(role)


# @bot.event
# async def on_raw_reaction_add(event):
#     await jager_event.reaction_add(bot, event, emoji_roles)
#
#
# @bot.event
# async def on_raw_reaction_remove(event):
#     await jager_event.reaction_delete(bot, event, emoji_roles)


"""   Разговор с ботом   """

re_cmd = {
    r"привет|здарова|ку": view.talk.send_hello,
    r"как играть|как научит[ь]ся играть": view.talk.send_how_to_play,
    r"инструкция|help": view.talk.instruction,
    r"эхо": view.talk.echo,

    r"запомни меня": view.cmd
}


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.content.lower().startswith(prefix.lower()):
        return
    ctx = message.content.replace(prefix, "").lower()
    for name, action in re_cmd.items():
        if re.match(name, ctx):
            await action(bot, message)

# @bot.command(pass_context=True)
# async def меню_группировок(ctx):
#     await jager_cmd.menu(bot, emoji_roles)

"""   Работа с чатом   """


# @bot.command(pass_context=True)
# async def удали(ctx, arg):
#     await jager_cmd.delete_message(ctx, arg)


"""   Игровые возможности   """


# @bot.command(pass_context=True)
# async def дай(ctx, command, *args):
#     await jager_cmd.get_something(bot, ctx, command, *args)
#
#
# @bot.command(pass_context=True)
# async def рейтинг(ctx, *args):
#     await jager_cmd.rating(ctx, *args)
#
#
# @bot.command(pass_context=True)
# async def запомни(ctx, command, *args):
#     await jager_cmd.register_user(bot, ctx, command, *args)


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()

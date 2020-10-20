import asyncio
import time
import discord
from discord.ext import commands

from jager_function import jager_phrases as phrases
import jager_function.events as jager_event
import jager_function.commands as jager_cmd
import jager_function.season_events as jager_season

# TOKEN = 'Your token'
# email = "Your email"
# password = "Your Password"
TOKEN = "NzAwMzUyMTg3MjE3MjE1NTU5." + "Xtpr8Q.pyZIcYBL7cyiqINLgyiogRx8ThY"  # Чтобы не переделывать токен
bot = commands.Bot(command_prefix='Ягер ')

emoji_roles = {756609869326581840: 'Apex Legends', 756609380593434654: 'Dota 2',
               756609572172595380: 'Counter-Strike', 700596539499872256: 'R6', 701007348730167346: 'PUBG',
               756611247889317918: 'Valorant', 761243822716878859: 'Imposter'}

"""   Стандартные события   """

@bot.event
async def on_ready():
    jager_event.on_ready(bot)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Новичок")
    await member.add_roles(role)


@bot.event
async def on_raw_reaction_add(event):
    await jager_event.reaction_add(bot, event, emoji_roles)

@bot.event
async def on_raw_reaction_remove(event):
    await jager_event.reaction_delete(bot, event, emoji_roles)


"""   Разговор с ботом   """

@bot.command(pass_context=True)
async def привет(ctx):
    text = jager_cmd.get_random_item(phrases.hello).format(str(ctx.message.author.name))
    await ctx.send(text)


@bot.command(pass_context=True)
async def как(ctx, arg):
    if arg == 'научиться' or arg == 'играть':
        text = "Никак. Удали к чертям эту игру!"
        await ctx.send(text)


@bot.command(pass_context=True)
async def инструкция(ctx):
    await jager_cmd.instruction(bot, ctx)


@bot.command(pass_context=True)
async def меню_группировок(ctx):
    await jager_cmd.menu(bot, emoji_roles)

@bot.command(pass_context=True)
async def эхо(ctx, arg):
    await jager_cmd.echo(ctx, arg)


"""   Работа с чатом   """

@bot.command(pass_context=True)
async def удали(ctx, arg):
    await jager_cmd.delete_message(ctx, arg)


"""   Игровые возможности   """

@bot.command(pass_context=True)
async def дай(ctx, command, *args):
    await jager_cmd.get_something(bot, ctx, command, *args)


@bot.command(pass_context=True)
async def рейтинг(ctx, *args):
    await jager_cmd.rating(ctx, *args)


@bot.command(pass_context=True)
async def запомни(ctx, command, *args):
    await jager_cmd.register_user(bot, ctx, command, *args)


"""   Сезонные события   """

async def daily_loop():
    await asyncio.sleep(10)
    time_alarm = "19:00"
    while True:
        time_now = time.strftime("%H:%M", time.localtime())
        if time_now == time_alarm:
            # Обновление таблицы лидеров и награды
            await jager_season.update_daily_event_r6(bot)
        elif time_now[3:] == "15" or time_now[3:] == "45":
            # Обновление таблицы лидеров каждый час
            await jager_season.update_table_r6(bot)
        await asyncio.sleep(60)


def main():
    bot.loop.create_task(daily_loop())
    bot.run(TOKEN)


if __name__ == "__main__":
    main()

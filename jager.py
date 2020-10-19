import asyncio
import random
import threading
from prettytable import PrettyTable

import discord
import r6sapi as api
import time
from discord.ext import commands

import jager_phrases as phrases
import jager_maps as r6_maps

import jager_function.events as jager_event
import jager_function.commands as jager_cmd


# TOKEN = 'Your token'
# email = "Your email"
# password = "Your Password"
TOKEN = "NzAwMzUyMTg3MjE3MjE1NTU5." + "Xtpr8Q.pyZIcYBL7cyiqINLgyiogRx8ThY"  # Чтобы не переделывать токен
email = "hunterbot.jager@bk.ru"
password = "Jagerthebest01"
bot = commands.Bot(command_prefix='Ягер ')


EU = api.RankedRegions.EU
channel_memory_id = 701698041660309574
channel_memory = None

emoji_roles = {756609869326581840: 'Apex Legends', 756609380593434654: 'Dota 2',
               756609572172595380: 'Counter-Strike', 700596539499872256: 'R6', 701007348730167346: 'PUBG',
               756611247889317918: 'Valorant', 761243822716878859: 'Imposter'}

""" Синхронные функции """


def get_random_item(array):
    index_arr = random.randint(0, len(array) - 1)
    return array[index_arr]


""" Асинхронные функции """


async def is_required_role(guild, role, name_required_role):
    required_role = discord.utils.get(guild.roles, name=name_required_role)
    return role >= required_role


async def clear_channel(channel, n=1000):
    async for message in channel.history(limit=n):
        await message.delete()


""" Память бота """


async def get_all_memory():
    list_messages = []
    channel_memory = await bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        list_messages.append(message.content)
    return list_messages


async def get_nicks_memory():
    list_players = []
    channel_memory = await bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        list_players.append(message.content.split()[1])
    return list_players


async def get_nick_and_message_memory(user_id):
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        if message.content.startswith(str(user_id)):
            return message.content.split()[1], message
    return None, None


""" Статистика R6 """


async def get_player_batch_r6(list_nicks):
    auth = api.Auth(email, password)
    player_batch = []
    for nick in list_nicks:
        try:
            player = await auth.get_player(nick, api.Platforms.UPLAY)
            player_batch.append(player)
        except ConnectionError:
            continue
    return player_batch





""" Стандартные события """

@bot.event
async def on_ready():
    jager_event.on_ready(bot)
    channel_memory = bot.get_channel(channel_memory_id)

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


""" Разговор с ботом """


@bot.command(pass_context=True)
async def привет(ctx):
    text = get_random_item(phrases.hello).format(str(ctx.message.author.name))
    await ctx.send(text)


@bot.command(pass_context=True)
async def как(ctx, arg):
    if arg == 'научиться' or arg == 'играть':
        text = "Никак. Удали к чертям эту игру!"
        await ctx.send(text)


@bot.command(pass_context=True)
async def инструкция(ctx):
    await jager_cmd.instruction(bot, ctx)


""" Работа с чатом """


@bot.command(pass_context=True)
async def удали(ctx, arg):
    await jager_cmd.delete_message(ctx, arg)


@bot.command(pass_context=True)
async def меню_группировок(ctx):
    await jager_cmd.menu(bot, emoji_roles)


@bot.command(pass_context=True)
async def дай(ctx, command, *args):
    await jager_cmd.get_something(ctx, command, *args)
    # if command == "карту":
    #     map_name = args[0]
    #     await r6_maps.send_map(ctx, map_name)
    # if command == "статистику":
    #     if args[0] == "мою":
    #         nick, message = await get_nick_and_message_memory(ctx.author.id)
    #         if nick is None:
    #             await ctx.send('Я не знаю твоего ника в R6. Но я могу запомнить тебя!\n'
    #                            'Пример: `Ягер запомни меня KriptYashka`')
    #         await jager_cmd.send_statistic_r6(ctx, [nick])
    #     else:
    #         await jager_cmd.send_statistic_r6(ctx, args)


@bot.command(pass_context=True)
async def рейтинг(ctx, *args):
    pass


@bot.command(pass_context=True)
async def запомни(ctx, command, *args):
    """ Структура сообщения:
                ID Discord - R6 Nick - Wins - Kills """
    # Обработка ошибок
    if command != "меня":
        return await ctx.send("Что мне запоминать?\nЕсли ты забыл команды - смотри инструкцию")
    if len(args) == 0:
        emoji_r6 = str(bot.get_emoji(700596539499872256))
        return await ctx.send(
            "Не могу. Мне нужен твой ник в R6 {}\nПример: `Ягер запомни меня KriptYashka`".format(emoji_r6))

    nick, message = await get_nick_and_message_memory(ctx.author.id)
    if nick is not None:
        if nick == args[0]:
            return await ctx.send(get_random_item(phrases.ready) + "\nХа! Я тебя и так знаю =)")
        # Существующий пользователь
        try:
            auth = api.Auth(email, password)
            player = await auth.get_player(args[0], api.Platforms.UPLAY)
        except ConnectionError:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
        await player.load_general()
        new_content = "{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills)
        await message.edit(content=new_content)
        return await ctx.send(get_random_item(phrases.ready) + "\nНо я перезаписал твой ник:\n"
                                                               "**{}** --> **{}**".format(nick, args[0]))
    else:
        # Новый пользователь
        channel_memory = bot.get_channel(channel_memory_id)
        try:
            auth = api.Auth(email, password)
            player = await auth.get_player(args[0], api.Platforms.UPLAY)
        except ConnectionError:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
        await player.load_general()
        await channel_memory.send("{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills))
        await ctx.send("Запомнил!")
    await auth.close()


""" Сезонные события """


async def get_table_r6():
    list_messages = await get_all_memory()
    auth = api.Auth(email, password)
    list_id, list_nicks, list_wins, list_kills = [], [], [], []
    player_batch = []
    for item in list_messages:
        try:
            player = await auth.get_player(name=item.split()[1], platform=api.Platforms.UPLAY)
            await player.load_general()
            player_batch.append(player)

            list_id.append(item.split()[0])
            list_nicks.append(item.split()[1])
            list_wins.append(item.split()[2])
            list_kills.append(item.split()[3])
        except:
            continue
    await auth.close()

    table_top = PrettyTable(["Игрок", "Ник", "Победы", "Убийства"])
    i = -1
    for player in player_batch:
        i += 1
        current_kills = int(list_kills[i])
        current_wins = int(list_wins[i])
        delta_wins = player.matches_won - current_wins
        delta_kills = player.kills - current_kills
        if delta_kills == 0 and delta_wins == 0:
            continue

        try:
            table_top.add_row([bot.get_user(int(list_id[i])).name, list_nicks[i], delta_wins, delta_kills])
        except:
            table_top.add_row(["Не запомнил", list_nicks[i], delta_wins, delta_kills])


    table_top.sortby = "Убийства"
    table_top.reversesort = True

    return table_top


async def send_table_r6(channel=bot.get_channel(703705481876733983)):


    table_top = await get_table_r6()
    emoji_r6 = str(bot.get_emoji(700596539499872256))
    return await channel.send("^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^\n\n"
                              "{}          **Таблица лидеров**          {}"
                              "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^```python\n".format(emoji_r6, emoji_r6)
                              + str(table_top) + "```")


async def update_daily_data_r6(player_batch):
    channel_memory = bot.get_channel(channel_memory_id)
    players = [player for player in player_batch]
    i = 0
    async for message in channel_memory.history():
        new_content = message.content.replace(message.content.split()[2], str(players[i].matches_won))
        new_content = new_content.replace(message.content.split()[3], str(players[i].kills))
        await message.edit(content=new_content)
        i += 1


async def update_table_r6():
    guild = bot.get_guild(700357287700594708)
    channel_tops = guild.get_channel(703705481876733983)
    await clear_channel(channel_tops, 1)
    await send_table_r6(channel_tops)


async def update_daily_event_r6():
    auth = api.Auth(email, password)
    guild = bot.get_guild(700357287700594708)
    channel_tops = guild.get_channel(703705481876733983)
    role = guild.get_role(703744789035876393)  # Выдача роли
    list_messages = await get_all_memory()
    for member in guild.members:
        await member.remove_roles(role)
    list_id, list_nicks, list_wins, list_kills = [], [], [], []
    player_batch = []

    for item in list_messages:
        list_id.append(item.split()[0])
        list_wins.append(item.split()[2])
        list_kills.append(item.split()[3])
        try:
            player = await auth.get_player(name=item.split()[1], platform=api.Platforms.UPLAY)
            await player.load_general()
            player_batch.append(player)
            list_nicks.append(item.split()[1])
        except:
            list_nicks.append("Игрок сменил никнейм")
            continue

    max_wins, max_kills = -1, -1
    winner_id, killer_id = None, None
    winner_nick, killer_nick = None, None
    await auth.close()

    i = -1
    for player in player_batch:
        i += 1
        if list_nicks[i] == "Игрок сменил никнейм":
            continue
        current_id = int(list_id[i])
        current_kills = int(list_kills[i])
        current_wins = int(list_wins[i])

        delta_wins = player.matches_won - current_wins
        delta_kills = player.kills - current_kills
        if delta_kills == 0 and delta_wins == 0:
            continue

        if max_wins < delta_wins:
            winner_id = current_id
            winner_nick = list_nicks[i]
            max_wins = delta_wins
        if max_kills < delta_kills:
            killer_id = current_id
            killer_nick = list_nicks[i]
            max_kills = delta_kills

    if killer_id is None and winner_id is None:
        return

    killer = "<@" + str(killer_id) + ">"
    winner = "<@" + str(winner_id) + ">"
    emoji_r6 = str(bot.get_emoji(700596539499872256))

    text = "{}     **Герои дня**     {}\n^^^^^^^^^^^^^^^^^^^^^\n".format(emoji_r6, emoji_r6)
    text += "**Герой убийств {}**:\n".format(killer_nick)
    text += get_random_item(phrases.top_killer).format(killer, max_kills) + "\n\n"
    text += "**Герой побед {}**:\n".format(winner_nick)
    text += get_random_item(phrases.top_winner).format(winner, max_wins)
    text += "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
    text += "\nЖелаю хорошего настроения!"

    await guild.get_member(killer_id).add_roles(role)
    await guild.get_member(winner_id).add_roles(role)

    await clear_channel(channel_tops)
    await channel_tops.send(text)
    await send_table_r6(channel_tops)
    await update_daily_data_r6(player_batch)
    

async def daily_loop():
    await asyncio.sleep(10)
    time_alarm = "19:00"
    while True:
        time_now = time.strftime("%H:%M", time.localtime())
        if time_now == time_alarm:
            # Обновление таблицы лидеров и награды
            await update_daily_event_r6()
        elif time_now[3:] == "15" or time_now[3:] == "45":
            # Обновление таблицы лидеров каждый час
            await update_table_r6()
        await asyncio.sleep(60)


async def start_bot():
    pass


def run_bot_forever(loop_bot):
    loop_bot.run_forever()


def main():
    bot.loop.create_task(daily_loop())
    bot.run(TOKEN)


if __name__ == "__main__":
    main()

import asyncio
import random
import threading
from prettytable import PrettyTable

import discord
import r6sapi as api
import time
from discord.ext import commands

import jager_phrases as phrases
import maps

bot = commands.Bot(command_prefix='Ягер ')
# TOKEN = 'Your token'
# email = "Your email"
# password = "Your Password"

EU = api.RankedRegions.EU
channel_memory_id = 701698041660309574

emoji_roles = {701007355956953148: 'Ассасин', 701007347904151605: 'Наёмник',
               701007349338603570: 'Док', 701007348730167346: 'Военный', 701007347534921750: 'Анархист'}


def get_random_item(array):
    index_arr = random.randint(0, len(array) - 1)
    return array[index_arr]


async def clear_channel(channel, n=1000):
    async for message in channel.history(limit=n):
        await message.delete()


async def find_players(list_nicks):
    auth = api.Auth(email, password)
    player_batch = []
    for nick in list_nicks:
        player = await auth.get_player(nick, api.Platforms.UPLAY)
        player_batch.append(player)
    return player_batch


async def find_all_in_memory():
    list_messages = []
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        list_messages.append(message.content)
    return list_messages


async def find_nicks_in_memory():
    list_players = []
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        list_players.append(message.content.split()[1])
    return list_players


async def find_nick_in_memory(user_id):
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        if message.content.startswith(str(user_id)):
            return message.content.split()[1], message
    return None, None


async def is_required_role(guild, role, name_required_role):
    required_role = discord.utils.get(guild.roles, name=name_required_role)
    return role >= required_role


async def give_role(ctx, role_name):
    member = ctx.author
    server = ctx.guild
    role = discord.utils.get(server.roles, name=role_name)
    if role is None:
        return await ctx.send('Нет такой роли. Не трать моё время!')
    if role_name == 'Бармен':
        return await ctx.send('Нее, браток. У нас бармен единственный - **KriptYashka**.')
    await member.add_roles(role)
    await ctx.send(get_random_item(phrases.ready))


async def send_statistic_r6(ctx, nicks):
    await ctx.send(get_random_item(phrases.ready))
    auth = api.Auth(email, password)
    for nick in nicks:
        try:
            player = await auth.get_player(nick, api.Platforms.UPLAY)
        except:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
            continue
        await player.load_general()
        rank = await player.get_rank(EU)
        mmr = int(rank.mmr)

        hours = int(player.time_played / 60 / 60)
        if 2 <= hours % 10 <= 4:
            str_hours = str(hours) + " часа"
        elif hours % 10 == 1:
            str_hours = str(hours) + " час"
        else:
            str_hours = str(hours) + " часов"

        embed = discord.Embed(title="Статистика " + nick, color=0x7d17bb)
        embed.set_author(name="Rainbow Six: Siege", icon_url=player.icon_url)
        embed.set_thumbnail(
            url=rank.get_icon_url())
        embed.add_field(name="Текущее звание:", value=rank.get_bracket_name(), inline=True)
        embed.add_field(name="Рейтинг:", value=str(mmr), inline=False)
        embed.add_field(name="Убийства: ", value=player.kills, inline=True)
        embed.add_field(name="Смерти", value=player.deaths, inline=True)
        embed.add_field(name="Убийства/Смерти:", value="{:.2f}"
                        .format(player.kills / player.deaths), inline=True)
        embed.add_field(name="Победы:", value=player.matches_won, inline=True)
        embed.add_field(name="Поражения:", value=player.matches_lost, inline=True)
        embed.add_field(name="Победы/Поражения:", value="{:.2f}"
                        .format(player.matches_won / player.matches_lost), inline=True)
        embed.add_field(name="Время игры:", value=str_hours, inline=False)

        await ctx.send(embed=embed)
    auth.close()


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


@bot.command(pass_context=True)
async def привет(ctx):
    text = get_random_item(phrases.hello).format(str(ctx.message.author.name))
    await ctx.send(text)


@bot.command(pass_context=True)
async def эхо(ctx, args):
    text = args
    await ctx.send(text)


@bot.command(pass_context=True)
async def как(ctx, arg):
    if arg == 'научиться' or arg == 'играть':
        text = "Никак. Удали к чертям эту игру!"
        await ctx.send(text)


@bot.command(pass_context=True)
async def удали(ctx, arg):
    member = ctx.message.author
    required_role = discord.utils.get(ctx.guild.roles, name="Матёрый")
    if member.top_role < required_role:
        return await ctx.send(phrases.no_roots)
    await ctx.send(get_random_item(phrases.ready))
    if arg == 'все' or arg == 'всё' or arg is None:
        await clear_channel(ctx.channel)
    else:
        n = int(arg)
        await clear_channel(ctx.channel, n + 2)


@bot.command(pass_context=True)
async def меню_группировок(ctx):
    channel_role = bot.get_channel(700806731260755978)
    await clear_channel(channel_role)
    text = "Пока сервер развивается, я мало что могу сделать для тебя.\nХоть ты и так **охотник**, " \
           "наверное, но я могу отнести тебя к какой хочешь групировке..."
    for item in emoji_roles.items():
        text += "\n - " + str(bot.get_emoji(item[0])) + " " + item[1]
    text += "\nВыбирай одну роль."

    message = await channel_role.send(text)
    for id_emoji in emoji_roles:
        await message.add_reaction(bot.get_emoji(id_emoji))


@bot.command(pass_context=True)
async def дай(ctx, command, *args):
    if command == "роль":
        role_name = args[0]
        if is_required_role(ctx.guild, ctx.author.top_role, "Матерый"):
            await give_role(ctx, role_name)
    if command == "карту":
        map_name = args[0]
        await maps.send_map(ctx, map_name)
    if command == "статистику":
        if args[0] == "мою":
            nick, message = await find_nick_in_memory(ctx.author.id)
            if nick is None:
                await ctx.send('Я не знаю твоего ника в R6. Но я могу запомнить тебя!\n'
                               'Пример: `Ягер запомни меня KriptYashka`')
            await send_statistic_r6(ctx, [nick])
        else:
            await send_statistic_r6(ctx, args)


@bot.command(pass_context=True)
async def мут(ctx):
    member = ctx.author
    guild = ctx.guild
    print(member.top_role)
    if await is_required_role(guild, member.top_role, "Охотник"):
        channel = member.voice.channel
        pass


@bot.command(pass_context=True)
async def рейтинг(ctx, *args):
    auth = api.Auth(email, password)
    await ctx.send(get_random_item(phrases.ready))
    if args[0] == "вместе":
        nicks = args[1:]
        max_rank = 0
        min_rank = 10000
        for nick in nicks:
            try:
                player = await auth.get_player(nick, api.Platforms.UPLAY)
            except:
                await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
                continue
            rank = await player.get_rank(EU)
            max_rank = max(max_rank, int(rank.mmr))
            min_rank = min(min_rank, int(rank.mmr))
        delta = max_rank - min_rank
        str_delta = "Текущая разница: " + str(delta) + " MMR"
        if delta >= 1000:
            text = "К сожалению, вы не сможете сыграть... \n" + str_delta
        else:
            text = "Можно играть без проблем! \n" + str_delta
        return await ctx.send(text)
    nicks = args[:]
    for nick in nicks:
        try:
            player = await auth.get_player(nick, api.Platforms.UPLAY)
        except:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
            continue
        rank = await player.get_rank(EU)
        await ctx.send("**" + nick + "** - " + str(int(rank.mmr)) + ' MMR')
    await auth.close()


@bot.command(pass_context=True)
async def запомни(ctx, command, *args):
    if command != "меня":
        return await ctx.send("Что мне запоминать?\nЕсли ты забыл команды - смотри инструкцию")
    if len(args) == 0:
        emoji_r6 = str(bot.get_emoji(700596539499872256))
        return await ctx.send(
            "Не могу. Мне нужен твой ник в R6 {}\nПример: `Ягер запомни меня KriptYashka`".format(emoji_r6))
    nick, message = await find_nick_in_memory(ctx.author.id)
    if nick is not None:
        if nick == args[0]:
            return await ctx.send(get_random_item(phrases.ready) + "\nХа! Я тебя и так знаю =)")
        else:
            try:
                auth = api.Auth(email, password)
                player = await auth.get_player(args[0], api.Platforms.UPLAY)
                await player.load_general()
            except:
                await ctx.send('Хмм... Игрока {} не существует.'.format(nick))

            new_content = "{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills)
            await message.edit(content=new_content)
            return await ctx.send(get_random_item(phrases.ready) + "\nНо я перезаписал твой ник:\n"
                                                                   "**{}** --> **{}**".format(nick, args[0]))
    channel_memory = bot.get_channel(channel_memory_id)
    try:
        auth = api.Auth(email, password)
        player = await auth.get_player(args[0], api.Platforms.UPLAY)
        await player.load_general()
        auth.close()
        await channel_memory.send("{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills))
        await ctx.send("Запомнил!")
    except:
        await ctx.send('Хмм... Игрока {} не существует.'.format(nick))


@bot.command(pass_context=True)
async def инструкция(ctx):
    await clear_channel(ctx.channel, 1)
    guild_name = ctx.guild.name
    emoji = str(bot.get_emoji(701757818965065759))  # Pulse
    emoji_point = str(bot.get_emoji(700599296650903583))
    emoji_r6 = str(bot.get_emoji(700596539499872256))
    text = "{} Привет, ты на сервере **{}** {}\n\n".format(emoji, guild_name, emoji)
    text += "Если ты не знаком с правиами, советую тебе посмотреть их. Здесь очень много интересного" \
            " и самое главное - приятное окружение.\n\n"
    text += "Что я сообственно могу:\n\n"

    text += "{} `Ягер привет` - поздороваться с тобой\n\n".format(emoji_point)
    text += "{} `Ягер дай статистику UPlayNick1 UPlayNick2...` - найду основную статистику в R6 {}\n\n".format(
        emoji_point, emoji_r6)
    text += "{} `Ягер рейтинг UPlayNick1 UPlayNick2...` - скину MMR каждого игрока.\n\n".format(emoji_point)
    text += "{} `Ягер рейтинг вместе UPlayNick1 UPlayNick2...`" \
            " - проанализирую, можно ли вам идти в рейтинг.\n\n".format(emoji_point)
    text += "{} `Ягер запомни меня UPlayNick` - постараюсь запомнить, как выглядит твой ник. Но это не точно =)\n\n" \
        .format(emoji_point)
    text += "{} `Ягер инструкция` - покажу тебе ещё раз, что я умею.\n\n".format(emoji_point)
    await ctx.send(text)


def create_table(player_batch, list_messages):
    list_id, list_nicks, list_wins, list_kills = [], [], [], []
    for item in list_messages:
        list_id.append(item.split()[0])
        list_nicks.append(item.split()[1])
        list_wins.append(item.split()[2])
        list_kills.append(item.split()[3])

    table_top = PrettyTable(["Охотник", "Ник", "Победы", "Убийства"])
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


async def send_table(channel=bot.get_channel(703705481876733983), player_batch=None):
    list_nicks = await find_nicks_in_memory()
    if player_batch is None:
        auth = api.Auth(email, password)
        player_batch = await auth.get_player_batch(names=list_nicks, platform=api.Platforms.UPLAY)
        await player_batch.load_general()
        await auth.close()
    table_top = create_table(player_batch, await find_all_in_memory())
    emoji_r6 = str(bot.get_emoji(700596539499872256))
    return await channel.send("^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^\n\n"
                              "{}          **Таблица лидеров**          {}"
                              "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^```python\n".format(emoji_r6, emoji_r6)
                              + str(table_top) + "```")


async def reset_daily_data(player_batch):
    channel_memory = bot.get_channel(channel_memory_id)
    players = [player for player in player_batch]
    i = 0
    async for message in channel_memory.history():
        new_content = message.content.replace(message.content.split()[2], str(players[i].matches_won))
        new_content = new_content.replace(message.content.split()[3], str(players[i].kills))
        await message.edit(content=new_content)
        i += 1


async def server_tops_table():
    guild = bot.get_guild(700357287700594708)
    channel_tops = guild.get_channel(703705481876733983)
    await clear_channel(channel_tops, 1)
    await send_table(channel_tops)


async def server_tops():
    auth = api.Auth(email, password)
    guild = bot.get_guild(700357287700594708)
    channel_tops = guild.get_channel(703705481876733983)
    role = guild.get_role(703744789035876393)
    list_messages = await find_all_in_memory()
    for member in guild.members:
        await member.remove_roles(role)
    list_id, list_nicks, list_wins, list_kills = [], [], [], []
    for item in list_messages:
        list_id.append(item.split()[0])
        list_nicks.append(item.split()[1])
        list_wins.append(item.split()[2])
        list_kills.append(item.split()[3])

    player_batch = await auth.get_player_batch(names=list_nicks, platform=api.Platforms.UPLAY)
    await player_batch.load_general()
    max_wins, max_kills = -1, -1
    winner_id, killer_id = None, None
    winner_nick, killer_nick = None, None
    i = -1
    await auth.close()

    for player in player_batch:
        i += 1
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
    if killer_id is not None and winner_id is not None:
        killer = "<@" + str(killer_id) + ">"
        winner = "<@" + str(winner_id) + ">"
        everyone = "@everyone"
        emoji_r6 = str(bot.get_emoji(700596539499872256))
        text = "{}     **Герои дня**     {}\n^^^^^^^^^^^^^^^^^^^^^\n".format(emoji_r6, emoji_r6)
        text += "**Герой убийств {}**:\n".format(killer_nick)
        text += get_random_item(phrases.top_killer).format(killer, max_kills) + "\n\n"
        text += "**Герой побед {}**:\n".format(winner_nick)
        text += get_random_item(phrases.top_winner).format(winner, max_wins)
        text += "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
        text += "\n{} Желаю хорошего настроения!".format(everyone)

        await guild.get_member(killer_id).add_roles(role)
        await guild.get_member(winner_id).add_roles(role)
    else:
        text = "Упс... Никто сегодня не играл..."
    await clear_channel(channel_tops)
    await channel_tops.send(text)
    await send_table(channel_tops, player_batch)
    await reset_daily_data(player_batch)


async def daily_loop():
    await asyncio.sleep(10)
    time_alarm = "19:00"
    while True:
        time_now = time.strftime("%H:%M", time.localtime())
        if time_now == time_alarm:
            await server_tops()
        elif time_now[3:] == "22":
            await server_tops_table()
        await asyncio.sleep(60)


async def start_bot():
    bot.loop.create_task(daily_loop())
    await bot.start(TOKEN)


def run_bot_forever(loop_bot):
    loop_bot.run_forever()


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    thread_bot = threading.Thread(target=run_bot_forever, args=(loop,))
    thread_bot.start()

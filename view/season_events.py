from view.global_variable import *

import view.data as data
from prettytable import PrettyTable
from view.commands import clear_channel


async def get_table_r6(bot):
    list_messages = await data.get_all_memory(bot)
    auth = api.Auth(jager_email, jager_password)
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


async def send_table_r6(bot, channel):
    if channel is None:
        channel = bot.get_channel(703705481876733983)

    table_top = await get_table_r6(bot)
    emoji_r6 = str(bot.get_emoji(700596539499872256))
    return await channel.send("^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^     ^\n\n"
                              "{}          **Таблица лидеров**          {}"
                              "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^```python\n".format(emoji_r6, emoji_r6)
                              + str(table_top) + "```")


async def update_daily_data_r6(bot, player_batch):
    channel_memory = data.get_channel_memory(bot)
    players = [player for player in player_batch]
    i = 0
    async for message in channel_memory.history():
        new_content = message.content.replace(message.content.split()[2], str(players[i].matches_won))
        new_content = new_content.replace(message.content.split()[3], str(players[i].kills))
        await message.edit(content=new_content)
        i += 1


async def update_table_r6(bot):
    guild = bot.get_guild(700357287700594708)
    channel_tops = guild.get_channel(703705481876733983)
    await clear_channel(channel_tops, 1)
    await send_table_r6(bot, channel_tops)


async def update_daily_event_r6(bot):
    """
    Обновляет списки рейтингов игроков R6. Перезаписывает статистику в память.
    """
    auth = api.Auth(jager_email, jager_password)
    guild = bot.get_guild(700357287700594708)
    channel_tops = guild.get_channel(703705481876733983)
    role = guild.get_role(703744789035876393)  # Выдача роли
    list_messages = await data.get_all_memory(bot)
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
    await send_table_r6(bot, channel_tops)
    await update_daily_data_r6(bot, player_batch)


async def send_random_msg(bot):
    channel = bot.get_channel(700465669522849802)
    await channel.send(get_random_item(phrases.random_message))
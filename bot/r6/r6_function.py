from module.module import *
from jager import email, password

EU = r6sapi.RankedRegions.EU

async def get_player_batch_r6(list_nicks):
    auth = r6sapi.Auth(email, password)
    player_batch = []
    for nick in list_nicks:
        try:
            player = await auth.get_player(nick, r6sapi.Platforms.UPLAY)
            player_batch.append(player)
        except ConnectionError:
            continue
    return player_batch


async def send_statistic_r6(ctx, nicks):
    await ctx.send(get_random_item(phrases.ready))
    auth = r6sapi.Auth(email, password)
    for nick in nicks:
        try:
            player = await auth.get_player(nick, r6sapi.Platforms.UPLAY)
        except ConnectionError:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
            continue
        await player.load_general()

        rank = await player.get_rank(EU)
        mmr = int(rank.mmr)
        hours = int(player.time_played / 60 / 60)

        # Лексика
        if 2 <= hours % 10 <= 4:
            str_hours = str(hours) + " часа"
        elif hours % 10 == 1:
            str_hours = str(hours) + " час"
        else:
            str_hours = str(hours) + " часов"

        # Формирование карточки
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
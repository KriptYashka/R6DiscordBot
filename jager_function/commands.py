import discord
import random
from jager_function.global_variable import *
from jager_function import jager_maps as r6_maps
import jager_function.data as data
from classes.classes import PlayerR6

def get_random_item(array):
    index_arr = random.randint(0, len(array) - 1)
    return array[index_arr]


async def clear_channel(channel, n=1000):
    async for message in channel.history(limit=n):
        await message.delete()

async def get_player_batch_r6(list_nicks):
    auth = api.Auth(jager_email, jager_password)
    player_batch = []
    for nick in list_nicks:
        try:
            player = await auth.get_player(nick, api.Platforms.UPLAY)
            player_batch.append(player)
        except:
            continue
    return player_batch


async def send_statistic_r6(ctx, nicks):
    await ctx.send(get_random_item(phrases.ready))
    for nick in nicks:
        player = PlayerR6(nick)
        hours = player.time_played

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
        embed.set_thumbnail(url=player.rank_url)
        embed.add_field(name="Текущее звание:", value=player.rank_name, inline=True)
        embed.add_field(name="Рейтинг:", value=str(player.mmr), inline=False)
        embed.add_field(name="Убийства: ", value=player.kills, inline=True)
        embed.add_field(name="Смерти", value=player.deaths, inline=True)
        embed.add_field(name="Убийства/Смерти:", value="{:.2f}".format(player.kills / player.deaths), inline=True)
        embed.add_field(name="Победы:", value=player.wins, inline=True)
        embed.add_field(name="Поражения:", value=player.loses, inline=True)
        embed.add_field(name="Победы/Поражения:", value="{:.2f}".format(player.wins / player.loses), inline=True)
        embed.add_field(name="Время игры:", value=str_hours, inline=False)
        await ctx.send(embed=embed)


async def instruction(bot, ctx):
    await clear_channel(ctx.channel, 1)
    guild_name = ctx.guild.name
    emoji_pulse = str(bot.get_emoji(701757818965065759))  # Pulse
    emoji_point = str(bot.get_emoji(700599296650903583))
    emoji_r6 = str(bot.get_emoji(700596539499872256))
    text = "{} Привет, ты на сервере **{}** {}\n\n".format(emoji_pulse, guild_name, emoji_pulse)
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


async def delete_message(ctx, arg):
    member = ctx.message.author
    # Требуемая роль для выполнения команды
    role = discord.utils.get(member.guild.roles, name="Матёрый")
    if member.top_role < role:
        return await ctx.send(get_random_item(phrases.no_roots))

    if arg == 'все' or arg == 'всё' or arg is None:
        await clear_channel(ctx.channel)
    else:
        n = int(arg)
        await clear_channel(ctx.channel, n + 1)


async def menu(bot, emoji_roles):
    channel_role = bot.get_channel(700806731260755978)

    text = "Привет! Выбирай, в какую игру ты играешь, чтобы скорее найти себе друзей ^_^:\n"
    for item in emoji_roles.items():
        text += "\n - " + str(bot.get_emoji(item[0])) + " " + item[1]
    text += "\n\n**Have a good day**!"

    message = await channel_role.send(text)
    for id_emoji in emoji_roles:
        await message.add_reaction(bot.get_emoji(id_emoji))


async def get_something(bot, ctx, command, *args):
    if command == "карту":
        map_name = args[0]
        await r6_maps.send_map(ctx, map_name)
    if command == "статистику":
        if args[0] == "мою":
            nick, message = await data.get_nick_and_message_memory(bot, ctx.author.id)
            if nick is None:
                await ctx.send('Я не знаю твоего ника в R6. Но я могу запомнить тебя!\n'
                               'Пример: `Ягер запомни меня KriptYashka`')
            await send_statistic_r6(ctx, [nick])
        else:
            await send_statistic_r6(ctx, args)


async def rating(ctx, *args):
    await ctx.send(get_random_item(phrases.ready))
    if args[0] == "вместе":
        # Совместимость игроков для рейтинга
        nicks = args[1:]
        max_rank = 0
        min_rank = 10000
        for nick in nicks:
            player = PlayerR6(nick)
            mmr = player.mmr
            max_rank = max(max_rank, mmr)
            min_rank = min(min_rank, mmr)
        delta = max_rank - min_rank
        str_delta = "Текущая разница: " + str(delta) + " MMR"
        if delta >= 1000:
            text = "К сожалению, вы не сможете сыграть... \n" + str_delta
        else:
            text = "Можно играть без проблем! \n" + str_delta
        await ctx.send(text)
    else:
        # Рейтинг игроков по отдельности
        nicks = args[:]
        for nick in nicks:
            await ctx.send("**" + nick + "** - " + str(PlayerR6(nick).mmr) + ' MMR')


async def register_user(bot, ctx, command, *args):
    """ Структура сообщения:
                ID Discord - R6 Nick - Wins - Kills """
    # Обработка ошибок
    if command != "меня":
        return await ctx.send("Что мне запоминать?\nЕсли ты забыл команды - смотри инструкцию")
    if len(args) == 0:
        emoji_r6 = str(bot.get_emoji(700596539499872256))
        return await ctx.send(
            "Не могу. Мне нужен твой ник в R6 {}\nПример: `Ягер запомни меня KriptYashka`".format(emoji_r6))

    nick, message = await data.get_nick_and_message_memory(bot, ctx.author.id)
    if nick is not None:
        if nick == args[0]:
            return await ctx.send(get_random_item(phrases.ready) + "\nХа! Я тебя и так знаю =)")
        # Существующий пользователь
        try:
            auth = api.Auth(jager_email, jager_password)
            player = await auth.get_player(args[0], api.Platforms.UPLAY)
            await player.load_general()
            new_content = "{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills)
            await message.edit(content=new_content)
            await auth.close()
            return await ctx.send(get_random_item(phrases.ready) + "\nНо я перезаписал твой ник:\n"
                                                                   "**{}** --> **{}**".format(nick, args[0]))
        except:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))

    else:
        # Новый пользователь
        channel_memory = data.get_channel_memory(bot)
        try:
            auth = api.Auth(jager_email, jager_password)
            player = await auth.get_player(args[0], api.Platforms.UPLAY)
            await player.load_general()
            await channel_memory.send(
                "{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills))
            await ctx.send("Запомнил!")
            await auth.close()
        except:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))


async def echo(ctx, words):
    await clear_channel(ctx.channel, 1)
    await ctx.send(words)
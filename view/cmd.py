import discord
from view.global_variable import *
from view import r6maps as r6_maps
import view.data as data
from classes.PlayerR6 import PlayerR6
from classes.Database import DataBaseR6
from discord.ext import commands


async def send_statistic_r6(ctx, nicks):
    for nick in nicks:
        player = PlayerR6(nick)
        await player.load_stats()
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
        embed.add_field(name="Поражения:", value=player.losses, inline=True)
        embed.add_field(name="Победы/Поражения:", value="{:.2f}".format(player.wins / player.losses), inline=True)
        embed.add_field(name="Время игры:", value=str_hours, inline=False)
        await ctx.send(embed=embed)


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
    #  Возвращает карты из R6
    if command == "карту":
        map_name = args[0]
        await r6_maps.send_map(ctx, map_name)

    #  Возвращает статистику
    if command == "статистику":
        #  Пользователя из БД
        if args[0] == "мою":
            nick, message = await data.get_nickname(bot, ctx.author.id)
            if nick is None:
                await ctx.send('Я не знаю твоего ника в R6. Но я могу запомнить тебя!\n'
                               'Пример: `Ягер запомни меня KriptYashka`')  # TODO: Рандомные фразы
            await send_statistic_r6(ctx, [nick])
        #  Пользователя с никнеймом
        else:
            await send_statistic_r6(ctx, args)


async def get_statistic_player_r6(bot: commands.Bot, message: discord.Message):
    args = message.content.split()[2:]
    if len(args) == 0:
        # Статистика зарегистрированного игрока
        pass


async def rating(bot: commands.Bot, message: discord.Message):
    """ Проверяет игроков на совместимость рейтинга """
    await ctx.send(phrases.get_ready())

    #  Совместимость игроков для рейтинга
    if args[0] == "вместе":
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
    # Рейтинг игроков по отдельности
    else:
        nicks = args[:]
        for nick in nicks:
            await ctx.send("**" + nick + "** - " + str(PlayerR6(nick).mmr) + ' MMR')


async def register_user(bot: commands.Bot, message: discord.Message):
    """ Структура сообщения:
                ID Discord - R6 Nick - Wins - Kills """
    # Обработка ошибок
    words = message.content.split()
    ctx = message.channel

    if len(words) <= 4:
        return await ctx.send(phrases.get_incorrect_input())
    args = words[2:]

    if args[0].lower() != "меня":
        return await ctx.send("Возможно, ты хотел сказать `Ягер запомни меня NickName`")

    # При корректном вводе
    db_nick = data.get_nickname(bot, ctx.author.id)
    if db_nick is not None:
        await existing_user(db_nick, message, args[1])
    else:
        await new_user(args[1], message)


async def existing_user(nick, message: discord.Message, message_nick):
    if nick == message_nick:
        return await message.channel.send(phrases.get_random_phrase() + "\nХа! Я тебя и так знаю =)")
    # Перезапись имени пользователя
    try:
        db = DataBaseR6()
        db.update_player_nickname(message.author.id, message_nick)
        return await message.channel.send(phrases.get_random_phrase() +
                                          f"\nЯ перезаписал твой ник:\n**{nick}** --> **{message_nick}**")
    except:
        return await message.channel.send('Хмм... Игрока {} не существует.'.format(nick))


async def new_user(nick: str, message: discord.Message):
    db = DataBaseR6()
    player = PlayerR6(nick, message.author.id)
    # TODO: Если игрок не существует
    db.add_players(player)
    await message.channel.send(phrases.get_ready())  # TODO: Новая фраза о пользователе

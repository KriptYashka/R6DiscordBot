from jager import clear_channel, get_random_item, phrases, r6_maps, get_nick_and_message_memory, email, password, \
    api, EU
import discord

async def send_statistic_r6(ctx, nicks):
    await ctx.send(get_random_item(phrases.ready))
    auth = api.Auth(email, password)
    for nick in nicks:
        try:
            player = await auth.get_player(nick, api.Platforms.UPLAY)
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

async def get_something(ctx, command, args):
    if command == "карту":
        map_name = args[0]
        await r6_maps.send_map(ctx, map_name)
    if command == "статистику":
        if args[0] == "мою":
            nick, message = await get_nick_and_message_memory(ctx.author.id)
            if nick is None:
                await ctx.send('Я не знаю твоего ника в R6. Но я могу запомнить тебя!\n'
                               'Пример: `Ягер запомни меня KriptYashka`')
            await send_statistic_r6(ctx, [nick])
        else:
            await send_statistic_r6(ctx, args)

# async def rating():
#     auth = api.Auth(email, password)
#     await ctx.send(get_random_item(phrases.ready))
#     if args[0] == "вместе":
#         # Совместимость игроков для рейтинга
#         nicks = args[1:]
#         max_rank = 0
#         min_rank = 10000
#         for nick in nicks:
#             try:
#                 player = await auth.get_player(nick, api.Platforms.UPLAY)
#             except ConnectionError:
#                 await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
#                 continue
#             rank = await player.get_rank(EU)
#             max_rank = max(max_rank, int(rank.mmr))
#             min_rank = min(min_rank, int(rank.mmr))
#         delta = max_rank - min_rank
#         str_delta = "Текущая разница: " + str(delta) + " MMR"
#         if delta >= 1000:
#             text = "К сожалению, вы не сможете сыграть... \n" + str_delta
#         else:
#             text = "Можно играть без проблем! \n" + str_delta
#         await ctx.send(text)
#     else:
#         # Рейтинг игроков по отдельности
#         nicks = args[:]
#         for nick in nicks:
#             try:
#                 player = await auth.get_player(nick, api.Platforms.UPLAY)
#             except ConnectionError:
#                 await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
#                 continue
#             rank = await player.get_rank(EU)
#             await ctx.send("**" + nick + "** - " + str(int(rank.mmr)) + ' MMR')
#     await auth.close()
from module.module import *
from bot.r6.r6_function import *
from bot.r6.r6_maps import *
from jager import bot, email, password

@bot.command(pass_context=True)
async def дай(ctx, command, *args):
    if command == "карту":
        map_name = args[0]
        await send_map(ctx, map_name)
    if command == "статистику":
        if args[0] == "мою":
            nick, message = await get_nick_and_message_memory(ctx.author.id)
            if nick is None:
                await ctx.send('Я не знаю твоего ника в R6. Но я могу запомнить тебя!\n'
                               'Пример: `Ягер запомни меня KriptYashka`')
            await send_statistic_r6(ctx, [nick])
        else:
            await send_statistic_r6(ctx, args)


@bot.command(pass_context=True)
async def рейтинг(ctx, *args):
    auth = r6sapi.Auth(email, password)
    await ctx.send(get_random_item(phrases.ready))
    if args[0] == "вместе":
        # Совместимость игроков для рейтинга
        nicks = args[1:]
        max_rank = 0
        min_rank = 10000
        for nick in nicks:
            try:
                player = await auth.get_player(nick, r6sapi.Platforms.UPLAY)
            except ConnectionError:
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
        await ctx.send(text)
    else:
        # Рейтинг игроков по отдельности
        nicks = args[:]
        for nick in nicks:
            try:
                player = await auth.get_player(nick, r6sapi.Platforms.UPLAY)
            except ConnectionError:
                await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
                continue
            rank = await player.get_rank(EU)
            await ctx.send("**" + nick + "** - " + str(int(rank.mmr)) + ' MMR')
    await auth.close()


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
            auth = r6sapi.Auth(email, password)
            player = await auth.get_player(args[0], r6sapi.Platforms.UPLAY)
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
            auth = r6sapi.Auth(email, password)
            player = await auth.get_player(args[0], r6sapi.Platforms.UPLAY)
        except ConnectionError:
            await ctx.send('Хмм... Игрока {} не существует.'.format(nick))
        await player.load_general()
        await channel_memory.send("{} {} {} {}".format(str(ctx.author.id), args[0], player.matches_won, player.kills))
        await ctx.send("Запомнил!")
    await auth.close()
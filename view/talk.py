import discord
from discord.ext import commands

from view import phrases
from view.cmd import clear_channel


async def send_hello(bot: commands.Bot, message: discord.Message):
    await message.channel.send(phrases.get_hello(message.author.name))


async def send_how_to_play(bot: commands.Bot, message: discord.Message):
    await message.channel.send(phrases.get_how_to_play())


async def instruction(bot: commands.Bot, message: discord.Message):
    guild_name = message.guild.name
    emoji_pulse = str(bot.get_emoji(701757818965065759))
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
    await clear_channel(message.channel, 1)
    await message.send(text)


async def echo(bot: commands.Bot, message: discord.Message):
    await message.delete()
    await message.channel.send(message.content)

import discord
from discord.ext import commands
import random
import r6sapi as api
from flask import Flask, jsonify, render_template, request
import threading

application = Flask(__name__)

bot = commands.Bot(command_prefix='Ягер ')
# TOKEN = 'Your token'
# email = "Your email"
# password = "Your Password"

EU = api.RankedRegions.EU
channel_memory_id = 701698041660309574

text_np = ['Ну давай попробуем...', 'Ладно, щя сделаем.', 'Без проблем.',
           'Чуть синей изоленты и... Готово!', 'За **ACOG** сделаю всё, что угодно.',
           'Потерпи чуть, я не такой быстрый. У меня 2 скорости.\n*звуки плача*',
           'Ставлю **СОГ**.', 'Vierundzwanzigstundenglück!']
text_hello = ['Guten Tag, {}', 'Здаров {}', 'Привет {}', '{} и тебе привет.']
emoji_roles = {701007355956953148: 'Ассасин', 701007347904151605: 'Наёмник',
               701007349338603570: 'Док', 701007348730167346: 'Военный', 701007347534921750: 'Анархист'}


def get_random_item(array):
    index_arr = random.randint(0, len(array) - 1)
    return array[index_arr]


async def clear_channel(channel, n=1000):
    async for message in channel.history(limit=n):
        await message.delete()


async def find_nick_in_memory(user_id):
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        if message.content.startswith(str(user_id)):
            return message.content.split()[1]


async def give_role(ctx, role_name):
    member = ctx.message.author
    server = ctx.message.guild
    role = discord.utils.get(server.roles, name=role_name)
    if role is None:
        return await ctx.send('Нет такой роли. Не трать моё время!')
    if role_name == 'Бармен':
        return await ctx.send('Нее, браток. У нас бармен единственный - **KriptYashka**.')
    await member.add_roles(role)
    await ctx.send(get_random_item(text_np))


async def send_statistic_r6(ctx, nicks):
    # text_statistic = "**Статистика игрока {}** {}\n\n".format(nick, str(bot.get_emoji(700596539499872256)))
    await ctx.send(get_random_item(text_np))
    auth = api.Auth(email, password)
    for nick in nicks:
        player = await auth.get_player(nick, api.Platforms.UPLAY)
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
    print('{0.user} пришел на сервера'.format(bot))
    
    


@bot.event
async def on_member_join(member):
    server = member.guild
    role = discord.utils.get(server.roles, name='Новичок')
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
    print(emoji.id)
    if emoji_roles[emoji.id] is not None:
        role = discord.utils.get(member.guild.roles, name=emoji_roles[emoji.id])
        await member.remove_roles(role)


@bot.command(pass_context=True)
async def привет(ctx):
    text = get_random_item(text_hello).format(str(ctx.message.author.name))
    await ctx.send(text)


@bot.command(pass_context=True)
async def как(ctx, args):
    if args == 'научиться' or args == 'играть':
        text = "Никак. Удали к чертям эту игру!"
        await ctx.send(text)


@bot.command(pass_context=True)
async def удали(ctx, arg):
    member = ctx.message.author
    required_role = discord.utils.get(member.guild.roles, name="Матёрый")
    if member.top_role >= required_role:
        await ctx.send(get_random_item(text_np))
        if arg == 'все' or arg == 'всё' or arg is None:
            await clear_channel(ctx.channel)
        else:
            n = int(arg)
            await clear_channel(ctx.channel, n + 2)
    else:
        await ctx.send("Не превышайся. У тебя нет таких прав.")


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
        await give_role(ctx, args[0])
    if command == "статистику":
        if args[0] == "мою":
            nick = await find_nick_in_memory(ctx.author.id)
            if nick is None:
                await ctx.send('Я не знаю твоего ника в R6.')
        else:
            await send_statistic_r6(ctx, args)


@bot.command(pass_context=True)
async def рейтинг(ctx, *nicks):
    await ctx.send(get_random_item(text_np))
    auth = api.Auth(email, password)
    for nick in nicks:
        player = await auth.get_player(nick, api.Platforms.UPLAY)
        rank = await player.get_rank(EU)
        await ctx.send("**" + nick + "** - " + str(int(rank.mmr)) + ' MMR')
    await auth.close()


@bot.command(pass_context=True)
async def вместе(ctx, command, *nicks):
    if command != "рейтинг":
        return
    await ctx.send(get_random_item(text_np))
    auth = api.Auth(email, password)
    max_rank = 0
    min_rank = 10000
    for nick in nicks:
        player = await auth.get_player(nick, api.Platforms.UPLAY)
        rank = await player.get_rank(EU)
        max_rank = max(max_rank, int(rank.mmr))
        min_rank = min(min_rank, int(rank.mmr))
    delta = max_rank - min_rank
    if delta >= 1000:
        text = "К сожалению, вы не сможете сыграть... \nТекущая разница: " + str(delta) + " MMR"
    else:
        text = "Можно играть без проблем! \nТекущая разница: " + str(delta) + " MMR"
    await ctx.send(text)
    await auth.close()


@bot.command(pass_context=True)
async def запомни(ctx, command, *args):
    channel_memory = bot.get_channel(channel_memory_id)
    if command == "меня":
        user_id = ctx.author.id
        await channel_memory.send(str(user_id) + " " + args[0])
        await ctx.send(get_random_item(text_np))


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

    text += "{} `Ягер привет` - поздороваться с тобой\n\n".format(emoji_point, emoji_r6)
    text += "{} `Ягер дай статистику UPlayNick1 UPlayNick2...` - найду основную статистику в R6 {}\n\n".format(emoji_point,
                                                                                                   emoji_r6, emoji_r6)
    text += "{} `Ягер рейтинг UPlayNick1 UPlayNick2...` - скину MMR каждого игрока.\n\n".format(emoji_point, emoji_r6)
    text += "{} `Ягер вместе рейтинг UPlayNick1 UPlayNick2...`" \
            " - проанализирую, можно ли вам идти в рейтинг.\n{}\n".format(emoji_point, emoji_r6)
    text += "{} `Ягер запомни меня UPlayNick` - постараюсь запомнить, как выглядит твой ник. Но это не точно =)\n{}\n"\
        .format(emoji_point, emoji_r6)
    text += "{} `Ягер инструкция` - покажу тебе ещё раз, что я умею.\n{}\n".format(emoji_point, emoji_r6)
    await ctx.send(text)


@application.route('/')
def hello():
    return render_template('index.html')
    

if __name__ == "__main__":
    threading.Thread(target=bot.run(TOKEN)).join()
    #bot.run(TOKEN)
# if __name__ == "__main__":
#     from os import environ
#     threading.Thread(target=application.run(host='0.0.0.0', port=int(environ['PORT']))).join()
    

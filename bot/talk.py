from jager import *
from sync import *

@bot.command(pass_context=True)
async def привет(ctx):
    text = get_random_item(phrases.hello).format(str(ctx.message.author.name))
    await ctx.send(text)


@bot.command(pass_context=True)
async def как(ctx, arg):
    if arg == 'научиться' or arg == 'играть':
        text = "Никак. Удали к чертям эту игру!"
        await ctx.send(text)
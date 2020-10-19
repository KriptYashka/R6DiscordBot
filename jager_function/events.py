from jager import bot

@bot.event
async def on_ready():
    print("{0.user} пришел на сервера".format(bot))
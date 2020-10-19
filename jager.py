from module.module import *

from bot.command import *
from bot.r6.r6_cmd import *


bot = commands.Bot(command_prefix='Ягер ')
# TOKEN = 'Your token'
# email = "Your email"
# password = "Your Password"
TOKEN = "NzAwMzUyMTg3MjE3MjE1NTU5." + "Xtpr8Q.pyZIcYBL7cyiqINLgyiogRx8ThY"  # Чтобы не переделывать токен
email = "hunterbot.jager@bk.ru"
password = "Jagerthebest01"

emoji_roles = {756609869326581840: 'Apex Legends', 756609380593434654: 'Dota 2',
               756609572172595380: 'Counter-Strike', 700596539499872256: 'R6', 701007348730167346: 'PUBG',
               756611247889317918: 'Valorant'}

async def daily_loop():
    await asyncio.sleep(10)
    time_alarm = "19:00"
    while True:
        time_now = time.strftime("%H:%M", time.localtime())
        if time_now == time_alarm:
            # Обновление таблицы лидеров и награды
            await update_daily_event_r6()
        elif time_now[3:] == "15" or time_now[3:] == "45":
            # Обновление таблицы лидеров каждый час
            await update_table_r6()
        await asyncio.sleep(60)


def run_bot_forever(loop_bot):
    loop_bot.run_forever()


def main():
    bot.loop.create_task(daily_loop())
    bot.run(TOKEN)


if __name__ == "__main__":
    main()

from discord.ext import commands
from classes.Database import DataBaseR6


def get_nickname(bot: commands.Bot, discord_id: int):
    db = DataBaseR6()
    row = db.get_player_row_by_discord_id(discord_id)
    if row is None:
        return None
    return row["nickname"]


async def get_all_memory(bot):
    pass


async def get_nicks_memory(bot):
    pass

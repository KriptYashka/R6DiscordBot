import discord
import sqlite3
from discord.ext import commands
from classes.Database import DataBaseR6

channel_memory_id = 701698041660309574
guild_id = 700357287700594708


def get_channel_memory(bot):
    return bot.get_channel(channel_memory_id)


async def get_nickname(bot: commands.Bot, discord_id: int):
    db = DataBaseR6()
    row = db.get_player_row_by_discord_id(discord_id)
    return row["nickname"]


async def get_all_memory(bot):
    list_messages = []
    channel_memory = get_channel_memory(bot)
    async for message in channel_memory.history():
        list_messages.append(message.content)
    return list_messages


async def get_nicks_memory(bot):
    list_players = []
    channel_memory = get_channel_memory(bot)
    async for message in channel_memory.history():
        list_players.append(message.content.split()[1])
    return list_players

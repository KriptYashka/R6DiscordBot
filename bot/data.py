from jager import bot

channel_memory_id = 701698041660309574

async def get_all_memory():
    list_messages = []
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        list_messages.append(message.content)
    return list_messages


async def get_nicks_memory():
    list_players = []
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        list_players.append(message.content.split()[1])
    return list_players


async def get_nick_and_message_memory(user_id):
    channel_memory = bot.get_channel(channel_memory_id)
    async for message in channel_memory.history():
        if message.content.startswith(str(user_id)):
            return message.content.split()[1], message
    return None, None
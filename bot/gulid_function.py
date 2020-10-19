from module.module import *

def get_random_item(array):
    index_arr = random.randint(0, len(array) - 1)
    return array[index_arr]

async def is_required_role(guild, role, name_required_role):
    required_role = discord.utils.get(guild.roles, name=name_required_role)
    return role >= required_role


async def clear_channel(channel, n=1000):
    async for message in channel.history(limit=n):
        await message.delete()
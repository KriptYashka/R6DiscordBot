import discord

map_bank = ['https://steamuserimages-a.akamaihd.net/ugc/788614138475678496/5E79DD6D5F1676C822A0E426EAED46A5B3A89769/',
            'https://steamuserimages-a.akamaihd.net/ugc/788614138475678814/D3A78FBC8644F289B33DF1E2B10378D644E70ABF/',
            'https://steamuserimages-a.akamaihd.net/ugc/788614596624367346/F300BD8312166F0C657D687B05AAD8E14EC50C85/']

map_villa = [  # 'https://steamuserimages-a.akamaihd.net/ugc/788614138485887090
    # /94E5BB2164F75B7EB7300ECDF352A9CE18C10425/', Basement don't work
    'https://steamuserimages-a.akamaihd.net/ugc/788614138485887476/22F54B8CA1E709212D96C522BC52D44B4CB1D3EC/',
    'https://steamuserimages-a.akamaihd.net/ugc/788614138485887978/297522EBB53E09B095BF0375EF9105FD9516751B/']

map_kanal = ['https://steamuserimages-a.akamaihd.net/ugc/780734834272895649/182FCBA01946A91B863C6813365F603A023EC2A9/',
             'https://steamuserimages-a.akamaihd.net/ugc/780734834272896116/D9832038A36E0208CC8C239D2E010F9EFA0252F9/',
             'https://steamuserimages-a.akamaihd.net/ugc/780734834272896333/73F8FB86ACD37231C31D33CF4EDFC74469F0EF35/']

map_shale = ['https://steamuserimages-a.akamaihd.net/ugc/788614596623792401/58E469726F395D3EDA70316591210585479516AB/',
             'https://steamuserimages-a.akamaihd.net/ugc/788614596623792064/40D0B87EDB197FDEF888D5881A82D032FF51717C/',
             'https://steamuserimages-a.akamaihd.net/ugc/788614596623793105/CF8B3C02749871200887CB87CA6428B5A91FC380/']

map_border = ['https://steamuserimages-a.akamaihd.net/ugc/788614138480345333/A15472BC0DB09B118903759D2B742FCE8D322E59/',
              'https://steamuserimages-a.akamaihd.net/ugc/788614138480345616/FFF88CD5621AAB413D89D764A1BE2EBFF671D3BA/']

map_outback = [
    'https://steamuserimages-a.akamaihd.net/ugc/788614596619407725/275BBC9F6BE9B17071FF99FB4FEF31A7F0907CB5/',
    'https://steamuserimages-a.akamaihd.net/ugc/788614596619407506/BC1A3DA5095E41C3972A5BBDE30BB7CADDC5BD71/',
    'https://steamuserimages-a.akamaihd.net/ugc/788614596619408448/646CA3CC4DCC41F2CA1FFF1D48F540043BD5ECE6/']

map_club = ['https://steamuserimages-a.akamaihd.net/ugc/788614596619930898/6081C4B00948F9127DBDFE6687FF05A939B354C3/',
            'https://steamuserimages-a.akamaihd.net/ugc/788614596619978696/1590EB56C436EBD5217F59A040E8BFE46C0B9369/',
            'https://steamuserimages-a.akamaihd.net/ugc/788614596619930668/29E548710DCF545A745FD94D8EDE5E8099C64B05/']

map_coast = ['https://steamuserimages-a.akamaihd.net/ugc/788614138480799939/B3B54C160C9EAB9214349B498489FC260412F45E/',
             'https://steamuserimages-a.akamaihd.net/ugc/788614138480800228/01031B66DFD6FEFAA728A28EBCC0C239AD4DB860/']

map_consul = ['https://steamuserimages-a.akamaihd.net/ugc/786362975259494451/EC3191B98FFA0D252270459CD20592A85FA908BE/',
              'https://steamuserimages-a.akamaihd.net/ugc/786362975259494070/6C2A0B6B2F255ADB2FB4C8DB7DA52E65B7DDE2F8/',
              'https://steamuserimages-a.akamaihd.net/ugc/786362975259495136/E1362E97809C3EC51046D48DB94E221783B9DD54/']

maps = {"Банк": map_bank, "Вилла": map_villa, "Канал": map_kanal, "Шале": map_shale, "Граница": map_border,
        "Аутбэк": map_outback, "Клуб": map_club, "Побережье": map_coast, "Консульство": map_consul}


async def really_send_map(list_map, map_name, ctx, level=0):
    list_map.reverse()
    for url_level in list_map:
        embed = discord.Embed(title=map_name)
        embed.set_image(url=url_level)
        await ctx.send(embed=embed)
        level += 1


async def send_map(ctx, map_name):
    if maps[map_name] is None:
        return await ctx.send("Упс... Либо я забыл, как выглядит эта карта, либо ты ввел неверно название.")
    await really_send_map(maps[map_name], map_name, ctx)
import r6sapi as api

EU = api.RankedRegions.EU
jager_email = "hunterbot.jager@bk.ru"
jager_password = "Jagerthebest01"
jager_email = "mr.world.of.war@gmail.com"
jager_password = "r6PevQqc7gV29TA"

class PlayerR6:
    def __init__(self, nickname, member_id = -1):
        self.nickname = nickname
        self.member_id = member_id
        # Основная статистика
        self.kills = 0
        self.deaths = 0
        self.wins = 0
        self.loses = 0
        self.mmr = 0
        # Предыдущая статистика
        self.last_kills = 0
        self.last_deaths = 0
        self.last_wins = 0
        self.last_loses = 0
        self.last_mmr = 0
        # Прочее
        self.rank = 0
        self.time_played = 0
        self.icon_url = 0

    async def get_stats(self):
        """
        Загружает основную статистику
        """
        auth = api.Auth(jager_email, jager_password)
        try:
            player = await auth.get_player(self.nickname, api.Platforms.UPLAY)
        except:
            return
        await player.load_general()
        rank = await player.get_rank(EU)
        self.rank = rank
        self.mmr = int(rank.mmr)
        self.kills = player.kills
        self.deaths = player.deaths
        self.wins = player.matches_won
        self.deaths = player.matches_lost
        self.time_played = int(player.time_played / 60 / 60)
        self.icon_url = player.icon_url

    async def update_daily_stats(self):
        await self.get_stats()
        self.last_kills = self.kills
        self.last_deaths = self.deaths
        self.last_wins = self.wins
        self.last_loses = self.loses
        self.last_mmr = self.mmr


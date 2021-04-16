from bs4 import BeautifulSoup
import requests
import r6sapi as api
import asyncio

jager_email = "hunterbot.jager@bk.ru"
jager_password = "Jagerthebest01"
url_tracker = "https://r6.tracker.network/profile/pc/"


def to_digital(word):
    res = ""
    for symbol in word:
        if '0' <= symbol <= '9':
            res += symbol
    return int(res)


async def get_player_data(nick):
    auth = api.Auth(jager_email, jager_password)
    player_data = await auth.get_player(nick, api.Platforms.UPLAY)
    await player_data.load_general()
    await player_data.load_level()
    await player_data.load_rank(api.RankedRegions.EU)
    await auth.close()
    # result = {"player": player, "rank": rank}
    return player_data

class PlayerR6:
    def __init__(self, nickname=None, member_id=-1):
        """
        Класс игрока R6.
        Имеет статистику: убийства, смерти, победы, проигрыши, время игры, ММР.
        Дополнительная информация: ID участника сервера, URL аватара аккаунта UPlay.

        При инициализации подгружаются все данные.
        """
        self.nickname = nickname
        self.member_id = member_id

        # Основная статистика
        self.kills, self.deaths, self.wins, self.loses, self.time_played = None, None, None, None, None
        self.mmr, self.rank_name, self.rank_url = None, None, None
        self.icon_url = None

        # Предыдущая статистика ( думаю от нее нужно избавлятся )
        self.last_kills, self.last_kills, self.last_wins, self.last_loses, self.last_mmr = None, None, None, None, None

        if self.nickname is not None:
            self.load_stats()

    def __iter__(self):
        return iter([self])

    @asyncio.coroutine
    def load_stats(self):
        """
        Загружает основную статистику
        Используется BS4, требуется перейти на r6sapi
        """
        player_data = yield from get_player_data(self.nickname)

        # parser_data = ["PVPKills", "PVPDeaths", "PVPMatchesWon", "PVPMatchesLost", "PVPTimePlayed"]
        # url = url_tracker + self.nickname
        # full_page = requests.get(url)
        # soup = BeautifulSoup(full_page.content, 'html.parser')
        # stats = []
        # for item in parser_data:
        #     stats.append(to_digital(soup.find('div', {'data-stat': item}).contents[0]))
        # self.icon_url = soup.find('div', {'class': 'trn-profile-header__avatar'}).find('img').attrs['src']
        # trn_defstat = soup.find_all('div', {'class': 'trn-defstat'})
        # for item in trn_defstat:
        #     div_text = item.find('div', {'class': 'trn-defstat__name'})
        #     if div_text.next_element == "MMR" and self.mmr is None:
        #         self.mmr = to_digital(item.find('div', {'class': 'trn-defstat__value'}).contents[0])
        #     if div_text.next_element == "Rank" and self.rank_name is None:
        #         self.rank_name = item.find('div', {'class': 'trn-defstat__value'}).contents[0]
        #
        # self.rank_url = rank_icons[self.rank_name.replace("\n", "")]
        # self.kills, self.deaths, self.wins, self.loses, self.time_played = (item for item in stats)

    def update_daily_stats(self):
        self.load_stats()
        self.last_kills = self.kills
        self.last_deaths = self.deaths
        self.last_wins = self.wins
        self.last_loses = self.loses
        self.last_mmr = self.mmr

from bs4 import BeautifulSoup
import requests
import r6sapi as api
import asyncio

jager_email = "hunterbot.jager@bk.ru"
jager_password = "Jagerthebest01"
url_tracker = "https://r6.tracker.network/profile/pc/"

rank_icons = {
    "Not ranked yet.": "https://i.imgur.com/sB11BIz.png",  # unranked
    "COOPER I": "https://i.imgur.com/0J0jSWB.jpg",  # copper 1
    "COOPER II": "https://i.imgur.com/eI11lah.jpg",  # copper 2
    "COOPER III": "https://i.imgur.com/6CxJoMn.jpg",  # copper 3
    "COOPER IV": "https://i.imgur.com/ehILQ3i.jpg",  # copper 4
    "COOPER V": "https://i.imgur.com/B8NCTyX.png",  # copper 5
    "BRONZE I": "https://i.imgur.com/hmPhPBj.jpg",  # bronze 1
    "BRONZE II": "https://i.imgur.com/9AORiNm.jpg",  # bronze 2
    "BRONZE III": "https://i.imgur.com/QD5LYD7.jpg",  # bronze 3
    "BRONZE IV": "https://i.imgur.com/42AC7RD.jpg",  # bronze 4
    "BRONZE V": "https://i.imgur.com/TIWCRyO.png",  # bronze 5
    "SILVER I": "https://i.imgur.com/KmFpkNc.jpg",  # silver 1
    "SILVER II": "https://i.imgur.com/EswGcx1.jpg",  # silver 2
    "SILVER III": "https://i.imgur.com/m8GToyF.jpg",  # silver 3
    "SILVER IV": "https://i.imgur.com/D36ZfuR.jpg",  # silver 4
    "SILVER V": "https://i.imgur.com/PY2p17k.png",  # silver 5
    "GOLD I": "https://i.imgur.com/ffDmiPk.jpg",  # gold 1
    "GOLD II": "https://i.imgur.com/ELbGMc7.jpg",  # gold 2
    "GOLD III": "https://i.imgur.com/B0s1o1h.jpg",  # gold 3,
    "GOLD IV": "https://i.imgur.com/6Qg6aaH.jpg",  # gold 4
    "PLATINUM I": "https://i.imgur.com/qDYwmah.png",  # plat 1
    "PLATINUM II": "https://i.imgur.com/CYMO3Er.png",  # plat 2
    "PLATINUM III": "https://i.imgur.com/tmcWQ6I.png",  # plat 3
    "DIAMOND": "https://i.imgur.com/37tSxXm.png",  # diamond
    "CHAMPION": "https://i.imgur.com/VlnwLGk.png",  # champion
}


def to_digital(word):
    res = ""
    for symbol in word:
        if '0' <= symbol <= '9':
            res += symbol
    return int(res)


async def get_player_data(nick):
    auth = api.Auth(jager_email, jager_password)
    player_data = await auth.get_player(nick, api.Platforms.UPLAY)
    player_batch = await auth.get_player_batch(names=[nick],
                                               platform=api.Platforms.UPLAY)
    await player_data.load_general()
    await player_data.load_level()
    await auth.close()

    # Ranks
    mmr = None
    rank_name = None
    url = url_tracker + nick
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    trn_defstat = soup.find_all('div', {'class': 'trn-defstat'})

    for item in trn_defstat:
        div_text = item.find('div', {'class': 'trn-defstat__name'})

        if div_text.next_element == "MMR" and mmr is None:
            mmr = to_digital(item.find('div', {'class': 'trn-defstat__value'}).contents[0])

        if div_text.next_element == "Rank" and rank_name is None:
            rank_name = item.find('div', {'class': 'trn-defstat__value'}).contents[0]

    rank_url = rank_icons[rank_name.replace("\n", "")]
    icon_url = soup.find('div', {'class': 'trn-profile-header__avatar'}).find('img').attrs['src']
    player_data.url = icon_url

    rank = {"name": rank_name, "mmr": mmr, "rank_url": rank_url}
    result = {"player": player_data, "rank": rank}
    return result


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
        self.headshots = None
        self.level = None
        self.revives = None
        self.suicides = None

        if self.nickname is not None:
            self.load_stats()

    @asyncio.coroutine
    def load_stats(self):
        r6data = yield from get_player_data(self.nickname)
        player = r6data["player"]
        self.rank_name = r6data["rank"]["name"]
        self.mmr = r6data["rank"]["mmr"]
        self.rank_url = r6data["rank"]["rank_url"]
        self.kills, self.deaths = player.kills, player.deaths
        self.wins, self.loses, self.time_played = \
            player.matches_won, player.matches_lost, int(player.time_played / 60 / 60)
        self.icon_url = player.url
        self.headshots = player.headshots
        self.level = player.level
        self.revives = player.revives
        self.suicides = player.suicides

    def __iter__(self):
        return iter([self])

    def update_daily_stats(self):
        self.load_stats()
        last_kills = self.kills
        last_deaths = self.deaths
        last_wins = self.wins
        last_loses = self.loses
        last_mmr = self

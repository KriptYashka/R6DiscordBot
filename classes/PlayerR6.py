from bs4 import BeautifulSoup
import requests
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
        if ('0' <= symbol <= '9') or symbol == ".":
            res += symbol
    return float(res)


def get_player_data(nick):
    url = url_tracker + nick
    full_page = requests.get(url)
    if full_page.status_code != 200:
        if full_page.status_code == 404:
            return None
    soup = BeautifulSoup(full_page.content, 'html.parser')
    trn_defstat = soup.find_all('div', {'class': 'trn-defstat'})

    data = {
        "best mmr": None,
        "level": None,
        "wins": None,
        "losses": None,
        "win %": None,
        "headshot %": None,
        "headshots": None,
        "kills": None,
        "deaths": None,
        "kd": None,
        "time played": None,
        "mmr": None,
        "matches played": None,
        "melee kills": None,
        "blind kills": None,
    }

    rank_name = None

    for item in trn_defstat:
        item_name = item.find('div', {'class': 'trn-defstat__name'}).next_element.lower()
        if item_name in data:
            if data[item_name] is None:
                div_value = item.find('div', {'class': 'trn-defstat__value'})
                div_value_stylized = item.find('div', {'class': 'trn-defstat__value-stylized'})
                if div_value is not None and len(div_value.contents):
                    data[item_name] = to_digital(div_value.contents[0])
                if div_value_stylized is not None and len(div_value_stylized.contents):
                    data[item_name] = to_digital(div_value_stylized.contents[0])

        if item_name == "rank" and rank_name is None:
            rank_name = item.find('div', {'class': 'trn-defstat__value'}).contents[0]

    data["rank_name"], data["rank_url"] = None, None
    if rank_name is not None:
        data["rank_name"] = rank_name
        data["rank_url"] = rank_icons[rank_name.replace("\n", "")]
    data["icon_url"] = soup.find('div', {'class': 'trn-profile-header__avatar'}).find('img').attrs['src']

    return data


class PlayerR6:
    def __init__(self, nickname=None, member_id=-1):
        """
        Класс игрока R6.
        Имеет статистику: убийства, смерти, победы, проигрыши, время игры, ММР.
        Дополнительная информация: ID участника сервера, URL аватара аккаунта UPlay.

        При инициализации подгружаются все данные.
        """
        self.nickname = nickname
        self.discord_id = member_id

        # Основная статистика
        self.kills, self.deaths, self.wins, self.losses, self.time_played = None, None, None, None, None
        self.mmr, self.rank_name, self.rank_url = None, None, None
        self.icon_url = None
        self.headshots = None
        self.headshot_percentage = None
        self.level = None
        self.win_percentage = None
        self.matches = None
        self.kd = None
        self.melee_kills = None
        self.blind_kills = None

        if self.nickname is not None:
            self.load_stats()

    def load_stats(self):
        data = get_player_data(self.nickname)
        self.rank_name = data["rank_name"]
        self.mmr = data["mmr"]
        self.rank_url = data["rank_url"]
        self.kills, self.deaths = data["kills"], data["deaths"]
        self.wins, self.losses = data["wins"], data["losses"]
        self.time_played = data["time played"]
        self.icon_url = data["icon_url"]
        self.headshots = data["headshots"]
        self.headshot_percentage = data["headshot %"]
        self.level = data["level"]
        self.time_played = data["time played"]
        self.win_percentage = data["win %"]
        self.matches = data["matches played"]
        self.kd = data["kd"]
        self.melee_kills = data["melee kills"]
        self.blind_kills = data["blind kills"]

    def __iter__(self):
        return iter([self])

    def update_daily_stats(self):
        self.load_stats()
        last_kills = self.kills
        last_deaths = self.deaths
        last_wins = self.wins
        last_loses = self.losses
        last_mmr = self


def main():
    player = PlayerR6("KriptYashka", 42)
    print(player)


if __name__ == '__main__':
    main()

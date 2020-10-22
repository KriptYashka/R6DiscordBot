from bs4 import BeautifulSoup
import requests
import asyncio
import sqlite3

jager_email = "hunterbot.jager@bk.ru"
jager_password = "Jagerthebest01"
url_tracker = "https://r6.tracker.network/profile/pc/"
r6_data = []


def to_digital(word):
    res = ""
    for symbol in word:
        if '0' <= symbol <= '9':
            res += symbol
    return res


class PlayerR6:
    def __init__(self, nickname, member_id = -1):
        """
        Класс игрока R6.
        Имеет статистику: убийства, смерти, победы, проигрыши, время игры, ММР.
        Дополнительная информация: ID участника сервера, URL аватара аккаунта UPlay.

        При инициализации подгружаются все данные.
        """
        self.nickname = nickname
        self.member_id = member_id
        # Основная статистика
        self.kills = None
        self.deaths = None
        self.wins = None
        self.loses = None
        self.time_played = None
        self.data = [[self.kills, "PVPKills"], [self.deaths, "PVPDeaths"], [self.wins, "PVPMatchesWon"],
                     [self.loses, "PVPMatchesLost"], [self.time_played, "PVPTimePlayed"]]
        self.mmr = None
        self.icon_url = None,
        # Предыдущая статистика
        self.last_kills = None
        self.last_deaths = None
        self.last_wins = None
        self.last_loses = None
        self.last_mmr = None

        self.load_stats()

    def load_stats(self):
        """
        Загружает основную статистику
        """
        url = url_tracker + self.nickname
        full_page = requests.get(url)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        for item in self.data:
            item[0] = to_digital(soup.find('div', {'data-stat': item[1]}).contents[0])
        self.icon_url = soup.find('div', {'class': 'trn-profile-header__avatar'}).find('img').attrs['src']
        trn_defstat = soup.find_all('div', {'class': 'trn-defstat'})
        for stat in trn_defstat:
            div_text = stat.find('div', {'class': 'trn-defstat__name'})
            if div_text.next_element == "MMR":
                self.mmr = to_digital(stat.find('div', {'class': 'trn-defstat__value'}).contents[0])


    def update_daily_stats(self):
        self.load_stats()
        self.last_kills = self.kills
        self.last_deaths = self.deaths
        self.last_wins = self.wins
        self.last_loses = self.loses
        self.last_mmr = self.mmr


class DataBaseR6:
    def __init__(self):
        self.conn = sqlite3.connect("r6_players.db")
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE R6_players 
        (title text, artist text, release_date text, publisher text, media_type text)""")

async def main():
    ab = PlayerR6("KriptYashka")
    db = DataBaseR6()
    print(ab.mmr)

asyncio.run(main())
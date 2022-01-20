import sqlite3
from typing import List
from classes.PlayerR6 import PlayerR6
import datetime


def get_table_form(params):
    text = "("
    for item in params:
        if isinstance(item, (int, float)):
            item = str(item)
        text += item + ","
    text = text[:-1] + ")"
    return text


def get_insert_format(table, params: dict):
    req = "INSERT INTO {} {} VALUES (".format(table, get_table_form(params.keys()))
    for item in params.values():
        req += '"{}",'.format(item)
    req = req[:-1] + ");"
    return req


def get_set_format(params: dict):
    res = str()
    for item in params.items():
        res += "`{}`='{}',".format(item[0], item[1])
    return res[:-1]


def get_where_format(params: dict):
    res = str()
    for item in params.items():
        res += "`{}`='{}' AND ".format(item[0], item[1])
    return res[:-4]


def get_update_format(table, params: dict, where_params: dict):
    req = "UPDATE {} SET {} WHERE {}".format(table, get_set_format(params), get_where_format(where_params))
    return req


class DataBase:
    """База данных"""

    def __init__(self, name="default_db"):
        self.conn = sqlite3.connect(name + ".db")
        self.cursor = self.conn.cursor()

    def create_default_table(self, name: str, properties_str):
        request_user = """CREATE TABLE IF NOT EXISTS {}\n(id INTEGER PRIMARY KEY AUTOINCREMENT""".format(name)
        for item in properties_str:
            request_user += ",\n{} TEXT".format(item)
        request_user += ");"
        self.cursor.execute(request_user)

    def execute_and_commit(self, request: str):
        """Выполняет request в БД MySQL"""
        print(request)
        self.cursor.execute(request)
        self.conn.commit()

    def add_item(self, table: str, params: dict):
        """Добавляет в таблицу какие-либо данные ( params )"""
        request_insert = get_insert_format(table, params)
        self.execute_and_commit(request_insert)

    def update_item(self, table: str, params: dict, where_params: dict):
        """Обновляет в таблице строки"""
        request_insert = get_update_format(table, params, where_params)
        self.execute_and_commit(request_insert)

    def select(self, table, search_item_name=None, search_item_value=None):
        """Поиск объектов в таблице"""
        if search_item_name is None:
            request = "SELECT * FROM {};".format(table)
        else:
            request = "WHERE {} = {};".format(search_item_name, search_item_value)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def delete_item(self, table: str, search_id):
        request = "DELETE FROM {} WHERE id == {}".format(table, search_id)
        self.execute_and_commit(request)

    def is_exist(self, table: str, search_parameter_name: str, search_parameter_value):
        request = "SELECT * FROM {} WHERE `{}`={}".format(table, search_parameter_name, search_parameter_value)
        self.cursor.execute(request)
        if self.cursor.fetchall():
            return True
        return False

    def delete(self, table, search_item_name=None, search_item_value=None):
        """ Удаление объекта в таблице """
        request = "DELETE FROM {} WHERE {} = {}".format(table, search_item_name, search_item_value)
        self.execute_and_commit(request)

    def get_ids(self, table: str):
        request = "SELECT * FROM {}".format(table)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        arr = []
        for item in result:
            arr.append(item[0])
        return arr


class DataBaseR6(DataBase):
    """ Класс базы данных с игроками R6 """

    def __init__(self):
        super().__init__("r6.db")
        self.players_table_name = "players"
        self.players_cols = {
            "id": "INT PRIMARY KEY",
            "member_id": "INT",
            "nickname": "TEXT",
            "kills": "INT",
            "deaths": "INT",
            "wins": "INT",
            "loses": "INT",
            "mmr": "FLOAT",
        }
        self.create_table_player()

    def create_table_player(self):
        request = f"CREATE TABLE IF NOT EXISTS {self.players_table_name}("
        for name, type_db in self.players_cols:
            request += f"{name} {type_db},"
        request = request[:-1] + ");"
        self.cursor.execute(request)

    def add_players(self, players: PlayerR6):
        """ Добавляет в таблицу новых игроков """
        for player in players:
            player_request = {
                "member_id": player.member_id,
                "nickname": player.nickname,
                "kills": player.kills,
                "deaths": player.deaths,
                "wins": player.wins,
                "loses": player.loses,
                "mmr": player.mmr,
            }

            self.add_item(self.players_table_name, player_request)

    def get_all_players(self, search_item_name=None, search_item_value=None):
        """ Возвращает массив всех игроков.
        Можно выбрать параметры поиска."""
        fetch = self.select(self.players_table_name, search_item_name, search_item_value)
        players = []
        for data in fetch:
            player = PlayerR6
            item_id, player.member_id, player.nickname, player.kills, player.deaths, \
            player.wins, player.loses, player.mmr = [item for item in data]
            players.append(player)
        return players


def main():
    db = DataBaseR6()


if __name__ == '__main__':
    main()
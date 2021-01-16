import sqlite3

from typing import List

from classes.PlayerR6 import PlayerR6

def get_table_form(params):
    if params == "":
        return ""
    text = "("
    for item in params:
        text += item + ","
    text = text[:-1] + ")"
    return text

def get_insert_format(table, params, table_params):
    req = "INSERT INTO {} {} VALUES (".format(table, get_table_form(table_params))
    for item in params:
        if item == 'null':
            req += '{},'.format(item)
        else:
            req += '"{}",'.format(item)
    req = req[:-1] + ");"
    print(req)
    return req

class DB:
    """ Базовый класс БД """
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_and_commit(self, request):
        """ Выполняет запрос и фиксирует изменения в БД """
        self.cursor.execute(request)
        self.conn.commit()

    def insert(self, table: str, data: List[str], col_fields=""):
        """ Добавляет в нужную таблицу данные ( data )
        table - название таблицы в БД
        data - данные нового объекта
        col_fields - названия колонок таблицы БД. Если данные вводятся по порядку названия таблицы, этот параметр не
        требуется """
        request_insert = get_insert_format(table, data, col_fields)
        self.execute_and_commit(request_insert)

    def select(self, table, search_item_name = None, search_item_value = None):
        """ Поиск объектов в таблице """
        if search_item_name is None:
            request = "SELECT * FROM {};".format(table)
        else:
            request = "WHERE {} = {};".format(search_item_name, search_item_value)
        print(request)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def delete(self, table, search_item_name = None, search_item_value = None):
        """ Удаление объекта в таблице """
        request = "DELETE FROM {} WHERE {} = {}".format(table, search_item_name, search_item_value)
        self.execute_and_commit(request)

class DataBaseR6(DB):
    """ Класс базы данных с игроками R6 """
    def __init__(self):
        super().__init__("../db_jager.db")
        self.table_name = "R6_players"
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS R6_players (
            id INT PRIMARY KEY,
            member_id INT,
            nickname TEXT, 
            kills INT, 
            deaths INT, 
            wins INT,
            loses INT,
            mmr INT
            );""")

    def add_players(self, players):
        """ Добавляет в таблицу новых игроков """
        for player in players:
            player_request = "null {} {} {} {} {} {} {}".format(player.member_id, player.nickname, player.kills,
                                                           player.deaths, player.wins, player.loses, player.mmr).split()
            super().insert(self.table_name, player_request)

    def get_all_players(self, search_item_name = None, search_item_value = None):
        """ Возвращает массив всех игроков.
        Можно выбрать параметры поиска."""
        fetch = super().select(self.table_name, search_item_name, search_item_value)
        players = []
        for data in fetch:
            player = PlayerR6
            item_id, player.member_id, player.nickname, player.kills, player.deaths, \
            player.wins, player.loses, player.mmr = [item for item in data]
            players.append(player)
        return players
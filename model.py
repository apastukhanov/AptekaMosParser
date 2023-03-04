import os
from typing import List, Tuple

import sqlite3


class Model:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join("db", "drugs.db"))
        self.cursor = self.conn.cursor()
        self.check_db_exists()

    def insert(self, table: str, columns: List, values: List[Tuple]):
        cnt = len(columns)
        columns = ', '.join( columns )
        placeholders = ", ".join( "?" * cnt)
        self.cursor.executemany(
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders})",
            values)
        self.conn.commit()

    def fetchall(self, table: str, columns: List[str]) -> List[Tuple]:
        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result

    def delete(self, table: str, row_id: int) -> None:
        row_id = int(row_id)
        self.cursor.execute(f"delete from {table} where id={row_id}")
        self.conn.commit()

    def clear_table(self, table: str) -> None:
        self.cursor.execute(f"delete from {table}")
        self.cursor.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table}';")
        self.conn.commit()

    def get_cursor(self):
        return self.cursor

    def _init_db(self) -> None:
        """Инициализирует БД"""
        with open("createdb.sql", "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.conn.commit()

    def check_db_exists(self) -> None:
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""
        self.cursor.execute("SELECT name FROM sqlite_master "
                       "WHERE type='table' AND name='prices'")
        table_exists = self.cursor.fetchall()
        if table_exists:
            return
        self._init_db()

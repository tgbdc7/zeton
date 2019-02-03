import os
import sqlite3 as sql
import sys

QUERY_PUNKTY_UCZNIOW = """create table punkty_uczniow (
    id_ucznia integer primary key autoincrement,
    suma_punktow integer not null,
    szkolny_rekord_tygodnia integer not null
    );"""

QUERY_UZYTKOWNICY = """create table uzytkownicy (
  id integer primary key autoincrement,
  login text not null,
  pass text not null
  );"""

# populowanie bazy testowymi danymi
QUERY_INSERT_POINTS = """insert into punkty_uczniow VALUES  (1, 17, 29)"""
QUERY_INSERT_USER = "insert into uzytkownicy VALUES  (NULL, 'test', 'testpass')"


def recreate_tables(db):
    cur = db.cursor()

    cur.execute("drop table if exists uzytkownicy")
    cur.execute(QUERY_UZYTKOWNICY)

    cur.execute("drop table if exists punkty_uczniow")
    cur.execute(QUERY_PUNKTY_UCZNIOW)

    cur.execute(QUERY_INSERT_POINTS)
    cur.execute(QUERY_INSERT_USER)

    db.commit()

    db.close()


if __name__ == '__main__':
    # drops and recreates two tables
    script_path = os.path.realpath(sys.argv[0])
    dir_path = os.path.dirname(script_path)
    db = sql.connect(dir_path + "/db.sqlite")
    recreate_tables(db)

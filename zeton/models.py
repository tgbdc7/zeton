import sqlite3 as sql


def wprowadzUzytkownika(login_uzytkownika, haslo_uzytkownika):
    con = sql.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("INSERT INTO uzytkownicy (login, haslo) VALUES (?,?)", (login_uzytkownika, haslo_uzytkownika))
    con.commit()
    con.close()


def wyciagnijUzytkownika():
    con = sql.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("SELECT login, haslo FROM uzytkownicy")
    uzytkownicy = cur.fetchall()
    con.close()
    return uzytkownicy


def create_tables():
    query_punkty_uczniow = """create table punkty_uczniow (
        id_ucznia integer primary key autoincrement,
        suma_punktow integer not null,
        szkolny_rekord_tygodnia integer not null
        );"""

    query_uzytkownicy = """create table uzytkownicy (
      id_uzytkownika integer primary key autoincrement,
      login text not null,
      haslo text not null
      );"""

    con = sql.connect("../db.sqlite")
    cur = con.cursor()

    cur.execute("drop table if exists uzytkownicy")
    cur.execute(query_uzytkownicy)

    cur.execute("drop table if exists punkty_uczniow")
    cur.execute(query_punkty_uczniow)

    con.commit()

    con.close()


if __name__ == '__main__':
    # drops and recreates two tables
    create_tables()

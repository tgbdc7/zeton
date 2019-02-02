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

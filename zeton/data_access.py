import json
from datetime import datetime, date

from flask import g


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def wczytaj_dane():
    """
    Wczytuje dane z pliku dane.json
    Jeśli nie ma tego pliku to go tworzy z ustawionymi wartościmai na "0"
    :return: dane ucznia
    """
    try:
        with open('dane.json', 'r') as plik:
            dane = json.load(plik)
    except FileNotFoundError:
        with open('dane.json', 'w') as plik:
            dane = {"punkty": 0, "szkolny_rekord_tygodnia": 0, "ban": False}
            json.dump(dane, plik, default=json_serial)
    return dane


def zapisz_dane(dane):
    """
    zapisuje dane do pliku "dane.json"
    :param dane: dane ucznia - słownik (dictionary)
    :return: None
    """
    try:
        with open('dane.json', 'w') as plik:
            json.dump(dane, plik, default=json_serial)
    except:
        return f'Nie można zapisać dancyh do pliku'


def get_points(user_id):
    query = 'select points from points_ where id = ?'
    result = g.db.cursor().execute(query, (user_id,))
    points = result.fetchone()[0]
    return points


def get_weekly_highscore(user_id):
    # TODO: do dopisania na podstawie funkcji 'get_points()'
    pass

def add_points(user_id, points):
    query = 'UPDATE points_ SET points = points + ? WHERE id = ?;'
    g.db.cursor().execute(query, [points, user_id])
    g.db.commit()


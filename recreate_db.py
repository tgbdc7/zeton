import os
import sqlite3 as sql
import sys
from werkzeug.security import generate_password_hash


def create_user(username, password, firstname):
    query = "insert into users (username, password, firstname) VALUES (?, ?, ?)"

    cur = db.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute(query, [username, hashed_password, firstname])
    db.commit()


if __name__ == '__main__':
    PATH_TO_APP = "zeton"
    db = sql.connect(PATH_TO_APP + "/db.sqlite")

    with open(PATH_TO_APP + '/sql/01_db_init.sql') as f:
        db.executescript(f.read())

    with open(PATH_TO_APP + '/sql/02_insert_test_data.sql') as f:
        db.executescript(f.read())

    db.close()

import os
import sqlite3 as sql
import sys
from werkzeug.security import check_password_hash, generate_password_hash


def create_points():
    query = "insert into points_ VALUES (1, 0, 0)"

    cur = db.cursor()
    cur.execute(query)
    db.commit()


def create_user(username, password):
    query = "insert into users VALUES (NULL, ?, ?)"

    cur = db.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute(query, [username, hashed_password])
    db.commit()


if __name__ == '__main__':
    script_path = os.path.realpath(sys.argv[0])
    dir_path = os.path.dirname(script_path)
    db = sql.connect(dir_path + "/db.sqlite")

    with open('01_db_init.sql') as f:
        db.executescript(f.read())

    create_user('admin', 'admin')
    create_points()

    db.close()

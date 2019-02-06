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
    script_path = os.path.realpath(sys.argv[0])
    dir_path = os.path.dirname(script_path)
    db = sql.connect(dir_path + "/db.sqlite")

    with open('01_db_init.sql') as f:
        db.executescript(f.read())

    create_user('admin', 'admin', 'Admin')
    create_user('testowy', 'testowy', 'Testowy')

    db.close()

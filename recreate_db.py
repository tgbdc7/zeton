import pathlib
import sqlite3 as sql
from werkzeug.security import generate_password_hash


def create_user(username, password, firstname, role):
    query = "insert into users (username, password, firstname, role) VALUES (?, ?, ?, ?)"

    cur = db.cursor()
    hashed_password = generate_password_hash(password)
    params = (username, hashed_password, firstname, role)
    cur.execute(query, params)
    db.commit()


def get_sql_scripts(dir):
    p = pathlib.Path(dir)
    scripts = p.glob('*.sql')
    return sorted(scripts)


def run_scripts(scripts_list):
    for script in scripts_list:
        with open(script) as f:
            db.executescript(f.read())
        print(f'Script "{f.name}" executed')


if __name__ == '__main__':
    DATABASE = 'db.sqlite'
    SQL_SCRIPTS_DIR = './sql'

    db = sql.connect(DATABASE)
    scripts = get_sql_scripts(SQL_SCRIPTS_DIR)
    run_scripts(scripts)

    # create_user('opiekun1', 'opiekun1', 'Antoni', 'caregiver')
    # create_user('dziecko1', 'dziecko1', 'Bazyli', 'child')
    # create_user('dziecko2', 'dziecko2', 'Celina', 'child')
    #
    # create_user('opiekun2', 'opiekun2', 'Dominika', 'caregiver')
    # create_user('dziecko3', 'dziecko3', 'Ewelina', 'child')
    # create_user('dziecko4', 'dziecko4', 'Filip', 'child')
    #
    # create_user('dyrektor', 'dyrektor', 'Zbigniew', 'caregiver')

    db.close()

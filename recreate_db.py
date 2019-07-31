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

def create_task(user_id, name, points, max_day, max_week):
    query = "INSERT INTO home_points (user_id, name, points, max_day, max_week) VALUES (?, ?, ?, ?, ?)"

    cur = db.cursor()
    params = (user_id, name, points, max_day, max_week)
    cur.execute(query, params)
    db.commit()

def get_sql_scripts(dir):
    p = pathlib.Path(dir)
    scripts = p.glob('*.sql')
    return sorted(scripts)


def run_scripts(scripts_list):
    for script in scripts_list:
        with open(script, encoding='utf-8') as f:
            db.executescript(f.read())
        print(f'Script "{f.name}" executed')


if __name__ == '__main__':
    DATABASE = 'db.sqlite'
    SQL_SCRIPTS_DIR = './sql'

    db = sql.connect(DATABASE)
    scripts = get_sql_scripts(SQL_SCRIPTS_DIR)
    run_scripts(scripts)

    create_user('opiekun1', 'opiekun1', 'Antoni', 'caregiver')
    create_user('dziecko1', 'dziecko1', 'Bazyli', 'child')
    create_user('dziecko2', 'dziecko2', 'Celina', 'child')

    create_user('opiekun2', 'opiekun2', 'Dominika', 'caregiver')
    create_user('dziecko3', 'dziecko3', 'Ewelina', 'child')
    create_user('dziecko4', 'dziecko4', 'Filip', 'child')

    create_user('dyrektor', 'dyrektor', 'Zbigniew', 'caregiver')

    create_task(2, "sprzątanie pokoju", 20, 1, 7)
    create_task(2, "wykonanie polecenia bez zwłoki", 20, 1, 7)
    create_task(2, "odrobienie lekcji", 20, 1, 5)
    create_task(2, "spakowanie plecaka", 20, 1, 5)
    create_task(2, "spakowanie plecaka z rodzicem", 20, 1, 5)
    create_task(2, "pomoc rodzicom", 10, 3, 35)
    create_task(2, "podlanie kwiatów", 5, 1, 7)
    create_task(2, "pomoc ślepej sąsiadce", 20, 1, 7)

    create_task(3, "granie na instrumencie", 20, 1, 7)
    create_task(3, "wyprowadzanie psa", 5, 3, 35)
    create_task(3, "sprawdzanie skrzynki na listy", 5, 1, 2)

    create_task(5, "ścieranie kurzy", 10, 1, 3)
    create_task(5, "czytanie książki", 10, 1, 7)
    create_task(5, "trening na basenie", 20, 1, 2)
    create_task(5, "mycie okien", 100, 1, 1)

    create_task(6, "karmienie rybek", 5, 1, 7)
    create_task(6, "naprawianie motocyklu", 20, 1, 2)
    create_task(6, "powrót do domu przed 20", 10, 1, 7)

    db.close()

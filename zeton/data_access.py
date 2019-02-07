import json
from datetime import datetime, date, timedelta
import ciso8601

from flask import g


def get_points(user_id):
    query = 'select points from users where id = ?'
    result = g.db.cursor().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def get_weekly_highscore(user_id):
    query = 'select school_weekly_highscore from users where id = ?'
    result = g.db.cursor().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['school_weekly_highscore']
    return None


def add_points(user_id, points):
    query = 'UPDATE users SET points = points + ? WHERE id = ?;'
    g.db.cursor().execute(query, [points, user_id])
    g.db.commit()


def get_firstname(user_id):
    query = 'select firstname from users where id = ?'
    result = g.db.cursor().execute(query, (user_id,))
    row = result.fetchone()
    if row:
        return row['firstname']
    return None


def get_last_active_ban(user_id):
    all_bans = get_all_bans(user_id)
    # sqlite3 nie wspiera typu datetime, więc obliczenia trzeba zrobić samemu
    for ban_id, _, start, end in reversed(all_bans):
        start = ciso8601.parse_datetime(start)
        end = ciso8601.parse_datetime(end)

        if start < datetime.now() < end:
            return {'ban_id': ban_id, 'start': start, 'end': end}


def get_all_bans(user_id):
    query = 'select * from bans where user_id = ?'
    result = g.db.cursor().execute(query, [user_id])
    return result.fetchall()


def give_ban(user_id, duration_minutes):
    start = datetime.now()
    end = start + timedelta(minutes=duration_minutes)
    start_timestamp = start.isoformat()
    end_timestamp = end.isoformat()

    query = 'insert into bans values (NULL, ?, ?, ?)'
    params = (user_id, start_timestamp, end_timestamp)
    result = g.db.cursor().execute(query, params)
    g.db.commit()

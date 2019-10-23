from zeton.db import get_db


def get_prizes(child_id):
    query = "SELECT * FROM prizes WHERE user_id = ? AND is_active = 1 ORDER BY points"
    result = get_db().execute(query, (child_id,))
    return result.fetchall()


def create_prize(user_id, name, points, max_day, max_week, max_month, is_active):
    query = "INSERT INTO prizes " \
            "(user_id, name, points, max_day, max_week, max_month, is_active) " \
            "VALUES (?, ?, ?, ?, ?, ?, ?)"

    cur = get_db().cursor()
    params = (user_id, name, points, max_day, max_week, max_month, is_active)
    cur.execute(query, params)
    get_db().commit()


def deactivate_prize(child_id, prizes_id):
    query = "UPDATE 'prizes' " \
            "SET is_active = 0 " \
            "WHERE user_id = ? AND id = ? "
    cur = get_db().cursor()
    params = (child_id, prizes_id)
    cur.execute(query, params)
    get_db().commit()


def update_prize(user_id, name, points, max_day, max_week, max_month, prize_id):
    query = "UPDATE 'prizes' " \
            "SET user_id = ?, name = ?, points = ?, max_day = ?, max_week = ?, max_month = ?" \
            "WHERE id = ?"
    params = (user_id, name, points, max_day, max_week, max_month, prize_id)
    get_db().execute(query, params)
    get_db().commit()


def get_prize(child_id, prize_id):
    query = "SELECT * FROM 'prizes'" \
            "WHERE user_id = ? AND id = ?"
    params = (child_id, prize_id)
    result = get_db().execute(query, params)
    return result.fetchone()

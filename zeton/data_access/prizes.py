from zeton.db import get_db


def get_prizes(child_id):
    query = "SELECT * FROM prizes WHERE user_id = ? ORDER BY points"
    result = get_db().execute(query, (child_id,))
    return result.fetchall()


def create_prize(user_id, name, points, max_day, max_week, max_month):
    query = "INSERT INTO prizes (user_id, name, points, max_day, max_week, max_month) VALUES (?, ?, ?, ?, ?, ?)"

    cur = get_db().cursor()
    params = (user_id, name, points, max_day, max_week, max_month)
    cur.execute(query, params)
    get_db().commit()


def delete_childs_prize(child_id, prizes_id):
    query = "DELETE FROM prizes WHERE user_id = ? AND id = ?"
    cur = get_db().cursor()
    params = (child_id, prizes_id)
    cur.execute(query, params)
    get_db().commit()

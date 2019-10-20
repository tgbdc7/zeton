from zeton.db import get_db


def get_tasks(child_id):
    query = "SELECT * FROM home_points WHERE user_id = ? AND is_active=1 ORDER BY points LIMIT 10"

    result = get_db().execute(query, (child_id,))
    return result.fetchall()


def create_task(user_id, name, points, max_day, max_week):
    query = "INSERT INTO home_points (user_id, name, points, max_day, max_week) VALUES (?, ?, ?, ?, ?)"

    cur = get_db().cursor()
    params = (user_id, name, points, max_day, max_week)
    cur.execute(query, params)
    get_db().commit()

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


def deactivate_task(child_id, task_id):
    query = "UPDATE 'home_points' " \
            "SET is_active = 0 " \
            "WHERE user_id = ? AND id = ? "
    cur = get_db().cursor()
    params = (child_id, task_id)
    cur.execute(query, params)
    get_db().commit()


def add_new_task(user_id, name, points, max_day, max_week, is_active):
    query = "INSERT INTO 'home_points' " \
            "(user_id, name, points, max_day, max_week, is_active) " \
            "VALUES (?, ?, ?, ?, ?, ?) "
    params = (user_id, name, points, max_day, max_week, is_active)
    get_db().execute(query, params)
    get_db().commit()


def update_task(user_id, name, points, max_day, max_week, is_active, task_id):
    query = "UPDATE 'home_points' " \
            "SET user_id = ?, name = ?, points = ?, max_day = ?, max_week = ?, is_active = ?" \
            "WHERE id = ?"
    params = (user_id, name, points, max_day, max_week, is_active, task_id)
    get_db().cursor().execute(query, params)
    get_db().commit()


def get_task_by_tasks_id(child_id, task_id):
    query = "SELECT * FROM 'home_points' " \
            "WHERE user_id = ? AND id = ?"
    params = (child_id, task_id)
    result = get_db().execute(query, params)
    return result.fetchone()
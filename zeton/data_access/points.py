from zeton.db import get_db


def get_points(user_id):
    query = 'select points from users where id = ?'
    result = get_db().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def change_points_by(target_id, points, user_id, logged_user_firstname):
    """ used both to add and subtract points from the current amount """
    query = 'UPDATE users SET points = points + ?, last_insert_id = ?, last_insert_firstname = ?   WHERE id = ?;'
    get_db().execute(query, [points, user_id, logged_user_firstname, target_id])
    get_db().commit()

def get_points_history(child_id):
    query = 'SELECT * FROM points_history WHERE child_id = ? ORDER BY id DESC LIMIT 10'
    result = get_db().execute(query, [child_id,])
    return result.fetchall()
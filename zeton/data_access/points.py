from zeton.db import get_db


def get_points(user_id):
    query = 'select points from users where id = ?'
    result = get_db().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def change_points_by(user_id, points):
    """ used both to add and subtract points from the current amount """
    query = 'UPDATE users SET points = points + ? WHERE id = ?;'
    get_db().execute(query, [points, user_id])
    get_db().commit()

from zeton.db import get_db


def get_points(user_id):
    query = 'select points from users where id = ?'
    result = get_db().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def change_points_by(target_id, points, user_id):
    """ used both to add and subtract points from the current amount """
    query = 'UPDATE users SET points = points + ?, last_insert_id = ?   WHERE id = ?;'
    get_db().execute(query, [points, user_id, target_id])
    get_db().commit()

def add_exp(exp, user_id):
    query = 'UPDATE users SET exp = exp + ?  WHERE id = ?;'
    get_db().execute(query, [exp, user_id])
    get_db().commit()
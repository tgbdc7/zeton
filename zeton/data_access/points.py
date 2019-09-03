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

def get_points_history(child_id, id_changing_user):
    query = 'SELECT p.points_change, p.change_timestamp, u.firstname ' \
            'FROM points_history p ' \
            'JOIN users u ' \
            'ON (p.id_changing_user=u.id) ' \
            'WHERE (p.child_id = ? AND u.firstname = ?) ' \
            'ORDER BY p.id DESC LIMIT 10'
    result = get_db().execute(query, [child_id, id_changing_user,])
    return result.fetchall()
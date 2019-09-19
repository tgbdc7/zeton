from zeton.db import get_db


def get_points(child_id):
    query = 'select points from main_points where child_id = ?'
    result = get_db().execute(query, [child_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def change_points_by(target_id, points, child_id):
    """ used both to add and subtract points from the current amount """
    query = 'UPDATE main_points SET points = points + ?, last_insert_id = ?   WHERE child_id = ?;'
    get_db().execute(query, [points, child_id, target_id])
    get_db().commit()


def add_exp(exp, child_id):
    query = 'UPDATE main_points SET exp = exp + ?  WHERE child_id = ?;'
    get_db().execute(query, [exp, child_id])
    get_db().commit()

def get_child_points(id):
    query = """
    SELECT mp.* 
    FROM users AS u 
    JOIN main_points AS mp on u.id = mp.child_id
    WHERE u.id = ?
    AND u.role = 'child'
    """
    result = get_db().execute(query, (id,))
    child_points = dict(result.fetchone())
    return child_points
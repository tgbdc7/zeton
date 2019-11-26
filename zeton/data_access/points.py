from zeton.db import get_db


def get_only_points(child_id):
    query = 'select points from main_points where child_id = ?'
    result = get_db().execute(query, [child_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def change_points_by(target_id, points, user_id, exercise_id):
    """ used both to add and subtract points from the current amount """
    query = 'UPDATE main_points SET points = points + ?, last_insert_id = ?, last_exercise_id= ?   WHERE child_id = ?;'
    get_db().execute(query, [points, user_id, exercise_id, target_id])
    get_db().commit()


def add_exp(exp, child_id):
    query = 'UPDATE main_points SET exp = exp + ? WHERE child_id = ?;'
    get_db().execute(query, [exp, child_id])
    get_db().commit()


def get_child_points(child_id):
    query = """
    SELECT * FROM  main_points
    WHERE main_points.child_id=?
    """
    result = get_db().execute(query, (child_id,))
    child_points = dict(result.fetchone())
    return child_points


def get_points_history(child_id):
    query = 'SELECT p.points_change, p.change_timestamp, u.firstname ' \
            'FROM points_history p ' \
            'INNER JOIN users u ' \
            'ON (p.id_changing_user=u.id) ' \
            'WHERE p.child_id = ? ' \
            'ORDER BY p.id DESC LIMIT 10'
    result = get_db().execute(query, [child_id, ])
    return result.fetchall()

def get_points_history_limits(child_id,dt_string, exercise_id):
    query = 'select points_history.child_id, points_history.change_timestamp, home_points.max_day, home_points.max_week, home_points.id ' \
            'from points_history INNER JOIN home_points on home_points.id=points_history.points_name ' \
            f'where points_history.child_id= {child_id} and points_history.change_timestamp>\'{dt_string}\' and  home_points.id = {exercise_id} '
    result = get_db().execute(query)
    return result.fetchall()
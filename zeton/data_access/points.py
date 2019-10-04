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
def get_points_history(child_id):
    query = 'SELECT p.points_change, p.change_timestamp, u.firstname ' \
            'FROM points_history p ' \
            'INNER JOIN users u ' \
            'ON (p.id_changing_user=u.id) ' \
            'WHERE p.child_id = ? ' \
            'ORDER BY p.id DESC LIMIT 10'
    result = get_db().execute(query, [child_id,])
    return result.fetchall()

def get_points_history_limits(child_id,start_date):
    query = "SELECT home_points.id, count(home_points.id) as 'sum', home_points.max_day, home_points.max_week, users.id as 'user_id', points_history.change_timestamp" \
             "FROM home_points" \
             "INNER JOIN users" \
             "ON home_points.user_id = users.id" \
             "INNER JOIN points_history" \
             "ON users.id=points_history.child_id" \
             "where points_history.change_timestamp>'" + start_date + "' and users.id="+child_id + \
             "group by home_points.id"



    result = get_db().execute(query)
    return result.fetchall()

def get_ex_day_limit(id):
    query = "SELECT home_points.max_day" \
            "FROM home_points" \
            "where home_points.id="+id

    result = get_db().execute(query)
    return result.fetchall()

def get_ex_week_limit(id):
    query = "SELECT home_points.max_week" \
            "FROM home_points" \
            "where home_points.id="+id

    result = get_db().execute(query)
    return result.fetchall()
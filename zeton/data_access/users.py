from flask import session, g

from zeton.data_access.bans import check_bans_status
from zeton.data_access.points import get_child_points

from zeton.db import get_db


def get_weekly_highscore(user_id):
    query = 'select school_weekly_highscore from users where id = ?'
    result = get_db().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['school_weekly_highscore']
    return None


def load_logged_in_user_data():
    session_user_id = session.get('user_id', None)
    user_data = get_user_data(session_user_id)
    if not 'user_data' in g:
        g.user_data = user_data


def get_user_data(user_id):
    query = 'select * from users where id = ?'
    result = get_db().execute(query, (user_id,))
    row = result.fetchone()
    if row:
        # TODO: load only necessary data to g, not the whole dict
        return dict(row)
    return None


def get_caregivers_children(user_id):
    # TODO remove _update_with_bans_and_points_data to data_access/bans.py
    def _update_with_bans_and_points_data(children):
        new_children = []
        for child in children:
            child = dict(child)
            child['bans'] = check_bans_status(child['id'])
            child['child_points'] = get_child_points(child['id'])
            new_children.append(child)
        return new_children

    query = """
    SELECT u.* 
    FROM caregiver_to_child AS ctc 
    JOIN users AS u on ctc.child_id = u.id
    WHERE ctc.caregiver_id = ?
    AND u.role = 'child'
    """
    result = get_db().execute(query, (user_id,))
    children = result.fetchall()
    children = _update_with_bans_and_points_data(children)
    return children


def get_child_data(child_id):
    query = """
    SELECT u.* 
    FROM caregiver_to_child AS ctc 
    JOIN users AS u on ctc.child_id = u.id
    WHERE ctc.child_id = ?
    AND u.role = 'child'
    """
    result = get_db().execute(query, (child_id,))
    child = dict(result.fetchone())
    child['bans'] = check_bans_status(child_id)
    return child


def is_child_under_caregiver(child_id, caregiver_id):
    query = "SELECT * FROM caregiver_to_child WHERE child_id = ? AND caregiver_id = ?"
    result = get_db().execute(query, (child_id, caregiver_id))
    return result.fetchone()


def update_password(user_id, hashed_new_password):
    query = "UPDATE users SET password = ? WHERE id = ?"
    params = (hashed_new_password, user_id)
    get_db().cursor().execute(query, params)
    get_db().commit()


def add_new_user(user_data):
    query = "INSERT INTO 'users' " \
            "(username, password, role, firstname) " \
            "VALUES (?, ?, ?, ?) "

    get_db().execute(query, user_data)
    get_db().commit()


def get_user_id(username):
    query = """
    SELECT id FROM users
    WHERE username = ?
    """
    result = get_db().execute(query, (username,))
    row = result.fetchone()
    if row:
        return row['id']
    return False


def associate_child_with_caregiver(caregiver_id, child_id):
    query = "INSERT INTO 'caregiver_to_child' " \
            "(caregiver_id, child_id)" \
            "VALUES (?, ?)"

    get_db().execute(query, (caregiver_id, child_id))
    get_db().commit()


def update_firstname(user_id, new_firstname):
    query = "UPDATE users SET firstname = ? WHERE id = ?"
    params = (new_firstname, user_id)
    get_db().cursor().execute(query, params)
    get_db().commit()


def get_username_id_and_role_by_username(username):
    query = 'select id, role from users where username = ?'
    result = get_db().execute(query, (username,))
    row = result.fetchone()
    if row:
        return dict(row)
    return None
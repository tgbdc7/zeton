from datetime import datetime

from flask import session, g

from zeton.data_access.bans import check_bans_status

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
    def _update_with_bans_data(children):
        new_children = []
        for child in children:
            child = dict(child)
            child['bans'] = check_bans_status(child['id'])
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
    children = _update_with_bans_data(children)
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
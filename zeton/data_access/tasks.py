from zeton.db import get_db

def get_tasks(child_id):
    query = "SELECT * FROM home_points WHERE user_id = ? ORDER BY points LIMIT 10"
    result = get_db().execute(query, (child_id,))
    return result.fetchall()

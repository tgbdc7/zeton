from zeton.db import get_db

def get_prizes(child_id):
    query = "SELECT * FROM prizes WHERE user_id = ? ORDER BY points"
    result = get_db().execute(query, (child_id,))
    return result.fetchall()
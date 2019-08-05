from datetime import datetime, timedelta

from flask import g


def parse_iso_timestamp(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")


def get_points(user_id):
    query = 'select points from users where id = ?'
    result = g.db.cursor().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['points']
    return None


def subtract_points(user_id, points):
    query = 'update users SET points = points - ? WHERE id = ?;'
    g.db.cursor().execute(query, [points, user_id])
    g.db.commit()


def get_weekly_highscore(user_id):
    query = 'select school_weekly_highscore from users where id = ?'
    result = g.db.cursor().execute(query, [user_id])
    row = result.fetchone()
    if row:
        return row['school_weekly_highscore']
    return None


def add_points(user_id, points):
    query = 'UPDATE users SET points = points + ? WHERE id = ?;'
    g.db.cursor().execute(query, [points, user_id])
    g.db.commit()


def get_user_data(user_id):
    query = 'select * from users where id = ?'
    result = g.db.cursor().execute(query, (user_id,))
    row = result.fetchone()
    if row:
        return dict(row)
    return None


#
# def _add_ban_data(children):
#     new_children = []
#     for child in children:
#         child = dict(child)
#         ban_data = get_last_active_ban(child['id'])
#         if ban_data:
#             child['ban'] = ban_data
#         new_children.append(child)
#     return new_children

def _update_bans_data(children):
    new_children = []
    for child in children:
        child = dict(child)
        child['bans'] = check_bans_status(child['id'])
        new_children.append(child)
    return new_children


def get_caregivers_children(user_id):
    query = """
    SELECT u.* 
    FROM caregiver_to_child AS ctc 
    JOIN users AS u on ctc.child_id = u.id
    WHERE ctc.caregiver_id = ?
    AND u.role = 'child'
    """
    result = g.db.cursor().execute(query, (user_id,))
    children = result.fetchall()
    children = _update_bans_data(children)
    return children


def get_bans_name(child_id):
    query = 'select ban_id, ban_name from bans_name where child_id = ? ORDER BY ban_id'
    result = g.db.cursor().execute(query, [child_id, ])
    result = dict(result.fetchall())
    return result


def get_all_bans(child_id):
    query = 'select * from bans where child_id = ? ORDER BY ban_id'
    bans = g.db.cursor().execute(query, [child_id])
    result = {}
    for ban in bans.fetchall():
        result[ban[2]] = {'start': ban[3], 'stop': ban[4]}

    return result


def check_bans_status(child_id):
    all_bans = get_all_bans(child_id)
    bans_name = get_bans_name(child_id)
    result = {}
    for ban_id, ban_name in bans_name.items():
        try:
            start = datetime.fromisoformat(all_bans[ban_id]['start'])
            stop = datetime.fromisoformat(all_bans[ban_id]['stop'])
            if datetime.now() < stop:
                active = True
            else:
                active = False

            # start1 = datetime.fromisoformat(all_bans[ban_id]['start'])
            # start = ('{:%Y-%m-%d %H:%M}'.format(start1))
            #
            # stop1 = datetime.fromisoformat(all_bans[ban_id]['stop'])
            # stop=('{:%Y-%m-%d %H:%M}'.format(stop1))
            #
            # if datetime.now() < stop1:
            #     active = True
            # else:
            #     active = False
        except KeyError:
            start = None
            stop = None
            active = False
        result[ban_id] = {'name': ban_name, 'active': active, 'start': start, 'stop': stop}

    return result


def get_child_data(child_id):
    query = """
    SELECT u.* 
    FROM caregiver_to_child AS ctc 
    JOIN users AS u on ctc.child_id = u.id
    WHERE ctc.child_id = ?
    AND u.role = 'child'
    """
    result = g.db.cursor().execute(query, (child_id,))
    child = dict(result.fetchone())
    child['bans'] = check_bans_status(child_id)
    return child


#
# def get_last_active_ban(user_id):
#     all_bans = get_all_bans(user_id)
#     # sqlite3 nie wspiera typu datetime, więc obliczenia trzeba zrobić samemu
#     for ban_id, _, start, end in reversed(all_bans):
#         start = parse_iso_timestamp(start)
#         end = parse_iso_timestamp(end)
#
#         if start < datetime.now() < end:
#             return {'ban_id': ban_id, 'start': start, 'end': end}


def set_to_midnight(dt):
    midnight = datetime.min.time()
    return datetime.combine(dt.date(), midnight)


def calculate_end_time_warn(start, ban_id):
    if ban_id <= 3:
        end = set_to_midnight(start + timedelta(days=1))
    elif ban_id == 4:
        end = start + timedelta(minutes=30)
    elif ban_id >= 5:
        end = start + timedelta(days=1)

    return end.isoformat()


def update_warn_per_ban_id(child_id, ban_id):
    start = datetime.now()
    start_timestamp = start.isoformat()

    end_timestamp = calculate_end_time_warn(start, ban_id)
    query = 'UPDATE bans SET  start_timestamp =  ?, end_timestamp = ? WHERE child_id = ? AND ban_id = ?'
    params = (start_timestamp, end_timestamp, child_id, ban_id)
    g.db.cursor().execute(query, params)
    g.db.commit()


def add_warn_per_ban_id(child_id, ban_id):
    start = datetime.now()
    start_timestamp = start.isoformat()
    end_timestamp = calculate_end_time_warn(start, ban_id)
    query = 'INSERT INTO bans valueS (NULL, ?, ?, ?, ?)'
    params = (child_id, ban_id, start_timestamp, end_timestamp)
    g.db.cursor().execute(query, params)
    g.db.commit()


def give_warn(child_id):
    bans_status = check_bans_status(child_id)
    for ban_id, ban in bans_status.items():
        if not ban['start']:
            return add_warn_per_ban_id(child_id, ban_id)
        elif not ban['active']:
            return update_warn_per_ban_id(child_id, ban_id)


def give_kick(child_id):
    bans_status = check_bans_status(child_id)
    #TODO - ustawić warny 1-2 na aktywne
    if not bans_status[3]['start']:
        return add_warn_per_ban_id(child_id, 3)
    elif not bans_status[3]['active']:
        return update_warn_per_ban_id(child_id, 3)
    else:
        # TODO dać komunikat do użytkownika
        pass


def give_ban(child_id, duration_minutes):
    bans_status = check_bans_status(child_id)
    start = datetime.now()
    start_timestamp = start.isoformat()
    try:
        if bans_status[6]['start']:
            # jeśli jest wpis bazie to robimy update

            # sprawdzamy czy ban jest aktualnie aktywny
            if bans_status[6]['active']:
                # jeśli jest aktywny to aktualizujemy czas końca bana
                end = bans_status[6]['stop'] + timedelta(minutes=duration_minutes)
                end_timestamp = end.isoformat()
                query = 'UPDATE bans SET   end_timestamp = ? WHERE child_id = ? AND ban_id = ?'
                params = (end_timestamp, child_id, 6)

            else:
                # jeśli jest ban ale nieaktywny to ustawimy czasy od początku,
                end = start + timedelta(minutes=duration_minutes)
                end_timestamp = end.isoformat()
                query = 'UPDATE bans SET  start_timestamp =  ?, end_timestamp = ? WHERE child_id = ? AND ban_id = ?'
                params = (start_timestamp, end_timestamp, child_id, 6)

        else:
            # jeśli nie ma wpisu w bazie to robimy nowy wpis
            end = start + timedelta(minutes=duration_minutes)
            end_timestamp = end.isoformat()
            query = 'INSERT INTO bans valueS (NULL, ?, ?, ?, ?)'
            params = (child_id, 6, start_timestamp, end_timestamp)

        g.db.cursor().execute(query, params)
        g.db.commit()

    except IndexError as e:
        print(e)


def is_child_under_caregiver(child_id, caregiver_id):
    query = "SELECT * FROM caregiver_to_child WHERE child_id = ? AND caregiver_id = ?"
    result = g.db.cursor().execute(query, (child_id, caregiver_id))
    return result.fetchone()

from datetime import datetime, timedelta

from zeton.db import get_db


def get_bans_name(child_id):
    query = 'select ban_id, ban_name from bans_name where child_id = ? ORDER BY ban_id'
    result = get_db().execute(query, [child_id, ])
    result = dict(result.fetchall())
    return result


def get_all_bans(child_id):
    query = 'select * from bans where child_id = ? ORDER BY ban_id'
    bans = get_db().execute(query, [child_id])
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


        except KeyError:
            start = None
            stop = None
            active = False
        result[ban_id] = {'name': ban_name, 'active': active, 'start': start, 'stop': stop}

    return result


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
    get_db().execute(query, params)
    get_db().commit()


def add_warn_per_ban_id(child_id, ban_id):
    start = datetime.now()
    start_timestamp = start.isoformat()
    end_timestamp = calculate_end_time_warn(start, ban_id)
    query = 'INSERT INTO bans VALUES (NULL, ?, ?, ?, ?)'
    params = (child_id, ban_id, start_timestamp, end_timestamp)
    get_db().execute(query, params)
    get_db().commit()


def give_warn(child_id):
    bans_status = check_bans_status(child_id)
    for ban_id, ban in bans_status.items():
        if not ban['start']:
            return add_warn_per_ban_id(child_id, ban_id)
        elif not ban['active']:
            return update_warn_per_ban_id(child_id, ban_id)


def give_kick(child_id):
    bans_status = check_bans_status(child_id)
    # TODO - ustawić warny 1-2 na aktywne
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
            query = 'INSERT INTO bans VALUES (NULL, ?, ?, ?, ?)'
            params = (child_id, 6, start_timestamp, end_timestamp)

        get_db().execute(query, params)
        get_db().commit()

    except IndexError as e:
        print(e)


def is_child_under_caregiver(child_id, caregiver_id):
    query = "SELECT * FROM caregiver_to_child WHERE child_id = ? AND caregiver_id = ?"
    result = g.db.cursor().execute(query, (child_id, caregiver_id))
    return result.fetchone()

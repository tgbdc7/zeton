from datetime import datetime, timedelta

from zeton.db import get_db

DEFAULT_BANS = [
    (1, '1 ustne ostrzeżenie'),
    (2, '2 ustne ostrzeżenie'),
    (3, 'KICK Przerwanie obecnej aktywności i udanie się do pokoju'),
    (4, 'BAN 2 stopnia na 30 min - brak komputera i telefonu'),
    (5, 'BAN 1 stopnia na 24h - brak telefonu'),
    (6, 'BAN 2 stopnia na 24h - brak komputera i telefonu'),
]


def insert_default_ban(target_id, ban_id, ban_name):
    query = "INSERT INTO  'bans_name' VALUES (NULL, ?, ?, ?)"
    params = (target_id, ban_id, ban_name)

    get_db().execute(query, params)
    get_db().commit()


def insert_all_default_bans(target_id):
    for values in DEFAULT_BANS:
        ban_id, ban_name = values
        insert_default_ban(target_id, ban_id, ban_name)


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


def get_most_important_warn_ban(child_id):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    query = 'select bans_name.ban_id, bans_name.ban_name, bans.start_timestamp, bans.end_timestamp from bans ' \
            f'inner JOIN bans_name ON bans.id=bans_name.ban_id where bans_name.child_id={child_id} ' \
            f'and bans.child_id={child_id} and bans.end_timestamp>\'{now}\' order by bans_name.ban_id desc'
    bans = get_db().execute(query)

    try:
        result = bans.fetchone()
        raw_start = result["start_timestamp"].replace('T', ' ').split(':')
        raw_end = result["end_timestamp"].replace('T', ' ').split(':')
        start = f'{raw_start[0]}:{raw_start[1]}'
        end = f'{raw_end[0]}:{raw_end[1]}'

        info_str = f'{result["ban_name"]} Od: {start} Do: {end};red'
    except:
        info_str = 'brak aktywnych warnów/banów;green'

    return info_str


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


def update_warn_per_ban_id(target_id, ban_id):
    start = datetime.now()
    start_timestamp = start.isoformat()

    end_timestamp = calculate_end_time_warn(start, ban_id)
    query = 'UPDATE bans SET  start_timestamp =  ?, end_timestamp = ? WHERE child_id = ? AND ban_id = ?'
    params = (start_timestamp, end_timestamp, target_id, ban_id)
    get_db().execute(query, params)
    get_db().commit()


def add_warn_per_ban_id(target_id, ban_id):
    start = datetime.now()
    start_timestamp = start.isoformat()
    end_timestamp = calculate_end_time_warn(start, ban_id)
    query = 'INSERT INTO bans VALUES (NULL, ?, ?, ?, ?)'
    params = (target_id, ban_id, start_timestamp, end_timestamp)
    get_db().execute(query, params)
    get_db().commit()


def give_warn(target_id, logged_user_id):
    # TODO add information to db about who give warn `logged_user_id` 
    bans_status = check_bans_status(target_id)
    for ban_id, ban in bans_status.items():
        if not ban['start']:
            return add_warn_per_ban_id(target_id, ban_id)
        elif not ban['active']:
            return update_warn_per_ban_id(target_id, ban_id)


def give_kick(target_id, logged_user_id):
    # TODO add information to db about who give kick `logged_user_id` 
    bans_status = check_bans_status(target_id)
    # TODO - ustawić warny 1-2 na aktywne
    if not bans_status[3]['start']:
        return add_warn_per_ban_id(target_id, 3)
    elif not bans_status[3]['active']:
        return update_warn_per_ban_id(target_id, 3)
    else:
        # TODO dać komunikat do użytkownika
        pass


def give_ban(target_id, duration_minutes, logged_user_id):
    # TODO add information to db about who give ban `logged_user_id` 
    bans_status = check_bans_status(target_id)
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
                params = (end_timestamp, target_id, 6)

            else:
                # jeśli jest ban ale nieaktywny to ustawimy czasy od początku,
                end = start + timedelta(minutes=duration_minutes)
                end_timestamp = end.isoformat()
                query = 'UPDATE bans SET  start_timestamp =  ?, end_timestamp = ? WHERE child_id = ? AND ban_id = ?'
                params = (start_timestamp, end_timestamp, target_id, 6)

        else:
            # jeśli nie ma wpisu w bazie to robimy nowy wpis
            end = start + timedelta(minutes=duration_minutes)
            end_timestamp = end.isoformat()
            query = 'INSERT INTO bans VALUES (NULL, ?, ?, ?, ?)'
            params = (target_id, 6, start_timestamp, end_timestamp)

        get_db().execute(query, params)
        get_db().commit()

    except IndexError as e:
        print(e)

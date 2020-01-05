from zeton.views import bp

from flask import render_template, abort, g, get_flashed_messages

from zeton import auth
from zeton.data_access import users, prizes, tasks, points, bans


@bp.route('/task_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def task_detail(child_id):
    child = users.get_child_data(child_id)
    childs_tasks = tasks.get_tasks(child_id)
    childs_points_history = points.get_points_history(child_id)
    role = g.user_data['role']
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'childs_tasks': childs_tasks,
               'childs_points_history': childs_points_history,
               'role': role,
               'child_points': child_points,
               "firstname": g.user_data['firstname']
               }

    return render_template('tasks/task_detail.html', **context)


@bp.route('/prizes_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def prizes_detail(child_id):
    role = g.user_data['role']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)

    childs_prizes = prizes.get_prizes(child_id)
    child_points = points.get_child_points(child['id'])
    childs_points_history = points.get_points_history(child_id)

    context = {'child': child,
               'childs_prizes': childs_prizes,
               'role': role,
               'child_points': child_points,
               'childs_points_history': childs_points_history,
               "firstname": g.user_data['firstname']
               }

    return render_template('prizes/prizes_detail.html', **context)


@bp.route('/school_points_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def school_points_detail(child_id):
    role = g.user_data['role']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'role': role,
               'child_points': child_points,
               "firstname": g.user_data['firstname']}

    return render_template('school_points/school_points_detail.html', **context)


@bp.route('/bans_detail/<child_id>')
@auth.login_required
@auth.logged_child_or_caregiver_only
def bans_detail(child_id):
    role = g.user_data['role']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)
    child_points = points.get_child_points(child['id'])
    info = bans.get_most_important_warn_ban(child_id).split(';')
    info_str = info[0]
    info_bck = info[1]

    context = {'child': child,
               'role': role,
               'child_points': child_points,
               'info_str': info_str,
               'info_bck': info_bck,
               "firstname": g.user_data['firstname']}

    return render_template('bans/bans_detail.html', **context)


@bp.route('/prizes_detail/<child_id>/add_prize')
@auth.login_required
@auth.caregiver_only
def add_prize(child_id):
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)
    child = users.get_child_data(child_id)

    context = {'user_data': user_data,
               'child': child}

    messages = get_flashed_messages()

    return render_template('prizes/add_prize.html', **context, messages=messages)


@bp.route('/prizes_detail/<child_id>/edit_prize/<prize_id>')
@auth.login_required
@auth.caregiver_only
def edit_prize(child_id, prize_id):
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)
    child = users.get_child_data(child_id)
    child_id = int(child_id)
    prize_id = int(prize_id)
    prize = prizes.get_prize(child_id, prize_id)

    context = {'user_data': user_data,
               'child': child,
               'prize': prize}

    messages = get_flashed_messages()

    return render_template('prizes/edit_prize.html', **context, messages=messages)


@bp.route('/task_detail/<child_id>/add_task')
@auth.login_required
@auth.caregiver_only
def add_task(child_id):
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)
    child = users.get_child_data(child_id)

    context = {'user_data': user_data,
               'child': child}

    messages = get_flashed_messages()

    return render_template('tasks/add_task.html', **context, messages=messages)


@bp.route('/task_detail/<child_id>/edit_task/<task_id>')
@auth.login_required
@auth.caregiver_only
def edit_task(child_id, task_id):
    logged_user_id = g.user_data['id']
    child_id = int(child_id)
    user_data = users.get_user_data(logged_user_id)
    child = users.get_child_data(child_id)
    task = tasks.get_task_by_tasks_id(child_id, task_id)

    context = {'user_data': user_data,
               'child': child,
               'task': task}

    messages = get_flashed_messages()

    return render_template('tasks/edit_task.html', **context, messages=messages)

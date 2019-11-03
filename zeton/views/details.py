from zeton.views import bp

from flask import render_template, abort, g, get_flashed_messages

from zeton import auth
from zeton.data_access import users, prizes, tasks, points


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
               'child_points': child_points
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
               'childs_points_history': childs_points_history
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
               'child_points': child_points}

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

    context = {'child': child,
               'role': role,
               'child_points': child_points}

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

    return render_template('add_prize.html', **context, messages=messages)


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

    return render_template('edit_prize.html', **context, messages=messages)

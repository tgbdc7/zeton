from zeton.views import bp

from flask import render_template, g, get_flashed_messages

from zeton import auth
from zeton.data_access import users, prizes, tasks, points


@bp.route('/')
@auth.login_required
def index():
    role = g.user_data['role']
    logged_user_id = g.user_data['id']

    template = None
    context = {}

    if role == 'caregiver':
        children = users.get_caregivers_children(logged_user_id)
        template = 'index_caregiver.html'

        context.update({"firstname": g.user_data['firstname'],
                        "role": role,
                        "children": children})

    elif role == 'child':

        template = 'index_child.html'
        child = users.get_child_data(logged_user_id)
        child_points = points.get_child_points(child['id'])
        childs_tasks = tasks.get_tasks(logged_user_id)
        childs_prizes = prizes.get_prizes(logged_user_id)
        context = {'child': child,
                   'child_points': child_points,
                   'childs_tasks': childs_tasks,
                   'childs_prizes': childs_prizes}

    messages = get_flashed_messages()

    return render_template(template, **context, messages=messages)


@bp.route('/child/<child_id>')
@auth.login_required
@auth.caregiver_only
def child(child_id):
    child = users.get_child_data(child_id)
    childs_tasks = tasks.get_tasks(child_id)
    childs_prizes = prizes.get_prizes(child_id)
    role = g.user_data['role']
    child_points = points.get_child_points(child['id'])

    context = {'child': child,
               'childs_tasks': childs_tasks,
               'childs_prizes': childs_prizes,
               'role': role,
               'child_points': child_points}

    messages = get_flashed_messages()

    return render_template('caregiver_panel.html', **context, messages=messages)

from flask import request, redirect, flash

from zeton.data_access.tasks import delete_childs_task, add_new_task, update_task, get_task_id_by_name

from zeton import auth
from zeton.api import bp


@bp.route("/child/<child_id>/tasks/delete/<task_id>", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def delete_task(child_id, task_id):
    child_id = int(child_id)
    task_id = int(task_id)

    delete_childs_task(child_id, task_id)

    return redirect(request.referrer)


@bp.route("/child/<child_id>/tasks/add", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def add_task(child_id):
    child_id = int(child_id)

    name = request.form['name']
    points = request.form['points']
    max_day = request.form['max_day']
    max_week = request.form['max_week']

    if not (name == '' or points == '' or max_day == '' or max_week == ''):
        add_new_task(child_id, name, points, max_day, max_week, 1)
        flash('Zadanie zostało dodane')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(request.referrer)


@bp.route("/child/<child_id>/tasks/update", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def update_tasks(child_id):
    child_id = int(child_id)

    tasks_name = request.form['tasks_name']
    name = request.form['name']
    points = request.form['points']
    max_day = request.form['max_day']
    max_week = request.form['max_week']

    tasks_id = get_task_id_by_name(child_id, tasks_name)

    if not (name == '' or points == '' or max_day == '' or max_week == ''):
        update_task(child_id, name, points, max_day, max_week, 1, tasks_id)
        flash('Zadanie zostało zmienione')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(request.referrer)

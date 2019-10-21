from flask import request, redirect, flash

from zeton.data_access.tasks import deactivate_task, add_new_task, update_task

from zeton import auth
from zeton.api import bp


@bp.route("/child/<child_id>/tasks/deactivate/<task_id>", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def deactivate_tasks(child_id, task_id):
    child_id = int(child_id)
    task_id = int(task_id)

    deactivate_task(child_id, task_id)

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

    points=int(points)

    if points > 0:
        if not (name == '' or points == '' or max_day == '' or max_week == ''):
            add_new_task(child_id, name, points, max_day, max_week, 1)
            flash('Zadanie zostało dodane')
        else:
            flash('Wypełnij wszystkie pola')
    else:
        flash('Liczba punktów musi być dodatnia')
    return redirect(request.referrer)


@bp.route("/child/<child_id>/tasks/<task_id>/update", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def update_tasks(child_id, task_id):
    child_id = int(child_id)
    task_id = int(task_id)

    name = request.form['name']
    points = request.form['points']
    max_day = request.form['max_day']
    max_week = request.form['max_week']

    points=int(points)

    if points > 0:
        if not (name == '' or points == '' or max_day == '' or max_week == ''):
            update_task(child_id, name, points, max_day, max_week, 1, task_id)
            flash('Zadanie zostało zmienione')
        else:
            flash('Wypełnij wszystkie pola')
    else:
        flash('Liczba puntków musi być dodatnia')

    return redirect(request.referrer)

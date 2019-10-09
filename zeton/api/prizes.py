from flask import request, redirect, flash

from zeton.data_access.prizes import delete_childs_prize, add_new_prize, update_prize, get_prize_id_by_name


from zeton import auth
from zeton.api import bp


@bp.route("/child/<child_id>/prizes/delete/<prizes_id>", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def delete_prizes(child_id, prizes_id):
    child_id = int(child_id)

    prizes_id = int(prizes_id)

    delete_childs_prize(child_id, prizes_id)

    return redirect(request.referrer)


@bp.route("/child/<child_id>/prizes/add", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def add_prizes(child_id):
    child_id = int(child_id)

    name = request.form['name']
    points = int(request.form['points'])
    max_day = int(request.form['max_day'])
    max_week = int(request.form['max_week'])
    max_month = int(request.form['max_month'])

    if not (name == '' or points == '' or max_day == '' or max_week == '' or max_month == ''):
        add_new_prize(child_id, name, points, max_day, max_week, max_month)
        flash('Nagroda została dodana')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(request.referrer)


@bp.route("/child/<child_id>/prizes/update", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def update_prizes(child_id):
    child_id = int(child_id)


    prizes_name = request.form['prizes_name']
    name = request.form['name']
    points = int(request.form['points'])
    max_day = int(request.form['max_day'])
    max_week = int(request.form['max_week'])
    max_month = int(request.form['max_month'])

    prizes_id = get_prize_id_by_name(child_id, prizes_name)

    if not (prizes_name == '' or name == '' or points == '' or max_day == '' or max_week == ''):
        update_prize(child_id, name, points, max_day, max_week, max_month, prizes_id)
        flash('Zadanie zostało zmienione')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(request.referrer)
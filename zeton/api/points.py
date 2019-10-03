from flask import request, redirect, url_for, abort, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

import zeton.data_access.bans
import zeton.data_access.points
from zeton import auth
from zeton.api import bp
from zeton.data_access import users


@bp.route("/child/<child_id>/points/add", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def add_points(child_id):
    logged_user_id = g.user_data['id']

    try:
        added_points = int(request.form['liczba_punktow'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if added_points > 0:
        zeton.data_access.points.change_points_by(child_id, added_points, logged_user_id)
        zeton.data_access.points.add_exp(added_points, child_id)

    return redirect(url_for('views.child', child_id=child_id))


@bp.route("/child/<child_id>/points/use", methods=['POST'])
@auth.login_required
@auth.logged_child_or_caregiver_only
def use_points(child_id):
    logged_user_id = g.user_data['id']
    child_id = int(child_id)

    return_url = request.args.get('return_url', '/')

    current_points = zeton.data_access.points.get_only_points(child_id)
    try:
        used_points = int(request.form['points'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if used_points > 0:
        if used_points <= current_points:
            zeton.data_access.points.change_points_by(child_id, -used_points, logged_user_id)
        else:
            missing_points = abs(current_points - used_points)
            if missing_points == 1:
                points_word = 'punktu'
            else:
                points_word = 'punktów'
            flash(f'Do tej nagrody brakuje Ci:  {missing_points} {points_word}')

    return redirect(return_url)


@bp.route("/settings/<child_id>/set_password", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def set_child_password(child_id):
    logged_user_id = g.user_data['id']
    child = users.get_child_data(child_id)
    child_password = child['password']

    password = request.form['password']
    new_password = request.form['new_password']
    repeat_new_password = request.form['repeat_new_password']

    hashed_new_password = generate_password_hash(new_password)

    if not logged_user_id:
        return abort(403)

    if not (password == '' or new_password == '' or repeat_new_password == ''):
        if new_password == repeat_new_password:
            if auth.password_validation(new_password):
                if check_password_hash(child_password, password):
                    users.update_password(child['id'], hashed_new_password)
                    flash('Nowe hasło wprowadzone poprawnie')
                flash('Aktualne hasło zostało źle wprowadzone. Spróbuj ponownie')
            flash('Hasło musi zawierać 1 dużą literę, 1 małą literę, 1 cyfrę i musi mieć długość 8 znaków')
        flash('Nowe hasło i powtórzone nowe hasło muszą się zgadzać. Spróbuj ponownie')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(url_for('views.child_password_change', child_id=child_id))


@bp.route('/settings/<child_id>/set_firstname', methods=['POST'])
@auth.login_required
@auth.caregiver_only
def set_child_firstname(child_id):
    child = users.get_child_data(child_id)

    new_firstname = request.form.get('new_firstname')

    if new_firstname:
        users.update_firstname(child_id, new_firstname)
    else:
        flash('Wprowadź imię')
    flash('Imię zostało zmienione')

    return redirect(url_for('views.child_firstname_change', child_id=child_id))

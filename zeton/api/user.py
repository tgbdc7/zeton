from flask import request, redirect, url_for, g, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash

from zeton import auth
from zeton.api import bp
from zeton.data_access import users
from zeton.data_access.bans import insert_all_default_bans


@bp.route('/settings/set_password', methods=['POST'])
@auth.login_required
def set_password():
    logged_user_id = g.user_data['id']
    logged_user_password = g.user_data['password']

    password = request.form['password']
    new_password = request.form['new_password']
    repeat_new_password = request.form['repeat_new_password']

    hashed_new_password = generate_password_hash(new_password)

    if not logged_user_id:
        return abort(403)

    if not (password == '' or new_password == '' or repeat_new_password == ''):
        if new_password == repeat_new_password:
            if auth.password_validation(new_password):
                if check_password_hash(logged_user_password, password):
                    users.update_password(logged_user_id, hashed_new_password)
                    flash('Nowe hasło wprowadzone poprawnie')
                flash('Aktualne hasło zostało źle wprowadzone. Spróbuj ponownie')
            flash('Hasło musi zawierać 1 dużą literę, 1 małą literę, 1 cyfrę i musi mieć długość 8 znaków')
        flash('Nowe hasło i powtórzone nowe hasło muszą się zgadzać. Spróbuj ponownie')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(url_for('views.password_change'))


@bp.route("/user", methods=['POST'])
def register():
    users.load_logged_in_user_data()
    username = request.form['username'].lower()
    password = request.form['password']
    email = request.form['email']
    password_hash = generate_password_hash(password)
    role = request.form.get('role') or 'caregiver'
    firstname = request.form.get('name') or username

    data = (username, password_hash, role, firstname, email)

    if username is None or password is None:
        abort(400)
    if users.get_user_id(username) or users.get_email_address(email) :
        abort(400)  # user already exists

    users.add_new_user(data)

    if role == 'child':
        child_id = users.get_user_id(username)

        caregiver_id = g.user_data['id']
        users.associate_child_with_caregiver(caregiver_id, child_id)
        insert_all_default_bans(child_id)

    return redirect(url_for('views.index'))


@bp.route('/settings/set_firstname', methods=['POST'])
@auth.login_required
def set_firstname():
    logged_user_id = g.user_data['id']

    new_firstname = request.form.get('new_firstname')

    if new_firstname:
        users.update_firstname(logged_user_id, new_firstname)
    else:
        flash('Wprowadź imię')
    flash('Imię zostało zmienione')

    return redirect(url_for('views.firstname_change'))

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

@bp.route('/<child_id>/assign/set_caregiver_to_child', methods=['POST'])
@auth.login_required
@auth.caregiver_only
def set_caregiver_to_child(child_id):
    child_id = int(child_id)

    caregiver_username_to_child = request.form.get('caregiver_username_to_child')
    caregiver_data = users.get_username_id_and_role_by_username(caregiver_username_to_child)

    if caregiver_data and caregiver_data['role'] == 'caregiver':
        if not users.is_child_under_caregiver(child_id, caregiver_data['id']):
            users.associate_child_with_caregiver(caregiver_data['id'], child_id)
            flash('Opiekun został przydzielony do dziecka')
        else:
            flash('Podany opiekun już był przydzielony')
    else:
        flash('Wprowadź poprawny login (username) opiekuna')

    return redirect(url_for('views.add_caregiver_to_child', child_id=child_id))


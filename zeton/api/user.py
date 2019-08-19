from flask import request, redirect, url_for, g, flash, get_flashed_messages, abort

from zeton import auth
from zeton.api import bp
from zeton.data_access import users
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route('/settings/set_password', methods=['POST'])
@auth.login_required
def set_password():
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']
    logged_user_password = g.user_data['password']
    user_data = users.get_user_data(logged_user_id)

    password = request.form['password']
    new_password = request.form['new_password']
    repeat_new_password = request.form['repeat_new_password']

    hashed_new_password = generate_password_hash(new_password)

    if not logged_user_id:
        return abort(403)

    if not (password == '' or new_password == '' or repeat_new_password == ''):
        if new_password == repeat_new_password:
            if user_data:
                if check_password_hash(logged_user_password, password):
                    users.update_password(logged_user_id, hashed_new_password)
                    flash('Nowe hasło wprowadzone poprawnie')
                flash('Aktualne hasło zostało źle wprowadzone. Spróbuj ponownie')
        flash('Nowe hasło i powtórzone nowe hasło muszą się zgadzać. Spróbuj ponownie')
    else:
        flash('Wypełnij wszystkie pola')

    return redirect(url_for('views.user_settings'))
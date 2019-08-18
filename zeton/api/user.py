from flask import request, redirect, url_for, g, flash, get_flashed_messages

from zeton import auth
from zeton.api import bp
from zeton.data_access import users
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route('/settings/set_password', methods=['POST'])
@auth.login_required
def set_password():
    # if request.method == 'GET':
    #     users.load_logged_in_user_data()
    #     logged_user_id = g.user_data['id']
    #     user_data = users.get_user_data(logged_user_id)
    #     # user_id = int(user_id)
    #
    #     context = {'user_data': user_data}
    #     messages = get_flashed_messages()
    #
    #     return render_template('user_settings.html', **context, messages=messages)

    # if request.method == 'POST':

    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']
    logged_user_password = g.user_data['password']
    user_data = users.get_user_data(logged_user_id)

    password = request.form['password']
    new_password = request.form['new_password']
    repeat_new_password = request.form['repeat_new_password']

    hashed_new_password = generate_password_hash(new_password)

    if new_password == repeat_new_password:
        if user_data:
            if check_password_hash(logged_user_password, password):
                users.update_password(logged_user_id, hashed_new_password)
                # flash('Nowe hasło wprowadzone poprawnie')
            # else:
                # flash('Aktualne hasło zostało źle wprowadzone. Spróbuj ponownie')
    # else:
    #     flash('Nowe hasło i powtórzone nowe hasło muszą się zgadzać. Spróbuj ponownie')

    return redirect(url_for('views.user_settings'))
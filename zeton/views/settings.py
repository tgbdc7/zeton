from zeton.views import bp

from flask import render_template, g, get_flashed_messages

from zeton import auth
from zeton.data_access import users


@bp.route('/settings/')
@auth.login_required
def user_settings():
    return render_template('user_settings.html')


@bp.route('/settings/password')
@auth.login_required
def password_change():
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'user_data': user_data}
    messages = get_flashed_messages()

    return render_template('password_change.html', **context, messages=messages)

from zeton.views import bp

from flask import render_template, g, get_flashed_messages

from zeton import auth
from zeton.data_access import users


@bp.route('/settings/')
@auth.login_required
def user_settings():
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)
    role = user_data['role']

    context = {'user_data': user_data,
               'role': role}

    return render_template('user/user_settings.html', **context)


@bp.route('/settings/password')
@auth.login_required
def password_change():
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'user_data': user_data}
    messages = get_flashed_messages()

    return render_template('user/password_change.html', **context, messages=messages)


@bp.route('/settings/firstname')
@auth.login_required
def firstname_change():
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'user_data': user_data}
    messages = get_flashed_messages()

    return render_template('user/firstname_change.html', **context, messages=messages)


@bp.route('/child-settings/<child_id>')
@auth.login_required
def child_settings(child_id):
    child = users.get_child_data(child_id)

    context = {'child': child}

    return render_template('user/child_settings.html', **context)


@bp.route('/child-settings/<child_id>/password')
@auth.login_required
@auth.caregiver_only
def child_password_change(child_id):
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)
    child = users.get_child_data(child_id)

    context = {'child': child,
               'user_data': user_data
               }

    messages = get_flashed_messages()

    return render_template('user/child_password_change.html', **context, messages=messages)


@bp.route('/child-settings/<child_id>/firstname')
@auth.login_required
@auth.caregiver_only
def child_firstname_change(child_id):
    child = users.get_child_data(child_id)
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'child': child,
               'user_data': user_data}

    messages = get_flashed_messages()

    return render_template('user/child_firstname_change.html', **context, messages=messages)


@bp.route('/settings/admin/permissions')
# @auth.login_required
@auth.caregiver_only
def manage_permissions():
    group_members = [1,2,4]
    context = {'group_members':group_members}
    messages = None
    return render_template('permissions.html', **context, messages=messages)

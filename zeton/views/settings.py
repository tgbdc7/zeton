from zeton.views import bp

from flask import render_template, g, get_flashed_messages, session

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
def list_family_members():
    family_id = users.get_family_id(g.user_data['id'])
    family_members_by_id = [user['family_member'] for user in  users.get_family_members(family_id)]
    members_role = [users.get_user_role(user_id) for user_id in
                    family_members_by_id]
    family_members_by_name = [users.get_username(user_id) for user_id
                              in family_members_by_id]
    family_members_by_name_and_id = zip(family_members_by_name,
                                        family_members_by_id)
    family_member_data = {}
    for member_name in family_members_by_name:
        family_member_data[member_name] = {}
    for index, item in enumerate(family_member_data.values()):
        item['id'] = family_members_by_id[index]
        item['name'] = family_members_by_name[index]
        item['role'] = members_role[index]
    context = {'members_data': family_member_data}
    return render_template('permissions/permissions.html', **context)


@bp.route('/settings/admin/permissions/<int:user_id>', methods=['GET'])
@bp.route('/settings/admin/permissions/<int:user_id>/<int:child_id>')
def manage_permissions(user_id, child_id=None):
    session['target_user_id'] = user_id
    session['child_id'] = child_id
    used_permissions = auth.get_used_permissions(
        user_id, auth.permissions)
    unused_permissions = auth.get_unused_permissions(user_id, auth.permissions)

    if users.get_user_role(user_id) in auth.SUPERVISING_ROLES and child_id is None:
        user_id = session.get('target_user_id')
        children_under_caregiver = users.get_caregivers_children(user_id)
        context = {'children_under_caregiver': children_under_caregiver, 'user_id': user_id}

        return render_template('permissions/permissions_children_list.html', **context)
    if child_id is not None:
        used_permissions = auth.get_used_permissions(
            user_id,
            auth.permissions,
            assigned_user_id=child_id
        )
        unused_permissions = auth.get_unused_permissions(
            user_id,
            auth.permissions,
            assigned_user_id=child_id
        )

    context = {'used_permissions': used_permissions,
               'unused_permissions': unused_permissions}
    return render_template('permissions/permissions_list.html', **context)

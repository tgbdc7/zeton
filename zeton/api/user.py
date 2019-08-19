from flask import request, url_for, g
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from data_access import users
from zeton.api import bp
from data_access.users import add_new_user, associate_child_with_caregiver, get_child_id


@bp.route("/user", methods=['POST'])
def register():
    users.load_logged_in_user_data()
    username = request.form['username']
    password = request.form['password']
    password_hash = generate_password_hash(password)
    role = request.form.get('role') or 'caregiver'
    firstname = request.form.get('name') or '-'

    data = (username, password_hash, role, firstname)
    try:
        add_new_user(data)
    except Exception as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if role == 'child':
        try:
            child_id = get_child_id(username)
            caregiver_id = g.user_data['id']
            associate_child_with_caregiver(caregiver_id, child_id)
        except Exception as ex:
            print(ex)
            return {'message': 'Bad request'}, 400

    return redirect(url_for('views.index'))

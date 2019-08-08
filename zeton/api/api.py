from flask import Blueprint, session, request, redirect, url_for, abort

from zeton import auth, db, data_access

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/child/<target_id>/points/add", methods=['POST'])
@auth.login_required
def dodaj_punkt(target_id):
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    try:
        nowe_punkty = int(request.form['liczba_punktow'])
    except ValueError as ex:
        print(ex)
    else:
        if nowe_punkty > 0:
            data_access.change_points_by(target_id, nowe_punkty)
    finally:
        return redirect(url_for('views.child', child_id=target_id))


@bp.route("/child/<child_id>/points/use", methods=['POST'])
@auth.login_required
def use_points(child_id):
    if request.method == 'POST':
        db.get_db()
        logged_user_id = session.get('user_id', None)
        child_id = int(child_id)

        return_url = request.args.get('return_url', '/')

        if not (child_id == logged_user_id or data_access.is_child_under_caregiver(child_id, logged_user_id)):
            return abort(403)

        current_points = data_access.get_points(child_id)

        try:
            used_points = int(request.form['points'])
            if used_points > 0:
                if used_points <= current_points:
                    data_access.change_points_by(child_id, -1 * used_points)
        except ValueError as ex:
            return {'message': 'Bad request'}, 400

    return redirect(return_url)


@bp.route("/ban/<target_id>")
@auth.login_required
def give_ban(target_id):
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    ten_minutes = 10
    data_access.give_ban(target_id, ten_minutes)
    return redirect(url_for('views.child', child_id=target_id))


@bp.route("/warn/<target_id>")
@auth.login_required
def give_warn(target_id):
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    data_access.give_warn(target_id)
    return redirect(url_for('views.child', child_id=target_id))


@bp.route("/kick/<target_id>")
@auth.login_required
def give_kick(target_id):
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    data_access.give_kick(target_id)
    return redirect(url_for('views.child', child_id=target_id))

from flask import Blueprint, session, request, redirect, url_for, abort

from . import auth, db, data_access

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/dodaj_punkt/<target_id>", methods=['POST'])
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
            data_access.add_points(target_id, nowe_punkty)
    finally:
        return redirect(url_for('views.child', child_id=target_id))


@bp.route("/wykorzystanie_punktow/<target_id>", methods=['POST'])
@auth.login_required
def wykorzystaj_punkty(target_id):
    db.get_db()
    USER_ID = session.get('user_id', None)
    current_points = data_access.get_points(target_id)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    if request.method == 'POST':
        try:
            used_points = int(request.form['points_to_be_used'])
            if used_points > 0:
                if used_points < current_points or used_points == current_points:
                    data_access.subtract_points(target_id, used_points)
        except Exception as e:
            print(e)

    return redirect(url_for('views.child', child_id=target_id))


@bp.route("/ban/<target_id>")
@auth.login_required
def daj_bana(target_id):
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    ten_minutes = 10
    data_access.give_ban(target_id, ten_minutes)
    return redirect(url_for('views.child', child_id=target_id))

@bp.route("/warn/<target_id>")
@auth.login_required
def daj_warna(target_id):
    #TODO
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    data_access.give_warn(target_id)
    return redirect(url_for('views.child', child_id=target_id))

@bp.route("/kick/<target_id>")
@auth.login_required
def daj_kicka(target_id):
    #TODO
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(target_id, USER_ID):
        return abort(403)

    data_access.give_kick(target_id)
    return redirect(url_for('views.child', child_id=target_id))
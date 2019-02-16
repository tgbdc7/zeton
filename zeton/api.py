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


@bp.route("/wykorzystanie_punktow", methods=['POST', 'GET'])
@auth.login_required
def wykorzystaj_punkty():
    if request.method == 'POST':
        # TODO: zaimplementować wykorzystywanie punktów
        return redirect(url_for('views.index'))


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

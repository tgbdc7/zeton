from flask import request, redirect

from zeton.data_access.prizes import delete_childs_prize


from zeton import auth
from zeton.api import bp


@bp.route("/child/<child_id>/prizes/delete/<prizes_id>", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def delete_prizes(child_id, prizes_id):
    child_id = int(child_id)

    prizes_id = int(prizes_id)

    delete_childs_prize(child_id, prizes_id)

    return redirect(request.referrer)


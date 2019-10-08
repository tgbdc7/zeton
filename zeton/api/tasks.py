from flask import request, redirect

from zeton.data_access.tasks import delete_childs_task

from zeton import auth
from zeton.api import bp


@bp.route("/child/<child_id>/tasks/delete/<task_id>", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def delete_task(child_id, task_id):
    child_id = int(child_id)
    task_id = int(task_id)

    delete_childs_task(child_id, task_id)

    return redirect(request.referrer)

from flask import request, redirect, url_for, abort, g, flash

from zeton.data_access.tasks import get_tasks, delete_childs_task
from zeton.data_access import users, tasks


from zeton import auth
from zeton.api import bp
from zeton.views import details


@bp.route("/child/<child_id>/tasks/delete/<task_id>", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def delete_task(child_id, task_id):
    child_id = int(child_id)

    task_id = int(task_id)

    delete_childs_task(child_id, task_id)

    return redirect(request.referrer)


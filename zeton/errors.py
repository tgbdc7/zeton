"""
 error handlers
"""
from flask import render_template, Blueprint

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def handle_404(err):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def handle_500(err):
    return render_template('errors/500.html'), 500


@bp.app_errorhandler(403)
def handle_403(err):
    return render_template('errors/403.html'), 403

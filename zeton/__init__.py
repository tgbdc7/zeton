"""
Aplikacja: system żetonowy ucznia/dziecka

"""

from flask import Flask
import os

from . import auth, views, db
from zeton.api import api
from zeton.custom_jinja2_filters import jinja2_ban_datetime_filter


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='AplikacjaDlaStasia',
        DATABASE=os.path.join(app.root_path, '..', 'db.sqlite'),
        SITE_NAME='Zeton'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.teardown_appcontext(db.close_db)

    app.add_template_filter(jinja2_ban_datetime_filter, 'ban_time')

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(api.bp)

    return app

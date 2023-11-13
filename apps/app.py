from pathlib import Path

from apps.config import config
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    from apps.auth import views as auth_views
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app


def page_not_found(e):
    return render_template("404.html"), 404


def internal_server_error(e):
    return render_template("500.html"), 500

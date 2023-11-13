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

    from apps.schejule import views as sche_views
    
    app.register_blueprint(sche_views.schejule, url_prefix="/schejule")
    return app
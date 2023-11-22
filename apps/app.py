from pathlib import Path

from apps.config import config
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

db = SQLAlchemy()
csrf = CSRFProtect()
scheduler = BackgroundScheduler()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    from apps.schejule import views as sche_views
    from apps.schejule.dbmanage import UpdateStream

    app.register_blueprint(sche_views.schejule, url_prefix="/schejule")

    scheduler.add_job(UpdateStream, trigger=CronTrigger(hour=5, minute=30,id="job2"))
    scheduler.add_job(UpdateStream, trigger=CronTrigger(hour=11, minute=0,id="job3"))
    scheduler.add_job(UpdateStream, trigger=CronTrigger(hour=18, minute=0,id="job4")) 
    scheduler.start()

    return app
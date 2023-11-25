from pathlib import Path
from apps.config import config
from apps.youtubeinfo import YouTubeInfo
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

db = SQLAlchemy()
csrf = CSRFProtect()
scheduler = BackgroundScheduler()
youtubeinfo = YouTubeInfo()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    from apps.schejule import views as sche_views
    from apps.schejule.dbmanage import UpdateCall,ResetQuota

    app.register_blueprint(sche_views.schejule, url_prefix="/schejule")

    # scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=5, minute=45, timezone="Asia/Tokyo"))
    # scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=10, minute=10, timezone="Asia/Tokyo"))
    # scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=10, minute=45, timezone="Asia/Tokyo"))
    # scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=14, minute=45, timezone="Asia/Tokyo"))
    # scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=17, minute=45, timezone="Asia/Tokyo"))
    # scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=20, minute=45, timezone="Asia/Tokyo"))
    # scheduler.add_job(ResetQuota, trigger=CronTrigger(hour=9, minute=21, timezone="Asia/Tokyo"))
 
    scheduler.start()

    return app
from flask import Blueprint, redirect, render_template, url_for, request, flash
from datetime import datetime
from apps.schejule.forms import RegisterForm
from apps.schejule.models import  Channel, Stream
import apps.schejule.dbmanage as dbmanage
from apps.app import db

schejule = Blueprint(
    "schejule",
    __name__,
    template_folder="templates",
)

@schejule.route("/")
def index():
    streams = (
        db.session.query(Channel, Stream)
        .join(Stream)
        .order_by(Stream.starttime)
        .all()
    )

    date_group = {}
    # for stream in streams:
    #     date_key = stream.starttime.data()
    #     if date_key not in date_group:
    #         date_group[date_key] = []
    #     date_group[date_key].append(stream)

    form = RegisterForm()

    return render_template(
        "schejule/index.html",
        date_group=date_group,
        form=form,
    )

@schejule.route("/register", methods=["POST"])
def channel_register():
    form = RegisterForm()
    if form.validate_on_submit():
        url = form.channel_url.data
        dbmanage.RegisterChannel(url)
        return redirect(url_for("schejule.index"))
    flash("チャンネルの形式がおかしいです！")
    return redirect(url_for("schejule.index")) 

@schejule.route("/update", methods=["POST"])
def stream_update():
    dbmanage.UpdateStream()
    
    return redirect(url_for("schejule.index")) 
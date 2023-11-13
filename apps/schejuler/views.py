from flask import Blueprint, redirect, render_template, url_for
from datetime import datetime
from apps.schejuler.forms import RegisterForm
from apps.schejuler.model import  Channel, Stream

schejule = Blueprint(
    "schejule",
    __name__,
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
    for stream in streams:
        date_key = stream.starttime.date()
        if date_key not in date_group:
            date_group[date_key] = []
        date_group[date_key].append(stream)

    register_form = RegisterForm()

    return render_template(
        "schejuler/index.html",
        date_group=date_group,
        register_form=register_form,
    )
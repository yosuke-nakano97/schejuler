from apps.app import db
from apps.schejule.models import Channel
from sqlalchemy.exc import IntegrityError
from flask import flash

def RegisterChannel(info):
    print(info)
    try:
        channel = Channel(
            id=info[1],
            name=info[0],
            icon_path=info[2],
            playlist=info[3]
        )
        db.session.add(channel)
        db.session.commit()
    except IntegrityError as e:
        flash("チャンネルは既に登録済みです")
        return 0
    flash("登録完了")

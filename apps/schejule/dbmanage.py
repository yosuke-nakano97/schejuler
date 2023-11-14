from apps.app import db
from apps.schejule.models import Channel
import apps.programs.register as register
from sqlalchemy.exc import IntegrityError
from flask import flash

def RegisterChannel(url):

    info = register.GetChannelInfo(url)
    try:
        # 基本系列：新しくレコードを作成する
        channel = Channel(
            id=info[1],
            name=info[0],
            icon_path=info[2],
            playlist=info[3]
        )
        db.session.add(channel)
        db.session.commit()
        flash("登録完了")
    except IntegrityError as e:
        # IDとそれに対応するデーターがもうあった場合：
        if (UpdateChannel(info)!=0):
            flash("something worng in RegisterChannel")
        
def DeleteChannel(ch_id):
    # IDをもらってきて対応するレコードを削除
    try:
        db.session.delete(
            session.query(Channel).filter_by(id==ch_id).first()
        )
        session.commit()
    except Exception as e:
        flash("something wrong in DeleteChannel")
        print(e)

def UpdateChannel(info):
    try:
        db.session.rollback()
        channel = db.session.query(Channel).filter_by(id=info[1]).first()
        channel.name = info[0]
        channel.icon_path = info[2]
        db.session.commit()
        flash("更新完了")
        return 0
    except Exception as e:
        flash("something wrong in UpdateChannel")
        print(e)
        return 1



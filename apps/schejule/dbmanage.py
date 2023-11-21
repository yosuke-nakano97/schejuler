from apps.app import db
from apps.schejule.models import Channel,Stream
import apps.programs.channel as ch
import apps.programs.stream as st
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from flask import flash
from datetime import datetime
import pytz


def RegisterChannel(url):

    info = ch.GetChannelInfo(url)
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
        db.session.close()
        flash("登録完了")

    except Exception as e:
        db.session.rollback()
        UpdateChannel(info)
        print(e)
    finally:
        if db.session is not None:
            db.session.close()
       
def DeleteChannel(ch_id):
    # IDをもらってきて対応するレコードを削除
    try:
        db.session.delete(
            session.query(Channel).filter_by(id==ch_id).first()
        )
        db.session.commit()
        db.session.close()

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
        db.session.close()
        flash("更新完了")
        return 1
    except Exception as e:
        flash("something wrong in UpdateChannel")
        print(e)
        return 0

def UpdateStream():
    # 今の時間よりもStarttimeが遅いものを削除する
    try:
        system_timezone = pytz.timezone('Asia/Jakarta')
        current_time=datetime.now()
        current_time_jst_minus_two = current_time.astimezone(system_timezone)
        db.session.query(Stream).filter(Stream.starttime < current_time_jst_minus_two).delete()
        db.session.commit()

    except Exception as e:
        # 削除で問題発生
        db.session.rollback()
        print(f"UpdateSteam:delete{e}")

    finally:
        db.session.close()
        
    # チャンネルIDもらってビデオIDもらって登録する
    channels = db.session.query(Channel).all()
    for channel in channels:
        print(channel)
        video_ids = st.GetRecentVideoId(channel.playlist)
        for video_id in video_ids:
            print(f"videoid:{video_id}")
            info = st.GetstreamInfo(video_id)
            print(f"info:{info}")
            if info is not None:
                if RegisterStream(info,channel.id)!=0:
                    UpdateStreamInfo(info)
    flash("update完了")

def RegisterStream(info,ch_id):
    try:
        # 基本系列：新しくレコードを作成する
        stream = Stream(
            id=info[0],
            channel_id=ch_id,
            title=info[1],
            thumbnail_path=info[3],
            starttime=info[2],
        )
        db.session.add(stream)
        db.session.commit()
        return 0

    except Exception as e:
        # IDとそれに対応するデーターがもうあった場合：
        db.session.rollback()
        # 更新処理
        if (UpdateStreamInfo(info)!=0):
            # 更新が失敗
            flash("something wrong in Register Stream")
        return 1

def DeleteStream(id):
    try:
        db.session.query(Stream).filter(Stream.id == id).delete()
        db.session.commit()
        flash("削除完了")
        return 0

    except Exception as e:
        db.session.rollback()
        flash("削除失敗")
        print(e)
        return 1 

    finally:
        db.session.close()

def UpdateStreamInfo(info):
    try:
        print(info[0])
        stream = db.session.query(Stream).filter_by(id=info[0]).first()
        stream.title = info[1]
        stream.thumbnail_path = info[3]
        stream.starttime = info[2]
        db.session.commit()
        flash("更新完了")
        return 0
    except Exception as e:
        db.session.rollback()
        flash("something wrong in UpdatestreamInfo")
        print(f"errorrrrrrrrrrrrrrrrrrrr{e}")
        return 1
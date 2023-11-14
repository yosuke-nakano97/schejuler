from datetime import datetime
from apps.app import db

class Channel(db.Model):
    __tablename__ = "channel"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, index=True)
    icon_path = db.Column(db.String, unique=True)
    playlist = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_images = db.relationship("Stream", backref="channel", order_by="desc(Stream.starttime)")

class Stream(db.Model):
    __tablename__ = "stream"
    id = db.Column(db.String, primary_key=True)
    channel_id = db.Column(db.String, db.ForeignKey('channel.id'))
    title = db.Column(db.String)
    thumbnail_path = db.Column(db.String, unique=True)
    starttime = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
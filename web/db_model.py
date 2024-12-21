from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ImageInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, nullable=False)
    group_index = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)


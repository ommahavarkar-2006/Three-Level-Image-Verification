from datetime import datetime
from app.extensions import db


class ImagePassword(db.Model):
    __tablename__ = 'image_passwords'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    encrypted_image_sequence = db.Column(db.Text, nullable=False)  # JSON array of image IDs in order
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

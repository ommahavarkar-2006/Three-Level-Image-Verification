from datetime import datetime
from app.extensions import db


class AuthenticationLog(db.Model):
    __tablename__ = 'authentication_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    authentication_level = db.Column(db.Integer, nullable=False)  # 1, 2, or 3
    status = db.Column(db.String(20), nullable=False)  # 'success' or 'failed'
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

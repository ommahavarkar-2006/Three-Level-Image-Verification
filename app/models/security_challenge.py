from datetime import datetime
from app.extensions import db


class SecurityChallenge(db.Model):
    __tablename__ = 'security_challenges'

    id = db.Column(db.Integer, primary_key=True)
    challenge_type = db.Column(db.String(50), nullable=False)  # e.g., 'select_bicycles', 'select_cars'
    challenge_data = db.Column(db.Text, nullable=False)  # JSON: {prompt, images: [{id, src, is_correct}], correct_ids: [...]}
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

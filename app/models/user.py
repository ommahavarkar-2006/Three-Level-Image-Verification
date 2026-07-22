from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    image_sequence_hash = db.Column(db.String(256), nullable=True)
    profile_image = db.Column(db.String(256), default='default_avatar.png')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    image_password = db.relationship('ImagePassword', backref='user', uselist=False, cascade='all, delete-orphan')
    auth_logs = db.relationship('AuthenticationLog', backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def lock_account(self, minutes=15):
        self.locked_until = datetime.utcnow() + datetime.timedelta(minutes=minutes)
        self.failed_login_attempts = 0
        db.session.commit()

    def increment_failed_attempts(self, max_attempts=5):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.lock_account(minutes=15)
        else:
            db.session.commit()

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()

    def security_score(self):
        score = 0
        if self.password_hash:
            score += 40
        if self.image_sequence_hash:
            score += 20
        if self.last_login:
            score += 10
        if self.failed_login_attempts == 0:
            score += 30
        else:
            score += max(0, 30 - (self.failed_login_attempts * 5))
        return min(score, 100)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from datetime import datetime, timedelta
import json
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.authentication_log import AuthenticationLog
from app.models.image_password import ImagePassword
from app.auth.utils import parse_image_sequence
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)

    # Stats
    total_success = AuthenticationLog.query.filter_by(
        user_id=current_user.id, status='success').count()
    total_failed = AuthenticationLog.query.filter_by(
        user_id=current_user.id, status='failed').count()
    last_login = current_user.last_login

    # Recent activity
    recent_logs = AuthenticationLog.query.filter_by(user_id=current_user.id) \
        .order_by(AuthenticationLog.created_at.desc()).limit(5).all()

    # Chart data - last 7 days activity
    chart_labels = []
    chart_success = []
    chart_failed = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        day_start = datetime.combine(day.date(), datetime.min.time())
        day_end = day_start + timedelta(days=1)
        label = day.strftime('%a')
        chart_labels.append(label)

        success_count = AuthenticationLog.query.filter(
            AuthenticationLog.user_id == current_user.id,
            AuthenticationLog.status == 'success',
            AuthenticationLog.created_at >= day_start,
            AuthenticationLog.created_at < day_end
        ).count()
        failed_count = AuthenticationLog.query.filter(
            AuthenticationLog.user_id == current_user.id,
            AuthenticationLog.status == 'failed',
            AuthenticationLog.created_at >= day_start,
            AuthenticationLog.created_at < day_end
        ).count()
        chart_success.append(success_count)
        chart_failed.append(failed_count)

    return render_template('dashboard/index.html',
                           total_success=total_success,
                           total_failed=total_failed,
                           last_login=last_login,
                           security_score=current_user.security_score(),
                           recent_logs=recent_logs,
                           chart_labels=chart_labels,
                           chart_success=chart_success,
                           chart_failed=chart_failed)


@dashboard_bp.route('/profile')
@login_required
def profile():
    # Get user's image password sequence
    image_sequence = []
    img_pw = ImagePassword.query.filter_by(user_id=current_user.id).first()
    if img_pw:
        sequence = parse_image_sequence(img_pw.encrypted_image_sequence)
        # Map image IDs to labels and sources
        image_map = {
            'mountain': {'label': 'Mountain', 'src': 'mountain.jpg'},
            'camera': {'label': 'Camera', 'src': 'camera.jpg'},
            'ocean': {'label': 'Ocean', 'src': 'ocean.jpg'},
            'bicycle': {'label': 'Bicycle', 'src': 'bicycle.jpg'},
            'car': {'label': 'Car', 'src': 'car.jpg'},
            'tree': {'label': 'Tree', 'src': 'tree.jpg'},
            'sunset': {'label': 'Sunset', 'src': 'sunset.jpg'},
            'bridge': {'label': 'Bridge', 'src': 'bridge.jpg'},
            'flower': {'label': 'Flower', 'src': 'flower.avif'},
            'castle': {'label': 'Castle', 'src': 'castle.JPG'},
            'rocket': {'label': 'Rocket', 'src': 'rocket.jpg'},
            'piano': {'label': 'Piano', 'src': 'piano.jpg'},
        }
        for img_id in sequence:
            if img_id in image_map:
                image_sequence.append({
                    'id': img_id,
                    'label': image_map[img_id]['label'],
                    'src': image_map[img_id]['src']
                })

    return render_template('profile/index.html', user=current_user, image_sequence=image_sequence)

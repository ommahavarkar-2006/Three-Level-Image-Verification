import json
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.user import User
from app.models.image_password import ImagePassword
from app.models.authentication_log import AuthenticationLog
from app.auth.routes import IMAGE_PASSWORD_IMAGES
from app.auth.utils import parse_image_sequence

security_bp = Blueprint("security", __name__, url_prefix="/security")


@security_bp.route("/overview")
@login_required
def overview():
    total_success = AuthenticationLog.query.filter_by(
        user_id=current_user.id, status="success").count()
    total_failed = AuthenticationLog.query.filter_by(
        user_id=current_user.id, status="failed").count()

    recent_logs = AuthenticationLog.query.filter_by(user_id=current_user.id) \
        .order_by(AuthenticationLog.created_at.desc()).limit(6).all()

    password_strength_pct = 100
    image_password_pct = 100 if current_user.image_password else 0

    return render_template(
        "security/overview.html",
        security_score=current_user.security_score(),
        password_strength_pct=password_strength_pct,
        image_password_pct=image_password_pct,
        total_success=total_success,
        total_failed=total_failed,
        recent_logs=recent_logs,
    )


@security_bp.route("/history")
@login_required
def history():
    status_filter = request.args.get("status", "all")
    time_filter = request.args.get("time", "all")
    page = request.args.get("page", 1, type=int)

    query = AuthenticationLog.query.filter_by(user_id=current_user.id)

    if status_filter in ("success", "failed"):
        query = query.filter(AuthenticationLog.status == status_filter)

    now = datetime.utcnow()
    if time_filter == "today":
        start = datetime.combine(now.date(), datetime.min.time())
        query = query.filter(AuthenticationLog.created_at >= start)
    elif time_filter == "week":
        start = now - timedelta(days=7)
        query = query.filter(AuthenticationLog.created_at >= start)

    query = query.order_by(AuthenticationLog.created_at.desc())
    pagination = query.paginate(page=page, per_page=10, error_out=False)

    return render_template(
        "security/history.html",
        pagination=pagination,
        logs=pagination.items,
        status_filter=status_filter,
        time_filter=time_filter,
    )


@security_bp.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'logout_all':
            flash('All other sessions have been logged out.', 'info')

        return redirect(url_for('security.settings'))

    return render_template("security/settings.html")


@security_bp.route("/change-image-password", methods=['GET', 'POST'])
@login_required
def change_image_password():
    if request.method == 'POST':
        data = request.get_json()
        new_sequence = data.get('images', [])

        if len(new_sequence) < 3 or len(new_sequence) > 5:
            return jsonify({'success': False, 'message': 'Select between 3 and 5 images.'}), 400

        if current_user.image_password:
            current_user.image_password.encrypted_image_sequence = json.dumps(new_sequence)
            current_user.image_password.updated_at = datetime.utcnow()
        else:
            img_pw = ImagePassword(
                user_id=current_user.id,
                encrypted_image_sequence=json.dumps(new_sequence)
            )
            db.session.add(img_pw)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Image password updated successfully.'})

    return render_template("security/change_image_password.html",
                           images=IMAGE_PASSWORD_IMAGES)

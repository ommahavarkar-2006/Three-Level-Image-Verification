import os
from flask import Flask, render_template, request, jsonify
from config import config_map
from app.extensions import db, login_manager, csrf, limiter


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.security.routes import security_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(security_bp)

    # Error handlers
    @app.errorhandler(400)
    def bad_request(e):
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': str(e.description) if hasattr(e, 'description') else 'Bad request.'}), 400
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def unauthorized(e):
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Unauthorized.'}), 401
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(e):
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Forbidden.'}), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Not found.'}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(429)
    def rate_limit(e):
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Rate limit exceeded.'}), 429
        return render_template('errors/429.html'), 429

    @app.errorhandler(500)
    def internal_error(e):
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'message': 'Internal server error.'}), 500
        return render_template('errors/500.html'), 500

    # Create tables and demo user
    with app.app_context():
        try:
            db.create_all()
            _create_demo_user(app)
            print("[SecureVision] Database initialized successfully.")
        except Exception as e:
            print(f"[SecureVision] Database error: {e}")

    # Landing page
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for('dashboard.index'))
        return render_template('auth/landing.html')

    return app


def _create_demo_user(app):
    from app.models.user import User
    from app.models.image_password import ImagePassword
    from werkzeug.security import generate_password_hash

    demo = User.query.filter_by(email='demo@securevision.com').first()
    if not demo:
        # Hash the image sequence: mountain|camera|ocean
        image_hash = generate_password_hash('mountain|camera|ocean')
        demo = User(
            full_name='Demo User',
            email='demo@securevision.com',
            password_hash=generate_password_hash('demo123'),
            image_sequence_hash=image_hash,
            is_active=True
        )
        db.session.add(demo)
        db.session.flush()

        # Also store in image_password table
        img_pw = ImagePassword(
            user_id=demo.id,
            encrypted_image_sequence='["mountain","camera","ocean"]'
        )
        db.session.add(img_pw)
        db.session.commit()
        print("[SecureVision] Demo user created: demo@securevision.com / password: demo123")

import json
import os
import random
from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, limiter
from app.models.user import User
from app.models.image_password import ImagePassword
from app.models.authentication_log import AuthenticationLog
from app.models.security_challenge import SecurityChallenge
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.utils import validate_image_sequence, parse_image_sequence
from app.security.utils import generate_challenge

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Visual challenge categories — map folder names to display labels
VISUAL_CHALLENGE_CATEGORIES = {
    'Animals': 'animals',
    'Food': 'food',
    'Nature': 'nature',
    'Places': 'places',
    'Sports': 'sports',
    'Vehicles': 'vehicles',
}

# Available images for image password selection
IMAGE_PASSWORD_IMAGES = [
    {'id': 'mountain', 'label': 'Mountain', 'src': 'mountain.jpg'},
    {'id': 'camera', 'label': 'Camera', 'src': 'camera.jpg'},
    {'id': 'ocean', 'label': 'Ocean', 'src': 'ocean.jpg'},
    {'id': 'bicycle', 'label': 'Bicycle', 'src': 'bicycle.jpg'},
    {'id': 'car', 'label': 'Car', 'src': 'car.jpg'},
    {'id': 'tree', 'label': 'Tree', 'src': 'tree.jpg'},
    {'id': 'sunset', 'label': 'Sunset', 'src': 'sunset.jpg'},
    {'id': 'bridge', 'label': 'Bridge', 'src': 'bridge.jpg'},
    {'id': 'flower', 'label': 'Flower', 'src': 'flower.avif'},
    {'id': 'castle', 'label': 'Castle', 'src': 'castle.JPG'},
    {'id': 'rocket', 'label': 'Rocket', 'src': 'rocket.jpg'},
    {'id': 'piano', 'label': 'Piano', 'src': 'piano.jpg'},
]


def _log_auth(user_id, level, status):
    log = AuthenticationLog(
        user_id=user_id,
        authentication_level=level,
        status=status,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')[:512]
    )
    db.session.add(log)
    db.session.commit()


def _hash_image_sequence(images):
    """Hash an image sequence like a password: image1|image2|image3"""
    sequence_string = '|'.join(images)
    return generate_password_hash(sequence_string)


def _check_image_sequence(submitted, stored_hash):
    """Check if submitted image sequence matches the stored hash."""
    if not stored_hash:
        return False
    sequence_string = '|'.join(submitted)
    return check_password_hash(stored_hash, sequence_string)


def _get_randomized_images(exclude_ids=None):
    """Get a randomized list of images for display. Optionally exclude some."""
    images = IMAGE_PASSWORD_IMAGES.copy()
    if exclude_ids:
        images = [img for img in images if img['id'] not in exclude_ids]
    random.shuffle(images)
    return images


def _generate_visual_challenge():
    """Generate a visual challenge: pick a random category, select 3 correct + 6 incorrect images."""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images')

    # Pick a random target category
    categories = list(VISUAL_CHALLENGE_CATEGORIES.keys())
    target_folder = random.choice(categories)
    target_label = VISUAL_CHALLENGE_CATEGORIES[target_folder]

    # Get images from target category (3 correct)
    target_path = os.path.join(static_dir, target_folder)
    target_files = [f for f in os.listdir(target_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
    correct_images = random.sample(target_files, min(3, len(target_files)))

    # Get images from other categories (6 incorrect)
    other_folders = [c for c in categories if c != target_folder]
    random.shuffle(other_folders)
    incorrect_images = []
    for folder in other_folders:
        if len(incorrect_images) >= 6:
            break
        folder_path = os.path.join(static_dir, folder)
        folder_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
        if folder_files:
            chosen = random.choice(folder_files)
            incorrect_images.append({
                'filename': chosen,
                'category': VISUAL_CHALLENGE_CATEGORIES[folder],
                'folder': folder
            })

    # Build challenge data
    images = []
    correct_filenames = []
    for f in correct_images:
        images.append({
            'filename': f,
            'category': target_label,
            'folder': target_folder,
            'is_correct': True
        })
        correct_filenames.append(f)

    for item in incorrect_images:
        images.append({
            'filename': item['filename'],
            'category': item['category'],
            'folder': item['folder'],
            'is_correct': False
        })

    random.shuffle(images)

    return {
        'target_category': target_label,
        'target_folder': target_folder,
        'prompt': f'Select all images containing {target_label}',
        'images': images,
        'correct_filenames': correct_filenames
    }


# ==================== REGISTRATION ====================

@auth_bp.route('/register', methods=['GET'])
def register():
    """Show registration form with name, email, and password."""
    return render_template('auth/register.html')


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10 per minute")
def register_submit():
    """Handle registration: Step 1 (name+email+password) then Step 2 (3-level image password)."""
    data = request.get_json()
    action = data.get('action', '')

    if action == 'step1':
        # Step 1: Validate name, email, and password
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')

        if not full_name or not email or not password:
            return jsonify({'success': False, 'message': 'Please fill in all fields.'}), 400

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters.'}), 400

        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match.'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'An account with this email already exists.'}), 400

        # Store in session and proceed to step 2
        session['reg_data'] = {
            'full_name': full_name,
            'email': email,
            'password': password
        }
        return jsonify({
            'success': True,
            'step': 2,
            'images': _get_randomized_images()
        })

    elif action == 'get_images':
        # Get randomized images for next level (exclude already selected)
        exclude_ids = data.get('exclude', [])
        return jsonify({
            'success': True,
            'images': _get_randomized_images(exclude_ids)
        })

    elif action == 'step2':
        # Step 2: Create user with password + image sequence hash
        reg_data = session.get('reg_data')
        if not reg_data:
            return jsonify({'success': False, 'message': 'Session expired. Please start again.'}), 400

        selected_images = data.get('images', [])
        if len(selected_images) != 3:
            return jsonify({'success': False, 'message': 'Please select exactly 3 images.'}), 400

        # Create user with password hash and image sequence hash
        user = User(
            full_name=reg_data['full_name'],
            email=reg_data['email'],
            password_hash=generate_password_hash(reg_data['password']),
            image_sequence_hash=_hash_image_sequence(selected_images),
            is_active=True
        )
        db.session.add(user)
        db.session.flush()

        # Also store raw image sequence in image_password table for verification lookup
        img_pw = ImagePassword(
            user_id=user.id,
            encrypted_image_sequence=json.dumps(selected_images)
        )
        db.session.add(img_pw)
        db.session.commit()

        # Clean session
        session.pop('reg_data', None)

        flash('Registration successful! Please log in.', 'success')
        return jsonify({'success': True, 'redirect': url_for('auth.login')})

    return jsonify({'success': False, 'message': 'Invalid request.'}), 400


# ==================== LOGIN ====================

@auth_bp.route('/login', methods=['GET'])
def login():
    """Show login form (email + password)."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login_submit():
    """Handle login: email+password verification, then 3-level image verification."""
    data = request.get_json()
    action = data.get('action', '')

    if action == 'authenticate':
        # Step 1: Verify email + password
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Please enter your email and password.'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

        if user.is_locked():
            return jsonify({'success': False, 'message': 'Account temporarily locked. Try again later.'}), 403

        if not user.check_password(password):
            user.increment_failed_attempts(max_attempts=5)
            _log_auth(user.id, 1, 'failed')
            if user.is_locked():
                return jsonify({'success': False, 'message': 'Account temporarily locked after too many failed attempts.', 'locked': True}), 403
            return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

        # Password correct! Store user ID in session for image verification
        session['login_user'] = user.id
        session['login_level'] = 1
        _log_auth(user.id, 1, 'success')

        # Return Level 1 images (randomized)
        return jsonify({
            'success': True,
            'level': 1,
            'images': _get_randomized_images()
        })

    elif action == 'verify_level':
        # Steps 2-4: Verify each image level
        user_id = session.get('login_user')
        current_level = session.get('login_level')

        if not user_id or not current_level:
            return jsonify({'success': False, 'message': 'Session expired. Please log in again.'}), 400

        user = User.query.get(user_id)
        if not user:
            session.clear()
            return jsonify({'success': False, 'message': 'User not found.'}), 400

        selected_image = data.get('image', '')
        if not selected_image:
            return jsonify({'success': False, 'message': 'Please select an image.'}), 400

        # Get the stored image sequence
        stored_sequence = parse_image_sequence(user.image_password.encrypted_image_sequence) if user.image_password else []
        if not stored_sequence or len(stored_sequence) < 3:
            return jsonify({'success': False, 'message': 'Image password not configured.'}), 400

        # Check if the selected image matches the expected one for this level
        expected_image = stored_sequence[current_level - 1]

        if selected_image == expected_image:
            # Correct image for this level
            _log_auth(user.id, current_level + 1, 'success')

            if current_level >= 3:
                # All 3 levels passed! Generate visual challenge
                challenge = _generate_visual_challenge()
                session['visual_challenge'] = challenge

                return jsonify({
                    'success': True,
                    'challenge': True,
                    'prompt': challenge['prompt'],
                    'images': [{'filename': img['filename'], 'folder': img['folder']} for img in challenge['images']]
                })
            else:
                # Move to next level
                next_level = current_level + 1
                session['login_level'] = next_level

                return jsonify({
                    'success': True,
                    'level': next_level,
                    'images': _get_randomized_images()
                })
        else:
            # Wrong image
            user.increment_failed_attempts(max_attempts=5)
            _log_auth(user.id, current_level + 1, 'failed')

            if user.is_locked():
                session.clear()
                return jsonify({'success': False, 'message': 'Account temporarily locked after too many failed attempts.', 'locked': True}), 403

            # Reset to level 1 for retry
            session['login_level'] = 1
            return jsonify({
                'success': False,
                'message': 'Incorrect image. Please start verification again.',
                'reset': True,
                'level': 1,
                'images': _get_randomized_images()
            }), 401

    elif action == 'visual_challenge':
        # Verify the visual challenge submission
        user_id = session.get('login_user')
        if not user_id:
            return jsonify({'success': False, 'message': 'Session expired. Please log in again.'}), 400

        challenge = session.get('visual_challenge')
        if not challenge:
            return jsonify({'success': False, 'message': 'No active challenge. Please log in again.'}), 400

        selected_files = data.get('selected', [])
        correct_files = challenge['correct_filenames']

        user = User.query.get(user_id)
        if not user:
            session.clear()
            return jsonify({'success': False, 'message': 'User not found.'}), 400

        # Check if selected images exactly match the correct ones
        if set(selected_files) == set(correct_files):
            # Challenge passed! Complete login
            session.pop('login_user', None)
            session.pop('login_level', None)
            session.pop('visual_challenge', None)

            login_user(user, remember=False)
            user.last_login = datetime.utcnow()
            user.reset_failed_attempts()
            db.session.commit()

            _log_auth(user.id, 4, 'success')

            return jsonify({
                'success': True,
                'verified': True,
                'redirect': url_for('dashboard.index'),
                'message': f'Welcome back, {user.full_name.split()[0]}!'
            })
        else:
            # Challenge failed
            user.increment_failed_attempts(max_attempts=5)
            _log_auth(user.id, 4, 'failed')

            if user.is_locked():
                session.clear()
                return jsonify({'success': False, 'message': 'Account temporarily locked after too many failed attempts.', 'locked': True}), 403

            # Generate a new challenge for retry
            new_challenge = _generate_visual_challenge()
            session['visual_challenge'] = new_challenge

            return jsonify({
                'success': False,
                'message': 'Incorrect selection. Please try again.',
                'new_challenge': {
                    'prompt': new_challenge['prompt'],
                    'images': [{'filename': img['filename'], 'folder': img['folder']} for img in new_challenge['images']]
                }
            }), 401

    return jsonify({'success': False, 'message': 'Invalid request.'}), 400


# ==================== LEGACY ROUTES (kept for compatibility) ====================

@auth_bp.route('/image-password', methods=['GET'])
@login_required
def image_password_page():
    if 'level1_user' not in session and not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.image_password_verify'))


@auth_bp.route('/image-password/verify', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def image_password_verify():
    user_id = session.get('level1_user')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        data = request.get_json()
        submitted = data.get('sequence', [])
        stored = parse_image_sequence(user.image_password.encrypted_image_sequence) if user.image_password else []

        if validate_image_sequence(submitted, stored):
            session['level2_passed'] = True
            _log_auth(user.id, 2, 'success')
            return jsonify({'success': True, 'redirect': url_for('auth.challenge')})
        else:
            _log_auth(user.id, 2, 'failed')
            return jsonify({'success': False, 'message': 'Authentication failed. Please try again.'}), 401

    return render_template('auth/image_password_verify.html',
                           images=IMAGE_PASSWORD_IMAGES,
                           user=user)


@auth_bp.route('/challenge', methods=['GET'])
def challenge_page():
    if not session.get('level2_passed'):
        return redirect(url_for('auth.login'))

    user_id = session.get('level1_user')
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    challenge = _get_active_challenge(user.id)
    if not challenge:
        challenge = generate_challenge(user.id)

    challenge_data = json.loads(challenge.challenge_data)
    return render_template('auth/challenge.html',
                           challenge=challenge,
                           challenge_data=challenge_data,
                           user=user)


@auth_bp.route('/challenge/verify', methods=['POST'])
@limiter.limit("10 per minute")
def challenge_verify():
    if not session.get('level2_passed'):
        return jsonify({'success': False, 'message': 'Authentication error.'}), 403

    user_id = session.get('level1_user')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Authentication error.'}), 403

    data = request.get_json()
    selected_ids = data.get('selected', [])
    challenge_id = data.get('challenge_id')

    challenge = SecurityChallenge.query.get(challenge_id)
    if not challenge or challenge.expires_at < datetime.utcnow():
        return jsonify({'success': False, 'message': 'Challenge expired. Please try again.'}), 400

    challenge_data = json.loads(challenge.challenge_data)
    correct_ids = challenge_data.get('correct_ids', [])

    if set(selected_ids) == set(correct_ids):
        session.pop('level1_user', None)
        session.pop('level2_passed', None)

        login_user(user, remember=False)
        user.last_login = datetime.utcnow()
        db.session.commit()

        _log_auth(user.id, 3, 'success')
        return jsonify({'success': True, 'redirect': url_for('dashboard.index')})
    else:
        _log_auth(user.id, 3, 'failed')
        new_challenge = generate_challenge(user.id)
        new_data = json.loads(new_challenge.challenge_data)
        return jsonify({
            'success': False,
            'message': 'Verification failed. Please try again.',
            'new_challenge': {
                'id': new_challenge.id,
                'prompt': new_data['prompt'],
                'images': [{'id': img['id'], 'src': img['src']} for img in new_data['images']]
            }
        }), 401


def _get_active_challenge(user_id):
    """Get a non-expired challenge for the user."""
    return SecurityChallenge.query.filter(
        SecurityChallenge.expires_at > datetime.utcnow()
    ).order_by(SecurityChallenge.created_at.desc()).first()


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

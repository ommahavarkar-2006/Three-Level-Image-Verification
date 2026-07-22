import re
import json


def check_password_strength(password):
    """Returns a dict with strength score (0-4) and label."""
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;\'`~/]', password):
        score += 1

    score = min(score, 4)
    labels = ['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong']
    colors = ['#ef4444', '#f59e0b', '#3b82f6', '#22c55e', '#06b6d4']

    return {
        'score': score,
        'label': labels[score],
        'color': colors[score],
        'percent': score * 25
    }


def validate_image_sequence(submitted_sequence, stored_sequence):
    """Compare submitted image sequence with stored sequence.
    Both should be lists of image ID strings.
    Returns True if they match exactly (order matters).
    """
    if not submitted_sequence or not stored_sequence:
        return False
    return submitted_sequence == stored_sequence


def parse_image_sequence(sequence_json):
    """Parse stored JSON image sequence string into a list."""
    try:
        return json.loads(sequence_json)
    except (json.JSONDecodeError, TypeError):
        return []

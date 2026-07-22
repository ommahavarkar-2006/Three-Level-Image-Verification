import json
import random
from datetime import datetime, timedelta
from app.extensions import db
from app.models.security_challenge import SecurityChallenge

# Challenge categories with images
CHALLENGE_CATEGORIES = {
    'bicycle': {
        'prompt': 'Select all images containing a bicycle',
        'correct': ['bicycle1.svg', 'bicycle2.svg', 'bicycle3.svg'],
        'incorrect': ['car1.svg', 'car2.svg', 'tree1.svg', 'tree2.svg', 'flower1.svg', 'house1.svg']
    },
    'car': {
        'prompt': 'Select all images containing a car',
        'correct': ['car1.svg', 'car2.svg', 'car3.svg'],
        'incorrect': ['bicycle1.svg', 'bicycle2.svg', 'tree1.svg', 'tree2.svg', 'flower1.svg', 'house1.svg']
    },
    'tree': {
        'prompt': 'Select all images containing a tree',
        'correct': ['tree1.svg', 'tree2.svg', 'tree3.svg'],
        'incorrect': ['car1.svg', 'car2.svg', 'bicycle1.svg', 'flower1.svg', 'house1.svg', 'rocket1.svg']
    },
    'flower': {
        'prompt': 'Select all images containing a flower',
        'correct': ['flower1.svg', 'flower2.svg', 'flower3.svg'],
        'incorrect': ['car1.svg', 'tree1.svg', 'bicycle1.svg', 'house1.svg', 'rocket1.svg', 'piano1.svg']
    }
}


def generate_challenge(user_id=None):
    """Generate a new visual security challenge."""
    category_name = random.choice(list(CHALLENGE_CATEGORIES.keys()))
    category = CHALLENGE_CATEGORIES[category_name]

    # Select 2-3 correct images
    num_correct = random.randint(2, 3)
    correct_images = random.sample(category['correct'], min(num_correct, len(category['correct'])))

    # Select 3-5 incorrect images
    num_incorrect = random.randint(3, 5)
    incorrect_images = random.sample(category['incorrect'], min(num_incorrect, len(category['incorrect'])))

    # Build image list with IDs
    images = []
    correct_ids = []

    for img_src in correct_images:
        img_id = img_src.replace('.svg', '')
        images.append({
            'id': img_id,
            'src': img_src,
            'is_correct': True
        })
        correct_ids.append(img_id)

    for img_src in incorrect_images:
        img_id = img_src.replace('.svg', '')
        images.append({
            'id': img_id,
            'src': img_src,
            'is_correct': False
        })

    random.shuffle(images)

    challenge_data = {
        'prompt': category['prompt'],
        'category': category_name,
        'images': images,
        'correct_ids': correct_ids
    }

    challenge = SecurityChallenge(
        challenge_type=f'select_{category_name}',
        challenge_data=json.dumps(challenge_data),
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )
    db.session.add(challenge)
    db.session.commit()

    return challenge

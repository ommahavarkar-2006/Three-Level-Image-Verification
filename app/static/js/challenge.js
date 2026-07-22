// SECUREVISION — Challenge JS (Level 3)

let challengeSelected = [];

function toggleChallengeSelect(card, imageId) {
    const idx = challengeSelected.indexOf(imageId);
    if (idx > -1) {
        challengeSelected.splice(idx, 1);
        card.classList.remove('selected');
    } else {
        challengeSelected.push(imageId);
        card.classList.add('selected');
    }
}

function submitChallenge() {
    const btn = document.getElementById('submitChallengeBtn');
    const errDiv = document.getElementById('challengeError');
    const successDiv = document.getElementById('challengeSuccess');

    if (!btn) return;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Verifying...';

    fetch(CHALLENGE_VERIFY_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({
            selected: challengeSelected,
            challenge_id: currentChallengeId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (errDiv) errDiv.classList.add('d-none');
            if (successDiv) successDiv.classList.remove('d-none');
            setTimeout(function() {
                window.location.href = data.redirect;
            }, 1500);
        } else {
            btn.disabled = false;
            btn.innerHTML = 'Submit Verification <i class="bi bi-shield-fill-check ms-2"></i>';

            if (errDiv) {
                errDiv.textContent = data.message || 'Verification failed.';
                errDiv.classList.remove('d-none');
            }
            if (successDiv) successDiv.classList.add('d-none');

            // Reset selection
            challengeSelected = [];
            document.querySelectorAll('.challenge-card.selected').forEach(c => c.classList.remove('selected'));

            // Load new challenge if provided
            if (data.new_challenge) {
                loadNewChallenge(data.new_challenge);
            }
        }
    })
    .catch(err => {
        btn.disabled = false;
        btn.innerHTML = 'Submit Verification <i class="bi bi-shield-fill-check ms-2"></i>';
        if (errDiv) {
            errDiv.textContent = 'An error occurred. Please try again.';
            errDiv.classList.remove('d-none');
        }
    });
}

function loadNewChallenge(challenge) {
    currentChallengeId = challenge.id;
    const promptEl = document.getElementById('challengePrompt');
    const grid = document.getElementById('challengeGrid');

    if (promptEl) promptEl.textContent = challenge.prompt;

    if (grid) {
        grid.innerHTML = '';
        challenge.images.forEach(function(img) {
            const col = document.createElement('div');
            col.className = 'col-4 col-md-3';
            col.innerHTML = '<div class="challenge-card glass-card hover-lift text-center p-3 cursor-pointer" data-img-id="' + img.id + '" onclick="toggleChallengeSelect(this, \'' + img.id + '\')">' +
                '<img src="/static/images/challenges/' + img.src + '" alt="Challenge" class="img-fluid" style="height:100px;object-fit:contain;">' +
                '</div>';
            grid.appendChild(col);
        });
    }
}
